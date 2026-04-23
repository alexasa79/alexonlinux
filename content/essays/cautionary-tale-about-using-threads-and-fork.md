---
title: "Cautionary tale about using threads and fork()"
date: "2015-05-25T05:34:31"
original_url: "http://www.alexonlinux.com/cautionary-tale-about-using-threads-and-fork"
categories: ["Blog"]
tags: []
---

I ran into one interesting problem. I found a process stuck on mutex. This
sounds like a common deadlock, but it wasn’t that obvious. Thread that was stuck
is the only thread in the process.

I clearly saw from printouts that that mutex was locked in the past by some
other thread that no longer exist. Sometimes you can get into this kind of
problems when you are not handling exceptions properly. The code is written in
C++.

Unfortunately for me, that mutex is always locked using guard variable – guard
variable locks the mutex in constructor and unlocks it in destructor. So any
exception thrown while mutex locked, wouldn’t have caused the problem – when
guard variable goes out of scope, it’s destructor would unlock the lock.

My first hunch was signals. One very common behavior when working with signals
is when you are locking a mutex and then receiving a signal. If signal handler
tries to lock same mutex you end up with deadlock. Fortunately for me the
process was still alive and I was able to check the backtrace. Backtrace showed
that thread is not stuck in the signal handler.

And this is it. I did not have second hunch. It took me a while to realize what
really happened.

This process expected to run in the background. So the most natural thing for it
to do was to `fork()` right after starting. A moment before that it was launching
a thread that handle some asynchronous tasks. When process calls `fork()`, the
child process inherits memory and file descriptors from parent process. One
thing that it is not inheriting is its threads.

In my particular case parent created a thread. Thread started running, locking
the mutex. At this exact moment parent process called `fork()` and child process
was born with that mutex locked.

To conclude, it never stops to amaze me how simple and yet how complicated
multi-threaded programming can be. As a precaution, try not to mix
multi-processed and multi-threaded programs. You may get surprising results.
