---
title: "SMP affinity and proper interrupt handling in Linux"
date: "2008-04-15T15:11:29"
original_url: "http://www.alexonlinux.com/smp-affinity-and-proper-interrupt-handling-in-linux"
categories: ["Programming Articles", "System Administrator Articles"]
tags: ["affinity", "apic", "cache", "code", "CPU", "interrupt", "irq", "kernel", "linux", "memory", "napi", "packets", "performance", "smp"]
---

### Introduction

Hardware interrupts has always been expensive. Somehow these small pieces of
software consume so much CPU power and hardware and software engineers has
always been trying to change this state of affairs. Some significant progress
has been made. Still hardware interrupts consume lots of CPU power.

You will rarely see effects of interrupt handling on desktop systems. Take a
look at your /proc/interrupts file. This file enlists all of your hardware
devices and how many interrupts received by each and one of them on each CPU. If
you are on a regular desktop system, you will see that number of interrupts that
your computer handles is relatively small. Even powerful servers handling
millions of packets per second handle only tens of thousands of interrupts per
second. Yet these interrupts consume CPU power and handling them properly
undoubtedly helps to improve system’s performance.

### But really, what can we do about interrupts?

There are many things that can be done. Many Linux distributions ship with
kernel that include modifications that significantly improve the situation.
Technologies, such as NAPI, reduce number of interrupts and interrupt handling
overhead so dramatically, that modern server probably wont be able to sustain a
1Gbps Ethernet link. NAPI is part of kernel for quiet some time. Other things
include interrupt coalescence.

In this article I would like to address one of the most powerful techniques to
optimize interrupt handling.

### SMP affinity

The SMP affinity or processor affinity term has quiet broad meaning and requires
an explanation. The word affinity addresses proximity of a certain task to
certain processor within multi-processor system. I.e. when processor X runs
process Y, they are affine to each other. The processor has parts of process’s
memory in cache, thus constantly moving the process to different processor when
scheduling it, would probably mean less effective scheduling.

As far as interrupts concerned, SMP affinity refers to a question what processor
handles certain interrupt. On the contrary to the processes, binding interrupts
to certain CPU will most likely cause performance degradation and here’s why.
Interrupt handlers are usually very small in size. Interrupt’s memory footprint
is relatively small, thus keeping interrupt on certain CPU will not improve
cache hits. Instead, multiple interrupts will keep one of the cores overloaded
while others remain relatively free. Scheduler has no idea about this state of
affairs. It assumes that our interrupt handling core is as busy as any other
core. As a result, you may face bottle necks as one of the processes or threads
will occasionally work on core that has only 90% of its power available.

Things may be even worse because often core 0 by default handles all interrupts.
On busy systems all interrupts may consume as much as 30% of core’s 0 power.
Because we assume that all cores are equally powerful, we may find ourselves in
a situation where our software system will effectively use only 70% of total CPU
power.

### Who’s responsible

APIC or Advanced Programmable Interrupt Controller has been integral part of all
modern x86 based systems for many years – both SP (single-processor) and MP.
This component is responsible for delivering interrupts. It also decides what
interrupt goes where, in terms of cores.

By default APIC delivers ALL interrupts to core 0.This is the reason why
/proc/interrupts will look like this on vast majority of modern Linux systems:

```text
         CPU0     CPU1     CPU2     CPU3

  0:   123357        0        0        0   IO-APIC-edge  timer

  8:        0        0        0        0   IO-APIC-edge  rtc

 11:        0        0        0        0  IO-APIC-level  acpi

169:        0        0        0        0  IO-APIC-level  uhci_hcd:usb1

177:        0        0        0        0  IO-APIC-level  qla2xxx

185:        0        0        0        0  IO-APIC-level  qla2xxx

193:    12252        0        0        0  IO-APIC-level  ioc0

209:        0        0        0        0  IO-APIC-level  uhci_hcd:usb2

217:      468        0        0        0  IO-APIC-level  eth0

225:      285        0        0        0  IO-APIC-level  eth1

NMI:      120       66       76       45

LOC:   123239   123220   123187   123065

ERR:        0

MIS:        0
```

See anything suspicious? Well, CPU0 handling all hardware interrupts. All of
them. This is the situation that you see on a system with misconfigured
interrupt SMP affinity.

### Simple solution for the problem

Solution for this problem has been around pretty much since the introduction of
the APIC. It has several interrupt delivery and destination modes. Physical and
logical. Fixed and low priority. Etc. The important fact is that it is capable
of delivering interrupts to any of the cores and even do load balancing between
them.

Its configuration is limited to first eight cores. I.e. if you have more than
eight cores, don’t expect any core higher than 7 to receive interrupts.

By default it operates in physical/fixed. This means that it will deliver
certain interrupt to certain core. You already know that by default it is core
0. The thing is that you can easily change core that receives certain interrupt.

For each and every IRQ number in the first column in /proc/interrupts file,
there’s a sub-directory in /proc/irq/. That directory contains a file named
smp_affinity. Using this file you can change what core handles that interrupt.
Reading from this file produces a hexadecimal number which is a bitmask with a
single bit for each core. When certain bit is set, APIC will deliver the
interrupt to corresponding core.

Let’s see an example…

```text
#

# cat /proc/interrupts

         CPU0     CPU1     CPU2     CPU3

  0: 19599546        0        0        0   IO-APIC-edge  timer

  8:        0        0        0        0   IO-APIC-edge  rtc

 11:        0        0        0        0  IO-APIC-level  acpi

169:        0        0        0        0  IO-APIC-level  uhci_hcd:usb1

177:        0        0        0        0  IO-APIC-level  qla2xxx

185:        0        0        0        0  IO-APIC-level  qla2xxx

193:    95337        0        0        0  IO-APIC-level  ioc0

209:        0        0        0        0  IO-APIC-level  uhci_hcd:usb2

217:   100778        0        0        0  IO-APIC-level  eth0

225:    56651        0        0        0  IO-APIC-level  eth1

NMI:      466      393      422      372

LOC: 19600453 19600434 19600401 19600279

ERR:        0

MIS:        0

#

#

# echo "2" > /proc/irq/217/smp_affinity

# cat /proc/interrupts

         CPU0     CPU1     CPU2     CPU3

  0: 19606722        0        0        0   IO-APIC-edge  timer

  8:        0        0        0        0   IO-APIC-edge  rtc

 11:        0        0        0        0  IO-APIC-level  acpi

169:        0        0        0        0  IO-APIC-level  uhci_hcd:usb1

177:        0        0        0        0  IO-APIC-level  qla2xxx

185:        0        0        0        0  IO-APIC-level  qla2xxx

193:    95349        0        0        0  IO-APIC-level  ioc0

209:        0        0        0        0  IO-APIC-level  uhci_hcd:usb2

217:   101027       49        0        0  IO-APIC-level  eth0

225:    56655        0        0        0  IO-APIC-level  eth1

NMI:      466      393      422      372

LOC: 19607629 19607610 19607577 19607455

ERR:        0

MIS:        0

#
```

As we can see, once we enter the magical command, CPU1 begins receiving
interrupts from eth0, instead of CPU0. The echo command that changed the state
of affairs is especially interesting. It is “2” that we’re echoing into the
file. Writing “4” to the file, would cause eth0 interrupt be handled by CPU2,
instead of CPU1. As I already mentioned, it is a bitmask where one bit
correspond to single CPU.

How about writing “3” into the file. In theory, this should cause APIC to divert
interrupts to CPU0 and CPU1. Unfortunately, things are a little more complicated
here. It all depends on whether APIC works in*physical*“destination mode”
and*low priority*“delivery mode”. If it is so, than you most likely would not be
seeing CPU0 handling all interrupts. This is because when kernel configures APIC
to work in*physical/low priority*modes, it automatically tells APIC to load
balance interrupts between first eight cores.

So if on your system CPU0 handles all interrupts by default, this probably means
that APIC configured ambiguously.

### Ultimate solution

First of all, unfortunately there is no choice but to replace the kernel.
Software that configures APIC is part of the kernel and if we want to change
things we have no choice but to fix things in kernel. Things related to APIC are
not configurable, so we have absolutely no choice. The only question is, replace
kernel with what?

I tested this with OpenSuSE 10.2 that comes with kernel 2.6.18. Installing
kernel 2.6.24.3 (the latest at the moment) with OpenSuSE’s default kernel
configuration (/proc/config.gz) fixes the problem. With this kernel, things look
like this, right from the start:

```text
# cat /proc/interrupts

         CPU0     CPU1     CPU2     CPU3

  0:   728895   728796   728624   728895  IO-APIC-edge     timer

  8:        0        0        0        0  IO-APIC-edge     rtc

 11:        0        0        0        0  IO-APIC-fasteoi  acpi

 16:        0        0        0        0  IO-APIC-fasteoi  uhci_hcd:usb1

 19:        0        0        0        0  IO-APIC-fasteoi  uhci_hcd:usb2

 24:    14090    14090    14327    14056  IO-APIC-fasteoi  ioc0

 49:        7        9        7        8  IO-APIC-fasteoi  qla2xxx

 50:        8       12       11       10  IO-APIC-fasteoi  qla2xxx

 77:     2849     2759     2841     2827  IO-APIC-fasteoi  eth0

 78:    25072    25138    24996    24980  IO-APIC-fasteoi  eth1

NMI:        0        0        0        0

LOC:  2915270  2915256  2915228  2915092

ERR:        0
```

Looks good isn’t it? All cores handle interrupts, thus working with maximum
efficiency. Now how about getting this result with just any kernel version? It
appears to be doable.

There’s a kernel configuration option that stands in our way and once removed
you will get similar situation with probably any kernel newer than 2.6.10. The
option is CONFIG_HOTPLUG_CPU. It adds support for hotplugable CPUs. It appears
that having this option off, makes kernel configure APIC properly.

Actually it is quiet understandable. You see, APIC has to be told what
processors should receive interrupts. You need additional piece of code that
tells APIC how to handle processor removals – processor removal is one of the
things that CONFIG_HOTPLUG_CPU allows you to do. I assume that this
functionality was missing from earlier kernel and got inside in 2.6.24.3.

### Conclusion

We saw that we can achieve really nice results by doing some modifications to
kernel configuration. On a very busy system, doing this small configuration
change can boost server’s productivity by large margin.

I hope you will find this information useful and use techniques I described in
this article.
