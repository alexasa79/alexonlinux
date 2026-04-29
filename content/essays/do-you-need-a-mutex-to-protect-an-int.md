---
title: "Do you need a mutex to protect an int?"
date: "2008-10-23T17:16:23"
original_url: "http://www.alexonlinux.com/do-you-need-mutex-to-protect-int"
categories: ["Short articles"]
tags: ["critical-section", "integer", "multi-threaded", "mutex", "semaphore", "spinlock", "synchronization", "threads"]
---

Recently I ran into few pieces of code here and there that assumed that `int` is
an atomic type. I.e. when you modify value of the variable from two or more
different threads at the same time, all of the changes you’ve made to the value
will remain intact.

But really, can you modify variables of basic types (integers, floats, etc),
from two or more threads, at the same time, without screwing their value?

Until now I’ve been very precautious with questions of this kind. I’ve spend
enormous amount of time solving synchronization problems. So when I have a
variable that being modified or accessed from two or more threads I always put
some mutex or semaphore (spinlock in kernel) around it – no questions asked.

Still, I decided to check things out, perhaps one more time. I wanted to see
what happens with a variable if two or more threads modifying it. So, I’ve
written a short program that demonstrates what happens when you do something
like this.

Here’s the code. See my comments below to understand what it does and how it
does it.

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
        global_int++;
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
        if (pthread_create( &thrs[i], NULL, thread_routine, (void *)(long)i ))
        {
            perror( "pthread_create" );
            procs = i;
            break;
        }
    }
    for (i = 0; i < procs; i++)
        pthread_join( thrs[i], NULL );
    free( thrs );
    printf( "After doing all the math, global_int value is: %d\n", global_int );
    printf( "Expected value is: %d\n", INC_TO * procs );
    return 0;
}
```

You can download the code and a Makefile
[here](http://www.alexonlinux.com/wp-content/uploads/2008/10/atomics.tgz).

The setup is simple. Number of threads is as number of CPUs in your machine
(this includes cores and even hyperthreaded semi-cores). Each thread affined to
certain core with `sched_setaffinity()`. I.e. scheduler configured to run
certain thread on certain core, to make sure that all cores access that
variable. Each thread increases a global integer named `global_int` one million
times.

In the meantime, main thread waits for the worker threads to do their job. Once
they’re done, it prints the value of `global_int`.

And the result is:

```text
Starting 4 threads...
After doing all the math, global_int value is: 1908090
Expected value is: 4000000
```

I guess numbers speak for themselves.

In case you still have some doubts, consider this. When I compile the code with
-O2 compiler option (enabling optimization), the value of the `global_int` is
4000000, as you may have expected. So, it is not really black and white. Also,
things may be different on different computers.

However, the bottom line is that you want to be on the safe side. This code is a
little simple proof that in some cases, simultaneous access to certain basic
variable can cause its value to become ambiguous. So, to be on the safe side,
protect your shared variables, no matter if it is a complex data structure or
simple integers.

If you have further questions, comment here or send me an email to
[alexander.sandler@gmail.com](mailto:alexander.sandler@gmail.com).

PS: I think this issue deserves full scale article. What do you think?
