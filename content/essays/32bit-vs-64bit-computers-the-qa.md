---
title: "32bit vs 64bit computers, the QA"
date: "2008-08-26T12:05:00"
original_url: "http://www.alexonlinux.com/32bit-vs-64bit-computers-the-qa"
categories: ["Opinion", "Programming Articles", "System Administrator Articles"]
tags: ["32-bit", "64-bit", "AMD", "CPU", "Intel", "Processor", "RAM"]
---

# Introduction

Many wonder what is the real difference between 64-bit and 32-bit computers. Is paying a little extra for 64-bit support really worth it?

# What 64-bit support mean?

This can mean many things actually. This article dedicated to recent (relatively of course) addition of the 64-bit support in AMD’s and Intel’s micro-processors. Processors supporting 64-bit calculations exists for many years. However these were industry class processors, very expensive and powerful. Couple of year ago, first AMD and then Intel began selling 64-bit processors designed with home user in mind. This historical change is the one I would like to review in this article.

# What the difference between the 32-bit and 64-bit anyway?

Processors with 64-bit support are those that natively support operations with 64-bit long numbers – you need lots of bits to accommodate large numbers. You may be a little confused by the fact that built into both Linux and Windows calculators easily sum a pair of nearly every possible numbers, including a pair of very big numbers. The thing is that 32-bit CPUs only simulate calculations with large numbers.

In 32-bit computer, summing two 64-bit numbers takes 10 and even more times than summing two 32-bit numbers. On the other hand, in 64-bit computers summing two 64-bit numbers takes same period of time as summing two 32-bit numbers.

## General purpose registers

Another, less obvious, difference between the two is that processors with 64-bit support has additional 8 general purpose registers – these are small pieces of memory that are built into processor itself and help it to do its job. Importance of the later addition often overlooked, however this is the change that has brought a truly significant performance boost to 64-bit processors over their 32-bit predecessors.

## What additional registers good for?

Actually the CPU does most of its operations using registers. Registers work as fast as the CPU itself, while RAM is much slower. So in terms of performance, it is better to do as many calculations using registers as possible. The problem is however that having registers is very expensive.

> Intel’s Itanim processors have 128 general purpose registers. Itaniums are an industry class processors and are very expensive.

Additional 8 registers is a significant addition that let the CPU to speed up some of its operations by a large margin.

# So how good 64-bit really is?

With 64-bit extension you get 10% performance boost for free. This number can be different from system to system of course, but I think we can presume this is pretty much the average.

# What about OS and software?

When you have some neat feature in your CPU, you need software uses it. This is why there are 32-bit operating systems and 64-bit operating systems. First knows nothing about 64-bit calculations and additional registers, while the later uses both of them all the time.

Same with regular software.

## Does that mean that paying extra money for 64-bit Windows XP/Vista worth it?

It’s a bit complex. You cannot run 64-bit software on 32-bit operating system. So if you plan running anything that uses 64-bit, you will need 64-bit operating system.

Still for most of the users the answer would be negative. The problem is that most of the software for Windows is 32-bit. 64-bit versions are rarely available. You can run 32-bit software on 64-bit computer and 64-bit operating system, but buying 64-bit operating system is often useless because you may end up using 32-bit software all the time.

**update:** As one of the readers kindly noted, amount of physical RAM that you plan to have in your computer is another consideration that should be taken. 32-bit versions of both Windows XP and Windows Vista limit amount of supported physical RAM to 4GB. In case you need more RAM, you will need 64-bit version of Windows.

## How about Linux?

Linux is completely different story. For most of the software there is a 64-bit version. Even if there is none, you can try to compile it yourself – it is not that complicated. And there is no difference between 64-bit and 32-bit operating system in terms of price. So go ahead, grab yourself a 64-bit Linux and enjoy its improved performance:D
