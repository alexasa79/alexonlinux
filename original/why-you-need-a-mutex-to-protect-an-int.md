---
title: "Why you need a mutex to protect an int"
type: "post"
created_at: "2016-07-05T04:49:56"
original_url: "http://www.alexonlinux.com/why-you-need-a-mutex-to-protect-an-int"
categories: ["Blog", "Programming Articles", "Short articles"]
tags: []
---

This is a follow up on [my previous post](http://www.alexonlinux.com/do-you-need-mutex-to-protect-int) about need to protect access to even simplest variables when working in multi-threaded environment. In this post I would like to explain what’s going on under the hood and why you actually need some protection here.

As in many other computer architectures, in x86 memory access is fairly slow. To give you some perspective, accessing register in CPU takes roughly .5 nano-seconds. Changing value in main memory takes roughly 100 nano-seconds. That’s 200 times slower.

There is number of reasons for that. Perhaps the simplest reason is that typical memory works at much lower frequencies compared to CPU. Typical CPU works at frequencies 2.5-3.5GHz while typical DRAM memory works at 1.333GHz. In addition to that, typical DRAM has to recharge it’s memory cells once in awhile. So typical DRAM doesn’t actually work some of these 1.333GHz.

Another reason for slow memory access is the fact that simple memory access require multiple operations. First of all CPU has to translate virtual address to physical address. Then it has to calculate memory bank that has specific memory cell. Then it has to send a request to read the memory. Somewhere along the way it has to gain access to Front Side Bus – bus that CPUs use to access RAM in x86.

Here’s another reason. CPU is 20-30cm away of memory. It takes roughly 1 nano-second for electrical signal to travel 30cm.

Typical x86 processor tries to solve the problem of slow memory using several different techniques:

1. Memory works in units of 32 and sometimes even 64 bytes called memory lines. I.e. when CPU reads memory cell, it typically reads 32 byte line.
2. Multiple levels of cache make sure that memory access is effective. Typically there are 3 levels of cache named L1, L2 and L3. Sometimes there are four levels. Sometimes there are two. With three levels of cache, L1 usually is local to CPU core, L2 local to physical CPU and L3 shared between several CPUs.
3. Special cache called instruction cache caches program’s instructions.
4. CPU does not immediately writes changes to main memory. Instead CPU tries to delay updating main memory hoping there will be additional changes in same memory line. Changes stored in so called Store Buffer.

Store buffer is the key to what happens with plain integer when multiple threads try to change it at the same time.

x86 maintains so called cache coherency. I.e. when one of the processors modifies one of the memory lines, all other processors become aware of that and modify their own cache. So it is impossible for one processor to modify some memory region, without other processors being aware of this.

> Processors use variation of a protocol called MESI (stands for Modified, Exclusive, Shared, Invalid, denoting four states of a state machine representing state of a memory line from single processor’s point of view) to synchronize ownership of memory lines. All processors listen to Front Side Bus at all times and synchronize their state of the memory line based on what other processors send over FSB.

So, if x86 is cache coherent, when one of the threads updates an integer, all other threads should become aware of that, right? Well, store buffer really messes up with this process. When one CPU updates an integer, the update is not written to main memory. It is stored in store buffer until CPU decides to flush the buffer. Only then variable value gets written to main memory.

When one thread increments the variable, it assumes current value of that variable based on what is in main memory. It may increment the variable once or twice before writing it to main memory. However, value that it writes is value of variable some time ago, plus few increments it performed. At the same time other processors do exactly the same. This causes both of them to miss some of the increments they performed.
