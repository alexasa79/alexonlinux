---
title: "Signal handling in Linux"
type: "post"
created_at: "2009-04-19T20:16:17"
original_url: "http://www.alexonlinux.com/signal-handling-in-linux"
categories: ["Programming Articles"]
tags: ["exception", "linux", "notifications", "programming", "sigaction", "sigkill", "signal", "thread"]
---

# Table of contents

[Introduction to the series](#introduction_to_the_series)
[Introduction to the article](#introduction_to_the_article)
[Way of working with Bazaar](#way_of_working_with_bazaar)
[Demo setup description](#demo_setup_description)
[Directory and user configuration](#directory_and_user_configuration)
[The basics](#the_basics)
[Creating a project](#creating_a_project)
[Checking-out the project](#checking-out_the_project)
[Adding files to the project](#adding_files_to_the_project)
[Committing files](#committing_files)
[Few words about revision numbers in Bazaar](#few_words_about_revision_numbers_in_bazaar)
[Local commits or offline commits](#local_commits_or_offline_commits)
[Committing local commits to remote branch](#committing_local_commits_to_remote_branch)
[Multi-user environment](#multi-user_environment)
[Making modifications to files and viewing differences](#making_modifications_to_files_and_viewing_differences)
[Committing non-up-to-date file](#committing_non-up-to-date_file)
[Merging with the latest version of the file](#merging_with_the_latest_version_of_the_file)
[Introduction](#introduction)
[What reference counting needed for?](#what_reference_counting_needed_for?)
[This is how we will use atomic variables to count references to objects](#this_is_how_we_will_use_atomic_variables_to_count_references_to_objects)
[The naive approach](#the_naive_approach)
[The RCU approach](#the_rcu_approach)
[Where atomic variables coming from?](#where_atomic_variables_coming_from?)
[Conclusion](#conclusion)
[Introduction](#introduction)
[What do we do with command line options](#what_do_we_do_with_command_line_options)
**[optparsebasics](#optparse_basics)
[Adding options](#adding_options)
[Specifying help string for an option](#specifying_help_string_for_an_option)
**[Tellingoptparseto parse arguments](#telling_optparse_to_parse_arguments)
[Putting it together](#putting_it_together)
**[optparsecookbook](#optparse_cookbook)
[Support for a standalone command line options](#support_for_a_standalone_command_line_options)
[Support for mandatory (required) options.](#support_for_mandatory_(required)_options.)
[Support for options with one or more arguments](#support_for_options_with_one_or_more_arguments)
[Option destination types](#option_destination_types)
[Dependencies between options](#dependencies_between_options)
[Help screen customizations](#help_screen_customizations)
[Grouping options](#grouping_options)
[Changing programs usage string](#changing_programs_usage_string)
[Telling option’s default value](#telling_option’s_default_value)
[Better argument description](#better_argument_description)
[Adding program description](#adding_program_description)
[Adding epilog](#adding_epilog)
[Program version string](#program_version_string)
[Conclusion](#conclusion)
[Introduction](#introduction)
[What are signals?](#what_are_signals?)
[Signal as interrupt](#signal_as_interrupt)
[Signal masks](#signal_masks)
[What signals are good for](#what_signals_are_good_for)
[Signals that report exceptions](#signals_that_report_exceptions)
[Other uses of signals](#other_uses_of_signals)
[Types of signals](#types_of_signals)
[Handling exception signals](#handling_exception_signals)
[SIGKILL and SIGSTOP](#sigkill_and_sigstop)
[SIGKILL](#sigkill)
[SIGSTOP](#sigstop)
[Registering signal handler](#registering_signal_handler)
**[signal()](#signal())
[Ignoring signals and restoring original signal handler function](#ignoring_signals_and_restoring_original_signal_handler_function)
**[sigaction()](#sigaction())
**[sigaction()in action](#sigaction()_in_action)
[Conclusion](#conclusion)

# Introduction [BACK TO TOC](#table_of_contents)

Perhaps any engineer developing for Linux encounters this problem. What’s is the right way to terminate the program? What are the ways to receive notifications from operating system about events that occur.

Traditional Unix systems have the answers ready. The answer to these questions is signals.

This article addresses these questions. Here, I’ll try to explain what signals are, their nature. We’ll talk about what are the right ways to handle signals, what signals to handle and what are the pitfalls of signal handling in Linux in particular.

# What are signals?[BACK TO TOC](#table_of_contents)

Signal is a notification, a message sent by either operating system or some application to your program (or one of its threads).

Each signal identified by a number, from 1 to 31. Signals don’t carry any argument and their names are mostly self explanatory. For instance SIGKILL or signal number 9 tells the program that someone tries to kill it.

## Signal as interrupt [BACK TO TOC](#table_of_contents)

In addition to informative nature of signals, they also interrupt your program. I.e to handle a signal, one of the threads in your program, stops its execution and temporarily switches to signal handler. Note that as in version 2.6 of Linux kernel, most of the signals interrupt only one thread and not the entire application as it used to be once. Moreover, signal handler itself can be interrupted by some other signal.

# Signal masks [BACK TO TOC](#table_of_contents)

Each one of signals can be in one of three states:

- We may have our own signal handler for the signal.
- Signal may be handled by the default handler. Every signal has its default handler function. For instance, SIGINT default handler will terminate your application.
- Signal may be ignored. Ignoring signal sometimes referred to as blocking signal.

When manipulating signals and managing signal configuration, it is often easier to manage a so called signal mask. It is a bit-mask, where each bit has a corresponding signal. There are 32 (actually 31, 0 doesn’t count) different signals, thus we can use single 32-bit integer (unsigned int) to keep information about 32 signals. This is exactly what operating system does. Moreover, signal masks used as arguments in different system calls, thus we will have to work with signal masks.

The C library assigns default signal handlers. This means that even if you leave signals untouched, your program will process signals and will respond to them according to default behavior. I will describe default signal behavior a little later in this article.

# What signals are good for [BACK TO TOC](#table_of_contents)

Signals, as their name implies, used to signal something. There are several types of signals, each indicating something of its own. For instance SIGINT that I already mentioned, tells your program that someone tries to interrupt it with CTRL-C.

Dedication of each signal is a matter of semantics. I.e. you may want to decide what action shall be associated with each one of the signals. You may decide that some signal will cause your program to print something or draw something on the screen. It is up to you, most of the time. However, there is a common convention of what each and every signal should do. According to this common convention SIGINT expected to cause your program to terminate itself. This is the default response for SIGINT signal and it is in your interest to keep it this way. It is a question of usability. No one wants a program that cannot be interrupted.

## Signals that report exceptions [BACK TO TOC](#table_of_contents)

Another way of using signals is to indicate that that something bad have happened. For instance when your program causes a segmentation fault, operating system sends SIGSEGV signal to your application.

## Other uses of signals [BACK TO TOC](#table_of_contents)

Signals have several different usages. For instance debuggers rely on signals to receive events about programs that being debugged (read more about this in my article [How Debugger Works](http://www.alexonlinux.com/how-debugger-works)). Signals is one of so called IPC – Inter Process Communication mechanisms. IPC used to, as the abbreviation implies, to allow processes communicate with one another.

Another common use is when user wishes that our program will reinitialize itself, but not terminate. In this case, user can send our program a signal from the terminal, using a program called*kill*. You may be already familiar with this program. It used to kill processes. The truth is that it sends a signal. Each signal has a number that identifies it. By default it sends signal 15, SIGTERM, but it can send just any signal.

Lets see most common and their use.

# Types of signals [BACK TO TOC](#table_of_contents)

- **SIGHUP
**This signal indicates that someone has killed the controlling terminal. For instance, lets say our program runs in xterm or in gnome-terminal. When someone kills the terminal program, without killing applications running inside of terminal window, operating system sends SIGHUP to the program. Default handler for this signal will terminate your program.
*Thanks to Mark Pettit for the tip.*
- **SIGINT**
This is the signal that being sent to your application when it is running in a foreground in a terminal and someone presses CTRL-C. Default handler of this signal will quietly terminate your program.
- **SIGQUIT**
Again, according to documentation, this signal means “Quit from keyboard”. In reality I couldn’t find who sends this signal. I.e. you can only send it explicitly.
- **SIGILL**
Illegal instruction signal. This is a exception signal, sent to your application by the operating system when it encounters an illegal instruction inside of your program. Something like this may happen when executable file of your program has been corrupted. Another option is when your program loads dynamic library that has been corrupted. Consider this as an exception of a kind, but the one that is very unlikely to happen.
- **SIGABRT**
Abort signal means you used used*abort()*API inside of your program. It is yet another method to terminate your program.*abort()*issues SIGABRT signal which in its term terminates your program (unless handled by your custom handler). It is up to you to decide whether you want to use*abort()*or not.
- **SIGFPE**
Floating point exception. This is another exception signal, issued by operating system when your application caused an exception.
- **SIGSEGV**
This is an exception signal as well. Operating system sends a program this signal when it tries to access memory that does not belong to it.
- **SIGPIPE**
Broken pipe. As documentation states, this signal sent to your program when you try to write into pipe (another IPC) with no readers on the other side.
- **SIGALRM**
Alarm signal. Sent to your program using*alarm()*system call. The*alarm()*system call is basically a timer that allows you to receive SIGALRM in preconfigured number of seconds. This can be handy, although there are more accurate timer API out there.
- **SIGTERM**
This signal tells your program to terminate itself. Consider this as a signal to cleanly shut down while SIGKILL is an abnormal termination signal.
- **SIGCHLD**
Tells you that a child process of your program has stopped or terminated. This is handy when you wish to synchronize your process with a process with its child*.*
- **SIGUSR1**and**SIGUSR2**
Finally, SIGUSR1 and SIGUSR2 are two signals that have no predefined meaning and are left for your consideration. You may use these signals to synchronise your program with some other program or to communicate with it.

## Handling exception signals [BACK TO TOC](#table_of_contents)

In general I think it would be a good advice to avoid changing signal handler for these signals. Default signal handler for these signals generates core file. Later, you can use core file to analyze the problem and perhaps find a solution. Overwriting signal handler for one of the exception signals, will cause your program to ignore this signal and an exception that has caused the signal. This is something that you don’t want to do.

In case you still want to handle exception signals, read my [How to handle SIGSEGV, but also generate a core dump](http://www.alexonlinux.com/how-to-handle-sigsegv-but-also-generate-core-dump) article.

## SIGKILL and SIGSTOP [BACK TO TOC](#table_of_contents)

These two signals are special. You cannot change how your program handles these two.

### SIGKILL [BACK TO TOC](#table_of_contents)

SIGKILL, on the contrary to SIGTERM, indicates abnormal termination of the program. You cannot change how your program handles it. It will always terminate your program. However, you can send this signal.

> SIGKILL’s value is 9. This is why*> kill -9 <pid>*> shell command is so effective – it sends SIGKILL signal to the process.

### SIGSTOP [BACK TO TOC](#table_of_contents)

SIGSTOP used when debugging. When you debug your program, operating system sends SIGSTOP to stop your program, for instance in case it reaches a breakpoint. Operating system does not let you change its handler because you may cause your program to be undebuggable.

# Registering signal handler [BACK TO TOC](#table_of_contents)

There are several interfaces that allow you to register your own signal handler.

## *signal()*[BACK TO TOC](#table_of_contents)

This is the oldest one. It accepts two arguments, first signal number (one of those SIG*something*) and second pointer to a signal handler function. Signal handler function returns void and accepts single integer argument that represents a signal number that has been sent. This way you can use the same signal handler function for several different signals.

Here is a short code snippet demonstrating how to use it.

```text
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>

void sig_handler(int signum)
{
    printf("Received signal %d\n", signum);
}

int main()
{
    signal(SIGINT, sig_handler);
    sleep(10); // This is your chance to press CTRL-C
    return 0;
}
```

This nice and small application registers its own SIGINT signal. Try compiling this small program. See what is happening when you run it and press CTRL-C.

### Ignoring signals and restoring original signal handler function [BACK TO TOC](#table_of_contents)

Using*signal()*you can set default signal handler for certain signal to be used. You can also tell the system that you would like to ignore certain signal. To ignore the signal, specify SIG_IGN as a signal handler. To restore default signal handler, specify SIG_DFL as signal handler.

Although this seems to be everything you may need, it is better to avoid using*signal().*There’s a portability problem with this system call. I.e. it behaves differently on different operating systems. There’s a newer system call that does everything*signal()*does and also gives slightly more information about the actual signal, its origin, etc.

## *sigaction()*[BACK TO TOC](#table_of_contents)

*sigaction()*is another system call that manipulates signal handler. It is much more advanced comparing to good old*signal()*. Let us take a look at its declaration

```text
int sigaction(int signum, const struct sigaction *act, struct sigaction *oldact);
```

Its first argument specifies a signal number. Second and third arguments are pointers to structure called*sigaction*. This structure specifies how process should handle given signal.

```text
struct sigaction
{
    void (*sa_handler)(int signum);
    void (*sa_sigaction)(int signum, siginfo_t *siginfo,
        void *uctx);
    sigset_t sa_mask;
    int sa_flags;
    void (*sa_restorer)(void);
};
```

*sa_handler*is a pointer to the signal handler routine. The routine accepts single integer number containing signal number that it handles and returns void – same as signal handler registered by*signal()*. In addition,*sigaction()*let you have more advanced signal handler routine. If needed*sa_sigaction*pointer should point to the advanced signal handler routine. This one receives much more information about the origin of the signal.

To use*sa_sigaction*routine, make sure to set SA_SIGINFO flag in*sa_flags*member of*struct sigaction*. Similarily to*sa_handler*,*sa_sigaction*receives an integer telling it what signal has been triggered. In addition it receives a pointer to structure called*siginfo_t*. It describes the origin of the signal. For instance,*si_pid*member of*siginfo_t*holds the process ID of the process that has sent the signal. There are several other fields that tell you lots of useful information about the signal. You can find all the details on*sigaction*‘s manual page (man sigaction).

Last argument received by*sa_sigaction*handler is a pointer to*ucontext_t*. This type different from architecture to architecture. My advice to you is to ignore this pointer, unless you are writing a new debugger.

One additional advantage of*sigaction()*compared to*signal()*is that it allows you to tell operating system what signals can handle signal you are registering. I.e. it gives you full control over what signals can arrive, while your program handling another signal.

To tell this, you should manipulate*sa_mask*member of the*struct sigaction*. Note that is a*sigset_t*field. sigset_t type represents signal masks. To manipulate signal masks, use one of the following functions:

- int sigemptyset(sigset_t *) – to clear the mask.
- int sigfillset(sigset_t *) – to set all bits in the mask.
- int sigaddset(sigset_t *, int signum) – to set bit that represents certain signal.
- int sigdelset(sigset_t *, int signum) – to clear bit that represents certain signal.
- int sigismember(sigset_t *, int signum) – to check status of certain signal in a mask.

### *sigaction()*in action [BACK TO TOC](#table_of_contents)

To conclude, I would like to show a small program that demonstrates*sigaction()*in use. I would like the program to register signal handler for SIGTERM and then, when it receives the signal, print some information about the origin of the signal.

On the other hand, I will use Python interpretor to send the program a signal.

Here is a program.

```text
#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <unistd.h>

struct sigaction act;

void sighandler(int signum, siginfo_t *info, void *ptr)
{
    printf("Received signal %d\n", signum);
    printf("Signal originates from process %lu\n",
        (unsigned long)info->si_pid);
}

int main()
{
    printf("I am %lu\n", (unsigned long)getpid());

    memset(&act, 0, sizeof(act));

    act.sa_sigaction = sighandler;
    act.sa_flags = SA_SIGINFO;

    sigaction(SIGTERM, &act, NULL);

    // Waiting for CTRL+C...
    sleep(100);

    return 0;
}
```

And this is what happens when we try to run it. First we run the program.

```text
~/works/sigs --> ./a.out
I am 18074
```

While it sleeps I ran Python shell and killed it.

```text
~ --> python
Python 2.5.2 (r252:60911, Jul 31 2008, 17:31:22)
[GCC 4.2.3 (Ubuntu 4.2.3-2ubuntu7)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import os
>>> import signal
>>> print os.getpid()
18075
>>> os.kill(18074, signal.SIGTERM)
>>>
```

Here’s the rest of the output of the program.

```text
~/lab/sigs --> ./a.out
I am 18074
Received signal 15
Signal originates from process 18075
~/lab/sigs -->
```

We can see that it recognized the process that has killed it and printed its process ID.

# Conclusion [BACK TO TOC](#table_of_contents)

I hope you found this article interesting. If you have questions, don’t hesitate to email me to alex@alexonlinux.com.
