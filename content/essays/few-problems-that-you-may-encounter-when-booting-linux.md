---
title: "Few problems that you may encounter when booting Linux"
date: "2008-07-26T12:08:30"
original_url: "http://www.alexonlinux.com/few-problems-that-you-may-encounter-when-booting-linux"
categories: ["System Administrator Articles"]
tags: ["boot", "disk", "hda", "ide", "init", "initrd", "kernel", "linux", "mkinitrd", "modprobe", "module", "script", "scsi", "sda", "shell", "system"]
---

# Introduction

I thought I’d write a few things that I do with kernel when administrating my
Linux machines. There are plenty of “how to compile your kernel” guides out
there and I won’t write another one. Instead I want to mention few things that
often neglected in those guides.

Let me give you an example. One very common situation is when you are trying to
boot with your newly compiled kernel and it won’t boot. Or something got wrong
and your network card isn’t working anymore. Are you familiar with these
problems? If so, this article is for you.

# Understanding the kernel installation

Lets start with simple understanding of the structure of the Linux kernel. In
this section we’re not going to dig into kernel source tree. Instead we’ll talk
a bit about kernel in its binary form.

## Kernel binary

No matter what Linux distribution you have, Linux kernel installed on your
machine can be divided into two parts. First comes kernel binary. It is a single
file that usually resides in /boot/ directory. The name of the file is usually
`vmlinuz` followed by version number. For instance, vmlinuz-2.6.18.2-34-default.
Some distributions have symbolic link /boot/vmlinuz pointing to real kernel file
(still somewhere in /boot/). This however is not a necessity.

When I am thinking about why kernel file is compressed, I can’t think of a
reasonable explanation. Today disk space is so cheap that we can safely spare
few megabytes for uncompressed version of the kernel. I guess its a backward
compatibility thing. Anyway, face it. Kernel binary file is compressed.

In case you’re wondering if you can decompress it, the answer is no. The problem
is that the compressed portion of the kernel prepended with some uncompressed
data. The size of the uncompressed portion varies. I’ve seen few people managing
to extract uncompressed kernel image out of compressed one, but its fairly
complex process.

Instead, it is a common practice to place an uncompressed version of the kernel
in /boot/ directory. Common practice is to place file named `vmlinux` followed
by the kernel version name and set /boot/vmlinux symbolic link to point to the
uncompressed kernel (usually residing in the same directory).

## Kernel version number

You can have several kernels on one system. Each kernel has a version number. It
might be a little long – version numbers like 2.6.21-8-default are common.
Modern kernels start with 2.6. You can find the later version of kernel at the
moment on [kernel.org](http://www.kernel.org) web-site. 2.6 actually is a major
version of the latest stable kernel. Kernel developers use odd numbers to
indicate development versions of the kernel and even numbers to indicate stable
versions. Hence, 2.6 is stable and 2.5 is a development version.

In case you’re wondering what version of the kernel you have, you can always
check this with `uname -r` command. Like this:

```text
# uname -r
2.6.21-8-default
```

## Kernel modules

Other part of kernel resides in many smaller files under /lib/modules/
directory. These are kernel modules.

Under /lib/modules/ there is a directory per kernel installed on your system.
Each sub-directory named as kernel version. I.e if you’re running kernel
2.6.21-8-default, you’ll find directory named 2.6.21-8-default in /lib/modules/.

Every kernel directory under /lib/modules/ contains several files and
directories. Few of them are important to remember. For instance, `build` is a
symbolic pointing for directory where the kernel has been built (usually
somewhere in /usr/src although it can be anywhere). `kernel` directory contains
several sub-directories that contain actual modules (or directories that contain
modules – anyway no module reside outside of `kernel`). Finally, it contains
several files that start with `modules.*`. These files used by different
utilities such as `modprobe` to locate right modules and resolve dependencies
between them.

# Linux boot process explained

Now I would like to say few words about how Linux boots. The overall boot
process involves several complicated steps, eventually leading to the kernel.

First, kernel being loaded into memory, decompressed and started. One of the
first things kernel does when it starts is loading something called `initrd`.
You may’ve met this name before. I would like to explain what it is.

## Initial ram-disk

In case you didn’t know, you can create a small virtual hard drive in your RAM.
Eventually it does not matter what medium sits beneath the file-system. As long
as you can read and write it, you can create a file-system on it, thus you can
mount it and work with it as if it was a real hard disk.

RAM disk is exactly this – virtual hard disk that resides in the memory. You can
format it and you can mount it.

When you create one, you usually create it empty. However, ram-disks are not
necessarily empty. You can create a ram-disk, write some data to it, save the
ram-disk image into a file and then mount it again. This is exactly what Linux
developers did with initial ram-disk.

Initial ram-disk or shorter `initrd` is a file-system in a file. When system
boots kernel loads it from hard drive into RAM. In case you want to know more
about `initrd`, read my article about internal structure of `initrd`. You can
find it [here]({{< relref "essays/opening-and-modifying-the-initrd.md" >}}).

## Mounting root file-system

This is where most of the fresh kernel compilations fail. Next thing kernel does
after loading `initrd` and running the script is trying to mount the real root
file-system. At this moment it should have a file-system driver, disk driver and
proper device file configuration.

You need a file-system driver because kernel has to understand the structure of
the data on the disk. File-systems usually implemented in one or several kernel
modules – mostly one. One very common exception is ext3 file-system. It’s built
of two modules, ext3.ko and jbd.ko.

Having right disk driver can be more complicated. Generic IDE controller support
is now built into the kernel in vast majority of distributions. Yet SCSI
controllers support may be a bit of a problem. With SCSI disks you need three
modules:

1. scsi_mod.ko – This module contains generic SCSI support.
2. sd_mod.ko – This module contains SCSI disks driver.
3. Kernel module with driver for you SCSI controller.

Missing any of these will cause your system to fail to boot.

Finally, last thing that required for your system to boot are device files. Each
represent a device, as you know. In particular, SCSI disks should have device
files. Each partition on the device should have a device files and most
important device files should point to right locations.

A common problem occurs when you introduce a new SCSI disk into your system.
Deciding how to present a new SCSI disk to your system is up to SCSI controller
and the controller driver. You may find yourself in a situation when before the
change in RAID configuration your root file-system was on /dev/sda, but after
the change it is on /dev/sdb. This often occurs when you have RAID with sparse
LUNs and you fill in the gaps between SCSI LUNs.

Different distributions use different ways to create required device files. In
some Linux distributions, `mkinitrd` itself creates all needed device files. In
others initrd carries `udev` daemon that creates needed files on the go.

In any case, lack of appropriate device files can definitely be a good reason
for the system to stop operating properly.

## init and services

Next thing kernel does after mounting real root file-system is running a program
named init. This program becomes first process that runs in your system. The
executable file usually resides in /sbin/ directory. The way this program works
differs from distribution to distribution. Actually this is one of the major
differences between different distributions.

One thing that remains unchanged is the fact that there’s a manual page for init
that tells how it works. On some systems it runs scripts located in /etc/init.d.
On other systems it will run scripts from /etc/event.d directory. Yet it will
always run some scripts.

### init levels

The scripts divided into several categories. Such division is merely a
compatibility issue – older Unix system had them, so Linux has them too.
Categories don’t have names. Instead they are numbered from 0 to 6. Each
category responsible for certain stage of the session. By session I mean
everything that happens from the moment machine boots, until the moment it’s
being shut down. During this period, machine is always in one of the `init
levels`, meaning it has executed scripts belonging to all categories from 0 up
to the current one.

For instance, normally you work in either init level 3 or level 5. 3 stands for
multi-user environment that supports networking – meaning that at level 3 system
has ran all scripts needed to allow several users to login and do some
networking stuff. Level 5 includes everything that is in level 3 and also
support for X windows. Hence when you work in graphical environment, you are at
level 5 and if you are working with console, you are in level 3. On the
contrary, level 1 stands for single-user no-network environment. Level 6 is a
reboot level, switched to when system shuts down.

Some levels are not in use. Different distributions use level 2 and 4 in
different manner, but most of the time they do nothing meaningful.

### Services

By the way, in nearly all Linux distributions, init scripts start so called
services. Services are programs that run in the background and so some useful
stuff, e.g SSH server usually runs as a service. Each service has a script that
starts and stops it.

One of the things that may go wrong when booting your system is one of the
service scripts (or script that runs service scripts). Perhaps you’ve changed
something yourself. Or one of the system variables that affect one of the
scripts can get wrong and cause the script to misbehave.

### Booting Linux with broken init scripts

Luckily, there’s a simple way to boot the system even if you don’t have a rescue
disk or don’t have an option to stop boot process at level 1, before most of the
init scripts are executed (in RedHat Linux descendants you can press I to stop
boot process on level 1). You can pass init=/bin/bash argument to the kernel,
when booting the system. This will cause the system to execute /bin/bash instead
of init. If you do that, instead of regular boot process you will find youself
in a shell. In this environment you probably won’t have PATH variable set
properly so don’t be surprised when it cannot find `vi` – help it by providing
full path to the executable you would like to run. You can use this limited
shell to fix whatever got wrong with scripts that being involved in the boot
process.

Passing arguments to kernel is easy. You can do this via GRUB boot menu. Usually
you select configuration you would like to boot with from the list and then
press ‘e’ key to edit it. Then you select line starting with kernel, press ‘e’
again to edit it and append init=/bin/bash to the end. Then you just press enter
few times to boot the system.

# Conclusion

There’s always a place for surprise of course. Also, there’re so many different
types of Linux, so it is nearly impossible to describe how to boot a faulty
system. Yet I think I’ve covered most of the important and common stuff. In case
you have problems, suggestions or just things to say about this article, please
fill free to leave a comment or email me at
[alexander.sandler@gmail.com](mailto:alexander.sandler@gmail.com).
