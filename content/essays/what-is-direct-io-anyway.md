---
title: "What is direct I/O anyway?"
date: "2010-02-15T12:03:57"
original_url: "http://www.alexonlinux.com/what-is-direct-io-anyway"
categories: ["Blog"]
tags: ["cache", "direct", "direct I/O", "io", "kernel", "linux", "page cache", "performance"]
---

Few days ago I’ve written [an essay explaining how to do a direct I/O in Python]({{< relref "essays/direct-io-in-python.md" >}}). But then I thought that it might be a good idea to explain what direct I/O is. So, here we go.

As surprising as it is, when you write some information to the disk, it doesn’t get there immediately. In Linux especially, the kernel tries to cache write requests in memory as much as it can. This means that in addition to writing the data to the disk, kernel keeps it in memory. Consecutive read request to the same place on the disk will be much faster because there’s no need to read the information from slow disk – it is already in memory. On the other hand, the information goes to the hard-disk only after some period of time (short though) or when the system runs out of memory. In the meantime, Linux reports that data has been written, despite it is not yet on the disk.

This causes several interesting phenomena that you may have noticed. For example Linux machines with little memory, even though not all memory is in use, do use disk much more than machines with more memory. There are several reasons for it. One of them is because kernel doesn’t have enough memory to cache information from the disks and as a result read requests rarely hit the cache and more often go to the disk.

> Want to see exactly how Linux reports successful write requests before data actually lands on the disk? Try writing some information to floppy disk and see how fast it is in Linux. The truth is that it’s still frustratingly slow. Linux just makes it look like a fast device.

Sheer thought that Linux doesn’t write the data to the disk, despite it says it did, may be pretty scary. But it shouldn’t really. First of all, if its not very busy it does write the data to the disk as soon as possible. Second, Linux does excellent job avoiding various problems and even if something bad happens, it is pretty good at recovering lost data. The way Linux works is excellent for 99% of users. This approach improves performance in various ways and makes the system more healthy and stable.

However, some folks out there are not happy with this situation. Some software systems cannot work the way Linux works. One of the examples are so called clustered file-systems – file-systems that are spread among multiple servers for redundancy purposes. Such systems need a way to know that data has been written to the disk for real, not just being cached. Also, such systems want to make sure that reads hit disk and not OS cache.

This is where direct I/O becomes handy. Direct I/O is a way to avoid entire caching layer in the kernel and send the I/O directly to the disk. Overall, this makes I/O slower and does not let Linux do various optimizations that it usually does. Also, it introduces some constraints on memory buffer that being used for the I/O. Yet sometimes it is inevitable.

Want to try it yourself?*dd*, I/O Swiss army knife, has an option called*direct*. It tells*dd*to do direct I/O instead of regular I/O. Another option for doing direct I/O is writing your own program that opens files with O_DIRECT flag (see*open*(2) for details).

*Update Feb. 12: Thanks to Ivan for noting the difference between synchronous I/O and direct I/O. I updated the essay to reflect the difference.
*
