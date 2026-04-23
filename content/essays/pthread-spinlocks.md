---
title: "pthread spinlocks"
date: "2008-11-09T09:23:39"
original_url: "http://www.alexonlinux.com/pthread-spinlocks"
categories: ["Short articles"]
tags: ["mutex", "pthread", "semaphore", "spinlock", "synchronization"]
---

Continuing my [previous essay]({{< relref "essays/do-you-need-a-mutex-to-protect-an-int.md" >}}), I would like to talk
about relatively new feature in glibc and pthreads in particular. I am talking
about spinlocks.

Quiet often you want to protect some simple data structures from simultaneous
access by two or more threads. As in my previous essay, this can even be a
simple integer. Using mutexes and semaphores (critical sections if you wish) to
protect simple integer is an overkill and here’s why.

Modifying or reading value of a single integer requires quiet often as few as
two or three CPU instructions. On the other hand, acquiring semaphore is a huge
operation. It involves at least one system call translated into thousands of CPU
instructions. Same when releasing the semaphore.

Things are a little better with mutexes, but still far from being perfect. Posix
mutexes in Linux implemented using futexes. Futex stands for
Fast-Usermode-muTEX. The idea behind futex is not to do system call when
locking**unlocked**futex. Waiting for locked futex would still require system
call because this is how processes wait for something in Linux. Yet locking
unlocked futex can be done without asking kernel to do things for you.
Therefore, locking futex is, at least in some cases, is very fast.

The problem is that in rest of the cases mutex in Linux is slow as semaphore.
And as with semaphores, spending thousands of CPU cycles just to protect a
single integer is definitely an overkill.

This is exactly the problem spinlocks solve. Spinlock is another synchronization
mechanism. It works in the same manner as mutexes. I.e. only one thread can have
it locked at the same time. However there’s a difference.

When thread tries to lock locked spinlock, it won’t sleep waiting for the
spinlock to get unlocked. It will do busy wait, i.e. spinning in a*while*loop.
This is why its called**spin**lock.

Locking spinlock takes only tens of CPU cycles. One important thing with
spinlocks is to hold it for short period of time. Don’t be surprised when your
program will begin consuming too much CPU, all because one of your threads holds
some spinlock for too long. To avoid this, try to avoid executing big chunks of
code while holding a spinlock. And by all means avoid doing I/O while holding
spinlock.

Now for the easy part.

First, to make things work, you have to include
pthread.h.*pthread_spin_init()*initializes the
spinlock.*pthread_spin_lock()*locks one and*pthread_spin_unlock()*unlocks it.
All as with pthread mutexes. And there are manual pages for each and every one
of them of course.
