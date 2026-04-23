---
title: "A new kind of virtualization"
date: "2009-05-06T12:39:32"
original_url: "http://www.alexonlinux.com/a-new-kind-of-virtualization"
categories: ["Blog", "Programming Articles"]
tags: ["CPU", "performance", "Processor", "programming", "smp", "threads", "virtualization"]
---

There are plenty of virtualization technologies. There are organizations like
VMware, VirtualBox and XEN, whose virtualization allows one to run several
virtual computers using one physical computer.

I worked at a company called ScaleMP. ScaleMP’s technology, vSMP, turns multiple
physical computers into one large computer.

Today I was looking for something different. I was looking for technology that
turns multi-core physical computer into a virtual computer with a single core,
whose power is a combined power of all physical CPUs. I.e. take two CPUs with
four cores each, each doing X flops. Turn them into single CPU with single core
that does 8X flops.

In case you wonder why on earth someone would need such program, here’s what I
was thinking about. Imagine you have a single threaded program. Lets also assume
that the program is difficult to change (or you only have its binary).

Single threaded implies scalability problem. This is because the only thing you
can do to improve its performance is to make the CPU, it runs on, to run faster.
But modern CPUs has reached their capability in terms of single core processing
power. To make CPUs faster, processor vendors add more cores – split CPU in two,
four, eight, etc. Yet they cannot make single core to be significantly faster.
Hence we’re stuck.

Such super CPU virtualization technology could solve the problem, but it appears
that such technology does not exist. There’s not a single firm that does
anything that even closely resembles something like this.

Then, I thought that actually such company cannot exist. Its a combination of
technological innovation and cost of development that simply cannot coexist.

Think about it. Technology behind virtualized CPU would have to split single
stream of execution into several streams. But this is exactly what modern CPUs
do already. Processor that utilizes*branch prediction*, try to predict most
probable path of execution of a thread and execute several chunks of code
simultaneously.

In case you’re wondering if a processor in your laptop computer does branch
prediction, the answer is probably yes.

Because CPUs already use branch prediction and perhaps other technologies that
speed up executable code processing, making our super CPU do the job even faster
would be a very difficult task. Task as difficult that it would probably require
some best minds in the world to join up. And best minds in the cost a lot of
money.

On the other hand, market size for such product is relatively small. There are
not many programs out there that cannot be optimized to run on SMP. So income
from such product wouldn’t be so great. Eventually, such company will bankrupt.

Unless, of course, there are other possible uses for such technology.
