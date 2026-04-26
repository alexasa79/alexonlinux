---
title: "Models for multithreaded applications"
date: "2011-04-22T00:00:18"
original_url: "http://www.alexonlinux.com/models-for-multithreaded-applications"
categories: ["Blog", "Programming Articles", "Short articles"]
tags: ["CPU", "performance", "scheduler", "synchronization", "thread"]
---

As you know, I changed a couple of workplaces during my career. Long story
short, one interesting thing that I noticed in different companies is various
models for multi-threaded programs (mostly for large embedded systems).

Lets say we have a multi-threaded program. The program should handle
heterogeneous tasks. On a very basic level, our program probably receives some
data, processes it and produces an output. Question of how to manage threads
usually arises in performance critical applications. Otherwise, it is quiet
simple – we squeeze into single thread as many tasks as possible.

Actual data processing may take several steps. We may want to split it to
several tasks, each handled by thread of its own.

## Thread per task model

When using this model, we allocate single thread per task. Since we want to pass
work from one thread to another, we will need some synchronization mechanism.

I suppose we’ll need some queues to pass things between threads. Also, we may
need muteces or semaphores to synchronize access to queues and other shared
objects.

One obvious weakness of this approach is performance. When moving task objects
from one thread to another we often move them from CPU to CPU. Modern CPUs
heavily deploy caching mechanisms. So keeping objects local to one CPU brings
significant performance boost. By moving task from one CPU to another we heart
caching and cause performance degradation.

Another performance related problem is that while your task object moves from
one thread to another it should undergo at least one context switch. Depending
on overall number of tasks, time it takes to process single task can be greater.
Another cause of context switches is mutual exclusion mechanism that have to
protect the data structure used to communicate objects between threads.

One last significant performance issue that I would like to mention is in the
core of this approach. Each thread is bound by processing power of a single
core. But what if one of the tasks require more processing power. The computer
may have enough processing power. This is especially true with recent multi-core
trend. But when a single thread runs on one core at a time inevitably each
thread processing the request, is a potential bottle-neck.

Advantage of this approach is in its simplicity. You don’t have to develop
significant infrastructure to make it work. All you need is pthreads and a
couple of classes that do the job. All tools that you will use are available out
of the box. Because it is so common, it will be easier to find skilled and
experienced engineers to implement and use with this model.

## Worker threads

In this model, each task split into multiple jobs. Each job being handled by
single thread. There is number of worker threads each taking care of at most
single job at any particular moment. To improve performance, system tries to
handle jobs that belong to same task on the same core. This means that there
might be number of threads per single core.

Unlike thread per task model, this model is much more difficult to implement. It
implies some constraints on the tasks:

1. Engineer designing such system should be able to split tasks into multiple
   jobs. Alternatively, tasks can be very short.
2. Jobs should be more or less equal in size in terms of required processing
   resources.

In addition, this approach requires smart task management. Such system should
implement scheduler that spreads tasks between cores. A serios problem arises
when number of running tasks becomes larger than number of cores in the system.
When it happens, scheduler should start two or more tasks on single core. To do
it wisely, it should be aware of how much processing power required by tasks. It
should manage number of tasks running on particular core and assign new task to
least busy core.

Needless to say that this approach is way more complex than naive thread per
task model. It requires more skilled engineers. Moreover, these engineers should
spend their time developing something that is not directly related to the
matters of the project – that is various infrastructures for the project.

On the other hand, this approach allows engineers to squeeze every bit of
performance out of the machine. This approach will take the hardware to its
limit.

## Other approaches

There are many other approaches of course. Most of them however, are an attempt
to merge between two models I described. For instance, one company started with
thread per task model for their embedded system and quickly ran into performance
problems. So they tried to solve problems by splitting busiest tasks into
multiple threads, basically changing threading model for one particular thread
into worker threads model.

Recently I ran into another model that is somewhat unique. This model implements
so called user-mode threads. Entire program runs in a single thread. Like worker
threads model, in this model tasks split into smaller jobs. However, instead of
letting the operating system to schedule between job execution, this model
implements a user-mode scheduler.

The actual scheduling is made using `setjmp()` and `longjmp()` calls. One obvious
constrain that this model presents is that if thread goes to sleep in operating
system terms it will send entire system to sleep. As a result, the system should
have very tight control over what threads does and in particular how it sleeps.
I.e. threads are not allowed to do regular I/O. Instead they should do I/O in a
centralized way.

For example, thread that wishes to read from a file-descriptor should register
this file-descriptor with scheduler. Scheduler will `select()` or `poll()` on all
registered file-descriptors. Depending on what file-descriptor requires
attention, scheduler will schedule thread that takes care of that
file-descriptor.

In this model you can run only a single instance of scheduler on single
processor. So this model is not entierly optimized for MP machines. If you still
want to run multiple schedulers on single computer then you can either run them
in separate processes or multiple threads of the same process. In both cases
communication between threads that belong to different schedulers is cumbersome.
For instance if run multiple schedulers in multiple threads, you cannot use
mutexes to synchronize between threads that belong to various schedulers because
locking such mutex will send entire system to sleep. Instead you should use some
sort of I/O based IPC.

Despite number of disadvantages that this approach has, there are couple of good
things into it. Synchronizing between threads that belong to same instance of
scheduler is much easier because there is, at most, one thread that runs at any
particular moment. So, if, for instance, you have some simple data structure
that being used by multiple threads there is no need to protect it from
simultaneous access.
