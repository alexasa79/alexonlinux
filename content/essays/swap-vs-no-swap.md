---
title: "Swap vs. no swap"
date: "2008-08-21T11:43:25"
original_url: "http://www.alexonlinux.com/swap-vs-no-swap"
categories: ["Opinion", "System Administrator Articles"]
tags: ["cache", "hibernate", "io", "kernel", "leaks", "linux", "memory", "partition", "performance", "RAM", "speed", "swap", "virtual memory"]
---

# Introduction

This short article deals with simple question. How exactly lack of swap
partition affects Linux’s performance. What would happen if you turn the swap
off?

# The obvious

## Memory leaks

The obvious price one would have to pay for turning the swap off is lack of so
called virtual memory. The term virtual memory refers to several different
things really. What I mean is that when a program leaks memory, the memory it
has leaked will remain unused as long as the program still running.

On the contrary, when swap is on, operating system copies memory that is not in
use to the swap partition, by that freeing actual memory. So when one of the
programs has memory leaks, memory that being lost by the program finds its way
to hard drive instead of continuing to take precious memory.

I never heart of a program that claims that it has no memory leaks. Every
program looses memory. It is a matter of time until it will ran out of memory
and then the program will crash. Swap is not an ultimate solution for this
problem because swap space can run out too, yet it significantly prologues live
of the individual processes and the overall system.

## Hibernation

It is being referred to as hibernation and perhaps few other ways. At the bottom
line this is a method to fast turn on and off the computer.

Instead of turning off all services and programs and then initializing them
again, operating system suspends execution of all processes, then writes all
used memory to swap space and then turns off the computer.

When you turn your computer back on, instead of starting a brand new session
from scratch, operating system restores memory from swap and resumes all
programs that were running, without reinitializing them.

> By the way, one of the reasons why recommended swap space size is twice the
> size of the RAM that is in the computer is to let the operating system to
> accommodate all your RAM in swap partition – to allow hibernation of course.

Obviously, when you don’t have swap partition, you cannot do hibernation
anymore.

# The less obvious

## I/O cache

Linux uses all available memory to do I/O cache – that is to save portions of
the hard disk space and to serve it straight from the memory avoiding relatively
long disk access. This is why for instance when you copy several large files
from one place to another several times in a row, second copy takes
significantly fewer time then the first. This is also the reason why, in Linux,
it takes a second to write a megabyte to a floppy disk, a device known for its
slowliness – the data being written to the memory and not to an actual disk.

Also, disks optimized to read and write large chunks of data. Average program on
the contrary reads and writes small chunks of data. To speed up the process,
Linux collects several small read and write requests into bigger thus increasing
disk performance. This however requires memory.

What many people don’t realize is that Linux uses all available memory and
always tries to free even more memory for caching. When it sees a piece of
memory that some program did claim, but doesn’t use very often, it will copy it
to swap partition and use the actual memory for caching. Once the program will
try to do something with this memory piece, Linux will detect this and read the
contents of the memory piece from swap partition back to the real RAM.

> By the way, this is the reason why when you minimize a program and after a
> while restore it, it takes it a few seconds to become fully functional – Linux
> had moved pieces of its memory to swap partition and now this memory has to be
> restored. Reading data from disk takes more time than actual memory access,
> thus the delay you see when you restore the program. You can change how hard
> the operating system tries to free memory for cache by changing value in the
> /proc/sys/vm/swappiness. The value varies between 0 and 100. Value of 100
> means that operating system will not wait much time to move memory to cache.
> Note that whatever swappiness value you have, Linux tries to keep your system
> stable and will move pieces of memory into cache if it thinks it is necessary.

The real issue here is that this mechanism should be very balanced. Linux is
optimized to use all available memory for caching. When it doesn’t have enough
memory, time it takes to access data on disks will rise! Since all programs leak
memory, over the time Linux will have less and less memory for caching and disk
access speed will drop.

# Bottom line

Bottom line is that, without swap:

1. Your system will be less stable.
2. Your system will not be able to hibernate.
3. Disk access speed in your system will be slower compared to a system that has
   swap partition. Moreover, disk access speed will drop in the course of time.

In case you have further questions, please email me to
[alexander.sandler@gmail.com](mailto:alexander.sandler@gmail.com).
