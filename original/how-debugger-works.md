---
title: "How debugger works"
type: "post"
created_at: "2008-03-24T11:39:18"
original_url: "http://www.alexonlinux.com/how-debugger-works"
categories: ["Programming Articles"]
tags: ["breakpoint", "cc", "coff", "debug", "debugger", "elf", "example", "int3", "kernel", "linux", "ptrace", "single", "step", "unix", "Windows"]
---

### Table of contents

[Introduction](#introduction)
[Kernel support](#kernel_support)
**[ptrace()](#ptrace())
[Starting to debug](#starting_to_debug)
[Debugger-debuggee synchronization](#debugger-debuggee_synchronization)
[A new debugger was born](#a_new_debugger_was_born)
[The magic behind INT 3](#the_magic_behind_int_3)
[Breakpoints hands on](#breakpoints_hands_on)
[Single steps](#single_steps)
[Conclusion](#conclusion)

### Introduction [BACK TO TOC](#table_of_contents)

In this article, I’d like to tell you how real debugger works. What happens under the hood and why it happens. We’ll even write our own small debugger and see it in action.

I will talk about Linux, although same principles apply to other operating systems. Also, we’ll talk about x86 architecture. This is because it is the most common architecture today. On the other hand, even if you’re working with other architecture, you will find this article useful because, again, same principles work everywhere.

### Kernel support [BACK TO TOC](#table_of_contents)

Actual debugging requires operating system kernel support and here’s why. Think about it. We’re living in a world where one process reading memory belonging to another process is a serious security vulnerability. Yet, when debugging a program, we would like to access a memory that is part of debugged process’s (debuggee) memory space, from debugger process. It is a bit of a problem, isn’t it? We could, of course, try somehow to use same memory space for both debugger and debuggee, but then what if debuggee itself creates processes. This really complicates things.

Debugger support has to be part of the operating system kernel. Kernel able to read and write memory that belongs to each and every process in the system. Furthermore, as long as process is not running, kernel can see value of its registers and debugger have to be able to know values of the debuggee registers. Otherwise it won’t be able to tell you where the debuggee has stopped (when we pressed CTRL-C in gdb for instance).

As we spoke about where debugger support starts we already mentioned several of the features that we need in order to have debugging support in operating system. We don’t want just any process to be able to debug other processes. Someone has to monitor debuggers and debuggees. Hence the debugger has to tell the kernel that it is going to debug certain process and kernel has to either permit or deny this request. Therefore, we need an ability to tell the kernel that certain process is a debugger and it is about to debug other process. Also we need an ability to query and set values from debuggee’s memory space. And we need an ability to query and set values of the debuggee’s registers, when it stops.

And operating system lets us to do all this. Each operating system does it in it’s manner of course. Linux provides single system call named*ptrace()*(defined in*sys/ptrace.h*), which allows to do all these operations and much more.

### *ptrace()*[BACK TO TOC](#table_of_contents)

*ptrace()*accepts four arguments. First is one of the values from*enum __ptrace_request*that defined in*sys/ptrace.h*. This argument specifies what operation we would like to do, whether it is reading debuggee registers or altering values in its memory. Second argument specifies*pid*of the debuggee process. It’s not very obvious, but single process can debug several other processes. Thus we have to tell exactly what process we’re referring. Last two arguments are optional arguments for the call.

### Starting to debug [BACK TO TOC](#table_of_contents)

One of the first things debuggers do to start debugging certain process is attaching to it or running it. There is a*ptrace()*operation for each one of these cases.

First called*PTRACE_TRACEME*, tells the kernel that calling process wants its parent to debug itself. I.e. me calling*ptrace( PTRACE_TRACEME )*means I want my dad to debug me. This comes handy when you want debugger process to spawn the debuggee. In this case you do*fork()*creating a new process, then*ptrace( PTRACE_TRACEME )*and then you call*exec()*or*execve()*.

Second operation called*PTRACE_ATTACH*. It tells the kernel that calling process should become debugging parent of the process being called. Debugging parent means debugger and a parent process.

### Debugger-debuggee synchronization [BACK TO TOC](#table_of_contents)

Alright. Now we told operating system that we are going to debug certain process. Operating system made it our child process. Good. This is a great time for us to have the debuggee stopped and us doing preparations before we actually start to debug. We may want to, for instance, analyze executable that we run and place a breakpoints before we actually start debugging. So, how do we stop the debuggee and let debugger do its thing?

Operating system does that for us using signals. Actually, operating system notifies us, the debugger, about all kinds of events that occur in debuggee and it does all that with signals. This includes the “debuggee is ready to shoot” signal. In particular, if we attach to existing process it receives*SIGSTOP*and we receive*SIGCHLD*once it actually stops. If we spawn a new process and it did*ptrace( PTRACE_TRACEME )*it will receive*SIGTRAP*signal once it attempts to*exec()*or*execve()*. We will be notified with*SIGCHLD*about this, of course.

### A new debugger was born [BACK TO TOC](#table_of_contents)

Now lets see code that actually demonstrates that. Complete listing can be found [here](http://www.alexonlinux.com/wp-content/uploads/2008/03/listing1.c).

The debuggee does the following…

```text
.
.
.
    if (ptrace( PTRACE_TRACEME, 0, NULL, NULL ))
    {
        perror( "ptrace" );
        return;
    } 

    execve( "/bin/ls", argv, envp );
.
.
.
```

Note the*ptrace( PTRACE_TRACEME )*followed by*execve*(). This is what real debuggers do to spawn the process that going to be debugged. As you know,*execve()*replaces current executable image and memory of the current process with the executable and memory space belonging to program that being*execve()*‘d. Once kernel finishes this operation, it sends*SIGTRAP*to calling process and*SIGCHLD*to the debugger. The debugger receives appropriate notifications via signals and via*wait()*that returns. Here is the debugger’s code.

```text
.
.
.
    do {
        child = wait( &status );
        printf( "Debugger exited wait()\n" );
        if (WIFSTOPPED( status ))
        {
            printf( "Child has stopped due to signal %d\n",
                WSTOPSIG( status ) );
        }
        if (WIFSIGNALED( status ))
        {
            printf( "Child %ld received signal %d\n",
                    (long)child,
                    WTERMSIG(status) );
        }
    } while (!WIFEXITED( status ));
.
.
.
```

Compiling and running listing1.c produces following output:

```text
In debuggee process 14095
In debugger process 14094
Process 14094 received signal 17
Debugger exited wait()
Child has stopped due to signal 5
```

Here we can clearly see that debugger indeed receives a signal and gets notified via*wait()*. If we want to place a breakpoint before we start to debug the process, this is our chance. Lets talk about how we can do something like that.

### The magic behind INT 3 [BACK TO TOC](#table_of_contents)

It is time to dig a bit into subject that is not adored by most of the programmers and that is assembler language. I am afraid we don’t have much choice because breakpoints work on assembler level.

We have to understand that each our compiled program is actually a set of instructions that tells CPU what to do. Some of our C expressions translated into single instruction, while others may be translated into hundreds and even thousands of instructions. Instruction may be bigger or smaller. From 1 byte up to 15 bytes long for modern CPUs (*Intel**x86*_64).

Debuggers mostly operate on CPU instruction level. The matter of fact that*gdb*understands C/C++ code and allows you to place breakpoints at certain C/C++ line is only an enhancement over*gdb*‘s basic ability to place breakpoints on certain instruction.

There are several ways to place breakpoints. The most widely used is the INT 3 instruction. It is a single byte operation code instruction that once reached by CPU, tells it to call special breakpoint interrupt handler, provided by operating system during its initialization. Since INT 3 instruction operation code is so small, we can safely substitute any instruction with it. Once operating system’s interrupt handler called, it figures what process reached a breakpoint and notifies it and its debugging process via signals.

### Breakpoints hands on [BACK TO TOC](#table_of_contents)

Lets return to our debuggee/debugger friends. As we mentioned debugger does have a chance to place a breakpoint before letting the debuggee process to run. Lets see how this can be done.

Breakpoints placed with INT 3 instruction. Before writing the actual 0xcc (INT 3 operation code), we should figure where to place the instruction. For purpose of this article we will do it manually. On the contrary, real debuggers include complex logic that calculates where and when to place the breakpoints.*gdb*places several breakpoints by itself, without you even knowing about it. And obviously it has functionality that places breakpoints once you ask it to do so.

In our previous example we had our debuggee process executing*ls*. It is not suitable for our next demonstration. We will need a sample program that would let us easily demonstrate breakpoints in action.[Here](http://www.alexonlinux.com/wp-content/uploads/2008/03/sleeper.c) it is.

```text
#include <stdio.h>

int main()
{
        printf( "~~~~~~~~~~~~> Before breakpoint\n" );
        // The breakpoint
        printf( "~~~~~~~~~~~~> After breakpoint\n" );

        return 0;
}
```

And here is the disassembler output of the*main()*routine.

```text
0000000000400508 <main>:
  400508:       55                      push   %rbp
  400509:       48 89 e5                mov    %rsp,%rbp
  40050c:       bf 18 06 40 00          mov    $0x400618,%edi
  400511:       e8 12 ff ff ff          callq  400428 <puts@plt>
  400516:       bf 2a 06 40 00          mov    $0x40062a,%edi
  40051b:       e8 08 ff ff ff          callq  400428 <puts@plt>
  400520:       b8 00 00 00 00          mov    $0x0,%eax
  400525:       c9                      leaveq
  400526:       c3                      retq
```

We can see that if we will place a breakpoint at address 0x400516, we will see a printout before reaching the breakpoint and right after reaching it. For the sake of our demonstration, we will place a breakpoint at this address. Once we will reach the breakpoint, we will sleep and then let the debuggee running. We should see debuggee producing first printout, then sleeping for a few seconds and then producing second printout.

We’ll achieve our goal in several steps.

1. First of all, we should*fork()*off the debuggee. We already did something similar.
2. Next step is to intercept the*execve()*call in debuggee. Been there, done that.
3. Here’s something new. We should modify a byte at address 0x400516 from 0xbf to 0xcc, saving original value (0xbf). This is how we place the breakpoint.
4. Next, we’re going to*wait()*for the process. Once it will reach the breakpoint, we’ll be notified.
5. Once the debuggee reaches the breakpoint we want to restore the code we broke with our 0xcc to its original state.
6. In addition, we want to fix value of RIP register. This register tells CPU what is the location in memory of next meaningful instruction for it to execute. It’s value will be 0x400517, one byte after 0xcc that we placed. We want to set the RIP register to 0x400516 value because we don’t want the CPU to skip over that MOV instruction that we broke with our 0xcc.
7. Finally, we want to wait five seconds for the sake of demonstration and let the debuggee continue running.

First things first. Lets see how we do step 3.

```text
.
.
.
        addr = 0x400516;

        data = ptrace( PTRACE_PEEKTEXT, child, (void *)addr, NULL );
        orig_data = data;
        data = (data & ~0xff) | 0xcc;
        ptrace( PTRACE_POKETEXT, child, (void *)addr, data );
.
.
.
```

Again, we can see how*ptrace()*does the job for us. First we peek 8 (*sizeof( long )*) bytes from address 0x400516. On some architectures this could cause lots of headache because of unaligned memory access. Luckily, we’re on x86_64 and unaligned memory accesses are permitted. Next we set the lowest byte to be 0xcc – INT 3 instruction. Finally, we place 8 bytes back to their place.

We’ve seen how we can wait for certain event in debuggee. Also, we now know how to restore the original value at address 0x400516. So we can skip over steps 4-5 and jump right into step 6. This is something that we haven’t done so far.

What we have to do is to read debuggee registers, change them and write them back. Again*ptrace()*does all the job for us.

```text
.
.
.
        struct user_regs_struct regs;
.
.
.
        ptrace( PTRACE_GETREGS, child, NULL, &regs );
        regs.rip = addr;
        ptrace( PTRACE_SETREGS, child, NULL, &regs );
.
.
.
```

Things are not too well documented here. For instance*ptrace()*documentation never mentions*struct user_regs_struct*, however this is what*ptrace()*system call expects to receive in kernel. Once we know what we should use as*ptrace()*arguments, it is easy. We use*PTRACE_GETREGS*operation to obtain values of debuggee’s registers, we modify the RIP register and write them back with*PTRACE_SETREGS*operation. Clear and simple.

Lets see how things actually work. You can find complete listing of debugger process [here](http://www.alexonlinux.com/wp-content/uploads/2008/03/listing2.c). Compiling and running listing2.c, produces following output.

```text
In debuggee process 29843
In debugger process 29842
Process 29842 received signal 17
~~~~~~~~~~~~> Before breakpoint
Process 29842 received signal 17
RIP before resuming child is 400517
Time before debugger falling asleep: 1206346035
Time after debugger falling asleep: 1206346040. Resuming debuggee...
~~~~~~~~~~~~> After breakpoint
Process 29842 received signal 17
Debuggee exited...
Debugger exiting...
```

You can see that “Before breakpoint” printout appears 5 seconds before “After breakpoint” printout. The “RIP before resuming child is 400517” clearly indicates that the debuggee has stopped on address 0x400517, as we expected.

### Single steps [BACK TO TOC](#table_of_contents)

After seeing how easy to place a breakpoint, you can guess that stepping over one line of C/C++ code is simply a matter of placing a breakpoint on the next line of code. This is exactly what*gdb*does when you want it to single step over some expression.

### Conclusion [BACK TO TOC](#table_of_contents)

Debuggers and how they work often associated with some kind of magic.

Debuggers, and*gdb*as an example, are exceptionally complicated piece of software. Placing breakpoints and single stepping is only a small fraction of what it is able to do.*gdb*in particular works on dozens of hardware architectures. It supports remote debugging. It is perhaps the most advanced and complicated executable analyzer. It knows when a program loads dynamic library and analyzes the code of that library automatically. It supports bunch of programming languages – from C/C++ to ADA. And these are just few out of its features.

On the contrary, we’ve seen how easy to start debugging certain process, place a breakpoint, etc. The basic functionality that allows debugging is in the operating system and in the CPU, waiting for us to use it.
