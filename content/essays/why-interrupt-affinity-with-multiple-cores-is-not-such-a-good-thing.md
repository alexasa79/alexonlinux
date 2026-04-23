---
title: "Why interrupt affinity with multiple cores is not such a good thing"
date: "2009-09-17T14:44:23"
original_url: "http://www.alexonlinux.com/why-interrupt-affinity-with-multiple-cores-is-not-such-a-good-thing"
categories: ["Blog", "System Administrator Articles"]
tags: ["affinity", "core", "CPU", "interrupt", "motherboard", "network", "performance", "tcp"]
---

One of the features of x86 architecture is ability to spread interrupts evenly
among multiple cores. Benefits of such configuration seems to be obvious.
Interrupts consume CPU time and by spreading them on all cores we avoid
bottle-necks.

I’ve written an [article explaining this mechanism in greater detail]({{< relref "essays/smp-affinity-and-proper-interrupt-handling-in-linux.md" >}}). Yet let me
remind you how it works in two words.

Every x86 motherboard has a chip called IO-APIC. This is a device that controls
interrupt delivery within your system. It knows how many CPUs are in your system
and can direct various interrupts to various CPUs. It uses so called local
APIC-ID as an identifier of the processor.

It has two modes of operation. In one mode it sends interrupts from certain
device to single, predefined core. This mode of operation called fixed/physical
mode. In another mode, it can deliver interrupts from certain device to multiple
cores. The later mode called logical/low priority interrupt delivery mode.

When in logical mode, IO-APIC can deliver interrupts to up to eight cores.
Source of this limitation is the size of the bitmask register that tells what
CPUs should receive the interrupts. The bitmask is only eight bits long.

When considering the round robin-type of interrupt delivery mode (the logical
mode), I cannot stop thinking about how it degrades performance.

You see, having burden of interrupt handling spread among multiple cores may
solve some bottle-necks, but it creates a problem.

Consider network interface card for example. Lets say we have a TCP connection
to some host out there. When packet arrives, the network card issues an
interrupt and IO-APIC directs it to one of the cores. Next, the core handing the
packet should fetch the TCP connection objects from the memory to its cache.

IO-APIC does not guarantee that next packet that belongs to the connection will
be handled by the same core. So, it is likely that two cores will have to work
with TCP connection object. Both of them will have to fetch its content into
their cache. This will cause [cache
coherency](http://en.wikipedia.org/wiki/Cache_coherence) problems (cache
misses). And as you can learn from the [article I’ve written on misaligned
memory accesses](aligned-vs-unaligned-memory-access), accessing memory that is
not in cache can take up to 30 times more time than accessing cached RAM.

Moreover, assuming TCP connection object is properly protected using
synchronization techniques, one of the cores will inevitably have to wait for
the other, adding unnecessary delay to packet processing.

My point is that round-robin style interrupt delivery can be quiet nasty on
performance. It is much better to deliver interrupts from certain device to
given core.

Luckily,*smp_affinity*interface, that I mentioned in my [old
article](smp-affinity-and-proper-interrupt-handling-in-linux), allows you to
bind interrupts from certain device to certain (single) core.

On some computers IO-APIC does not support logical delivery mode. This can be
because of buggy BIOS or too many CPUs. On such computers physical interrupt
delivery mode is the only thing that works, so binding single interrupt to
single core is the only choice and the only thing you can do is switch the core
from one to another.

My point is that round-robin style interrupt delivery can:

1. Malfunction
2. Cause performance degradation.

So, when it still might become useful, you may ask? It depends on what you do
with your computer. Usually, you don’t need round-robin style interrupt
delivery. You only need it if you know that your computer receives lots of
interrupts and you have real-time applications.

In this case, scheduler (which has no idea about interrupts) can schedule thread
that requires lots of CPU time to run on core that serves interrupts. Since
interrupts has higher priority, the thread will receive less CPU time. In case
of real-time application it may result in reduced responsiveness.

Even so, you can still assign all interrupts to one core and use thread affinity
techniques to make sure that your application doesn’t use that core.
