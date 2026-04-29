---
title: "Multithreaded simple data type access and atomic variables"
date: "2008-12-23T13:55:29"
original_url: "http://www.alexonlinux.com/multithreaded-simple-data-type-access-and-atomic-variables"
categories: ["Programming Articles"]
tags: ["atomic", "linux", "multithreaded", "mutex", "pthread", "semaphore", "spinlock", "thread"]
---

# Introduction

In this article I would like to continue subject I started in my previous two
essays ([essay 1]({{< relref "essays/do-you-need-a-mutex-to-protect-an-int.md"
>}}) and [essay 2]({{< relref "essays/pthread-spinlocks.md" >}})). Question I am
trying to answer is what is the most efficient, yet safe way of accessing simple
data type variables from two or more threads. I.e. how to change a variable from
two threads at the same time, without screwing its value.

[In my first essay]({{< relref "essays/do-you-need-a-mutex-to-protect-an-int.md"
>}}) I’ve shown how easy it is to turn variable value into garbage by modifying
it from two or more threads. [In my second essay]({{< relref
"essays/pthread-spinlocks.md" >}}) I am talking about spinlocks, a recent
addition into `pthread` library. Spinlocks indeed can help to solve the problem.
Yet spinlocks more suitable for protecting small data structures rather than
simple data types such as `int` and `long`. Atomic variables, on the other hand,
are perfect for the later task.

Key thing about atomic variables is that once someone starts reading or writing
it, nothing else cannot interrupt the process and come in the middle. I.e.
nothing can split the process of accessing atomic variable into two. This is why
they called atomic.

On the practical side, atomic variables are the best solution for the problem of
simultaneous access to a simple variable from two or more threads.

# How atomic variables work

This is actually quiet simple. Intel x86 and x86_64 processor architectures (as
well as vast majority of other modern CPU architectures) has instructions that
allow one to lock FSB, while doing some memory access. FSB stands for Front
Serial Bus. This is the bus that processor use to communicate with RAM. I.e.
locking FSB will prevent from any other processor (core), and process running on
that processor, from accessing RAM. And this is exactly what we need to
implement atomic variables.

Atomic variables being widely used in kernel, but from some reason no-one
bothered to implement them for user-mode folks. Until gcc 4.1.2.

# Atomic variables size limitations

From practical considerations, gurus at Intel did not implement FSB locking for
every possible memory access. For instance, for quiet some time, Intel
processors allow `memcpy()` and `memcmp()` implementation with one processor
instruction. But locking FSB while copying large memory buffer can be too
expensive.

In practice you can lock FSB while accessing 1, 2, 4 and 8 byte long integers.
Almost transparently, `gcc` allows you to do atomic operations on `int`s,
`long`s, and `long long`s (and their unsigned counterparts).

# Use cases

Incrementing a variable and knowing that no-one else screws its value is nice,
but not enough. Consider following piece of pseudo-code.

```c
decrement_atomic_value();
if (atomic_value() == 0)
    fire_a_gun();
```

Let us imagine that the value of an atomic variable is 1. What happens if two
threads of execution try to execute this piece of pseudo-C simultaneously?

Back to our simulation. It is possible that thread 1 will execute line 1 and
stop, while thread 2 will execute line 1 and continue executing line 2. Later
thread 1 will wake up and execute line 2.

![two_threads]({{< relurl "assets/2008-12-23T135529 Multithreaded simple data type access and atomic variables/two_threads-1d8b30a3c0.png" >}})

When this happens, no one of the threads will run `fire_a_gun()` routine (line
3). This is obviously wrong behavior and if we were protecting this piece of
code with a mutex or a spinlock this would not have happened.

> In case you’re wondering how likely something like this to happen, be sure
> that this is very likely. When I first started working with multithreaded
> programing I was amazed to find out that despite our intuition tells us that
> scenario I described earlier is unlikely, it happens overwhelmingly often.

As I mentioned, we could solve this problem by giving up on atomic variables and
using spinlock or mutex instead. Luckily, we can still use atomic variables.
`gcc` developers have thought about our needs and this particular problem and
offered a solution. Lets see actual routines that operate atomic variables.

# The real thing…

There are several simple functions that do the job. First of all, there are
twelve (yes, twelve – 12) functions that do atomic add, substitution, and
logical atomic or, and, xor and nand. There are two functions for each
operation. One that returns value of the variable before changing it and another
that returns value of the variable after changing it.

Here are the actual functions:

```c
type __sync_fetch_and_add (type *ptr, type value);
type __sync_fetch_and_sub (type *ptr, type value);
type __sync_fetch_and_or (type *ptr, type value);
type __sync_fetch_and_and (type *ptr, type value);
type __sync_fetch_and_xor (type *ptr, type value);
type __sync_fetch_and_nand (type *ptr, type value);
```

These are functions that return value of the variable before changing it.
Following functions, on the other hand, return value of the variable after
changing it.

```c
type __sync_add_and_fetch (type *ptr, type value);
type __sync_sub_and_fetch (type *ptr, type value);
type __sync_or_and_fetch (type *ptr, type value);
type __sync_and_and_fetch (type *ptr, type value);
type __sync_xor_and_fetch (type *ptr, type value);
type __sync_nand_and_fetch (type *ptr, type value);
```

`type` in each of the expressions can be one of the following:

- int unsigned int long unsigned long long long unsigned long long

These are so called built-in functions, meaning that you don’t have to include
anything to use them.

# Time to see some action

Back to the example I started in the [first essay]({{< relref
"essays/do-you-need-a-mutex-to-protect-an-int.md" >}}) I mentioned earlier.

To remind you, this small program opens several of threads. Number of threads is
as number of CPUs in the computer. Then it binds each one of the threads to one
of the CPUs. Finally each thread runs a loop and increments a global integer 1
million times.

```c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <sched.h>
#include <linux/unistd.h>
#include <sys/syscall.h>
#include <errno.h>
#define INC_TO 1000000 // one million...
int global_int = 0;
pid_t gettid( void )
{
    return syscall( __NR_gettid );
}
void *thread_routine( void *arg )
{
    int i;
    int proc_num = (int)(long)arg;
    cpu_set_t set;
    CPU_ZERO( &set );
    CPU_SET( proc_num, &set );
    if (sched_setaffinity( gettid(), sizeof( cpu_set_t ), &set ))
    {
        perror( "sched_setaffinity" );
        return NULL;
    }
    for (i = 0; i < INC_TO; i++)
    {
//        global_int++;
        __sync_fetch_and_add( &global_int, 1 );
    }
    return NULL;
}
int main()
{
    int procs = 0;
    int i;
    pthread_t *thrs;
    // Getting number of CPUs
    procs = (int)sysconf( _SC_NPROCESSORS_ONLN );
    if (procs < 0)
    {
        perror( "sysconf" );
        return -1;
    }
    thrs = malloc( sizeof( pthread_t ) * procs );
    if (thrs == NULL)
    {
        perror( "malloc" );
        return -1;
    }
    printf( "Starting %d threads...\n", procs );
    for (i = 0; i < procs; i++)
    {
        if (pthread_create( &thrs[i], NULL, thread_routine,
            (void *)(long)i ))
        {
            perror( "pthread_create" );
            procs = i;
            break;
        }
    }
    for (i = 0; i < procs; i++)
        pthread_join( thrs[i], NULL );
    free( thrs );
    printf( "After doing all the math, global_int value is: %d\n",
        global_int );
    printf( "Expected value is: %d\n", INC_TO * procs );
    return 0;
}
```

To compile and run, throw this snippet into a file and run:

```bash
gcc -pthread "file name"
```

Then run `./a.out` to execute the program.

Note lines 36 and 37. Instead of simply incrementing the variable, I use
built-in function `__sync_fetch_and_add()`. Running this code obviously produces
expected results – i.e. value of `global_int` is 4,000,000 as expected (number
of CPUs in the machine multiply 1 million – in my case this is a 4 core
machine). Remember that [when I ran this code snippet leaving line 36 as is]({{<
relref "essays/do-you-need-a-mutex-to-protect-an-int.md" >}}), the result was
1,908,090 and not 4,000,000 as we’d expect.

# Precautions

When using atomic variables, some extra precautions have to be taken. One
serious problem with atomic variable implementation in `gcc` is that it allows
you to do atomic operations on regular variables. I.e. there is no clear
distinction between atomic variables and regular variables. There is nothing
that prevents you from incrementing value of the atomic variable with
`__sync_fetch_and_add()` as I just demonstrated and later in the code doing same
thing with regular ++ operator.

Obviously this might be a serious problem. Things tend to be forgotten and it is
a matter of time until someone in your project or even you yourself will modify
value of the variable using regular operators, instead of atomic functions that
`gcc` has.

To address this problem, I strongly suggest wrapping around atomic functions and
variables with either ADT in C or C++ class.

# Conslusion

This article concludes a series or articles and essays where we investigate and
study newest techniques in the world of multithreaded programming for Linux.
Hope you’ll find these essays and article useful. As usual, in case you have
further questions please don’t hesitate to email me to
alexander.sandler@gmail.com.
