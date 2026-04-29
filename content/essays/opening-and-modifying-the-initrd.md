---
title: "Opening and modifying the initrd"
date: "2008-06-01T14:26:33"
original_url: "http://www.alexonlinux.com/opening-and-modifying-the-initrd"
categories: ["Howto", "Programming Articles", "System Administrator Articles"]
tags: ["boot", "init", "initrd", "kernel", "linux", "module", "script"]
---

## Introduction

Ever wondered what’s inside of the `initrd` file? This article tells you how to
look into the `initrd` and even modify it.

## Few words about initrd

Linux uses the `initrd` or `initial ram-disk` during the boot process. Linux
kernel is very modular as you know. While the kernel main file contains only the
most needed stuff, rest of the kernel, drivers included, reside in separate
files – the kernel modules.

It would be impossible to create a single kernel binary image that would suit
all the hardware configurations out there. Instead, kernel supports the
`initrd`. `initrd` is a virtual file-system that contains drivers (kernel
modules) needed to boot the system. For instance, very often a SCSI controllers
drivers reside inside of the `initrd`. Kernel needs a SCSI controller driver to
boot the operating system, but it does not include it, nor it can read it from
hard-disk (you’d need a driver for the hard-disk, right?). And this is when the
`initrd` becomes very handy.

BIOS routines that read the actual kernel from the disk into RAM, do the same
job with `initrd`. When Linux kernel boots, long before trying to mount the real
root file-system, it loads `initrd` into memory and makes it a temporary root
file-system.

See how handy this is. `initrd` itself requires no drivers whatsoever, because
BIOS handles all the work of loading it into memory. On the other hand, it
contains all the drivers Linux needs to boot. And you can easily rebuild it
without changing the kernel.

After loading `initrd` into RAM, the kernel runs a script named `init` that
resides in `initrd`’s root directory. The script contains commands that would
load all required kernel modules. And only after that Linux tries to mount the
real root file-system.

## Few words about history

Content of the `initrd` file and its format has significantly changed over last
couple of years. Something like four years ago, it was a common practice to
create a real RAM-disk with a fixed size, format it with ext2 file-system and
write some data to it.

To look into it, you had to open it up with `gzip` and then mount using
`loopback` device (`mount -o loop`).

Today things are totally different. Kernel configuration option that configures
the size of `initrd` has gone. It wasn’t really convenient because your system
was limited to certain `initrd` size. Instead kernel adapts itself to `initrd`,
no matter what is it’s size.

## Back to the real thing

Like the kernel, `initrd` is compressed to save disk space. Unlike the kernel,
it can be easily decompressed. The tool we’ll use to decompress it is, nothing
fancy, `gzip`. Same good old `gzip` that we use so often.

Now before we begin it is a good idea to create a directory where we’ll work.
After all, internal structure of `initrd` is quiet complex and we don’t want to
mix contents the initrd with contents of your, let’s say, home directory. So, do
`mkdir` and `cd` to create our clean environment. We’ll call this directory A.
To make things even cleaner, place `initrd` file into your newly created
directory and an additional directory in it. This is directory B. In that
directory we will have the contents of the `initrd`. Eventually, you should have
a layout similar to this one.

Let’s start decompressing. Enter directory A and copy `initrd` that you would
like to open into the directory. Then, rename it so that it would have `.gz`
extension. The thing is that `initrd` is `gzip` compressed archive. Since `gzip`
refuses do decompress something that doesn’t have `.gz` extension, we have to
rename the file.

Next we have to decompress the file. `gzip -d <file name>` does the job for us.
Next step is to open up the `cpio` archive. Yes, modern `initrd` is a `cpio`
archive. We can do that with `cpio -i < <file name>`, but before we do that, we
have to enter directory B specifying file name with double dots indicating file
is in the parent directory – the A directory.

```text
sasha@sasha-linux:~/A$ cp /boot/initrd.img-2.6.24-16-generic .
sasha@sasha-linux:~/A$ mv initrd.img-2.6.24-16-generic initrd.img-2.6.24-16-generi
c.gz
sasha@sasha-linux:~/A$ gzip -d initrd.img-2.6.24-16-generic.gz
sasha@sasha-linux:~/A$ ls
B/  initrd.img-2.6.24-16-generic
sasha@sasha-linux:~/A$ cd B/
sasha@sasha-linux:~/A/B$ cpio -i < ../initrd.img-2.6.24-16-generic
42155 blocks
sasha@sasha-linux:~/A/B$ ls -F
bin/  conf/  etc/  init*  lib/  modules/  sbin/  scripts/  usr/  var/
sasha@sasha-linux:~/A/B$
```

In this example you can see me opening default `initial ram-disk` image from my
Ubuntu 8.04 installation. We can see that the `initrd` opened up into a nice
directory tree that resembles your root directory structure. In the heart of the
`initrd` structure is the `init` script that does most of the job of loading
right modules when system boots.

The content of the `init` script is different from distribution to distribution.
The main difference is in approach. In some distributions developers preferred
to keep as many initializations as possible out of the `initrd`. In other
distributions developers didn’t care that much about keeping `initrd` small and
fast. In general both approaches has a place under the sun. First approach based
on the fact that `initrd` is a limited environment, on the contrary to Linux
when its fully loaded. Thus when Linux is fully loaded, you can do more complex
stuff with less effort. Second approach on the other hand, sees in `initrd` an
environment that works faster than “big” Linux, so it uses `initrd`’s fastness
to do some initializations.

Ubuntu’s `initrd` image based upon first approach. It uses a shell program named
`busybox` – the shell environment originally designed for embedded systems and
known for its small memory footprint and good performance. `initrd` in OpenSuSE
10.2 on the other hand uses `bash` shell – same shell as you use regularly. This
is a clear example of the second approach.

Another interesting input to look at, is the fact that `init` script in Ubuntu
8.04 is ~200 lines long, while in OpenSuSE 10.2 it is ~1000 lines long.

## Changing it

Once you have it opened up, you can see things inside of it and even make some
modifications. As I already explained, structure of the `initial ram-disk`
changes from distribution to distribution. However, all distributions share few
common things. For instance, disregarding the distribution and a particular
`initrd` format, `lib/modules/` directory always contains kernel modules that
`initrd` loads at boot time. You may swap one module with another without anyone
even noticing.

Number of modules, their names, etc controlled via `init` script in distribution
dependent form. Therefore, no matter what distribution of Linux you have, `init`
script is the key to understanding how `initrd` works. Apprehend the `init`
script, and you will have full control over your `initrd`, it’s contents and
what it does.

## Packing it back

Assuming you’re done playing around with `initrd` contents and you want to pack
it back. Here is what you do.

First you have to pack `cpio` archive. Remember the B directory we’ve created.
This is where it becomes handy. We want to keep contents of the `initrd` as
clean as possible. The A-B separation allows us to keep the original `initrd`
image out of the way when packing it back.

This is how we do that. First, we should enter the B directory. From there, run
following command:

```text
find | cpio -H newc -o > ../new_initrd_file
```

This will create a new `initrd` file named `new_initrd_file` inside of directory
A.

Next enter directory A and pack the `cpio` archive with `gzip`. Here’s the
command that should do the job.

```text
gzip -9 new_initrd_file
```

This will pack the `initrd` in `new_initrd_file` into `new_initrd_file.gz`
archive. Finally rename the file into whatever you want to call it. Remember
that getting rid of `.gz` extension is a common practice, although not a
necessity.

This is how complete session will look like on Ubuntu:

```text
sasha@sasha-linux:~$ cd A/B/
sasha@sasha-linux:~/A/B$ find | cpio -H newc -o > ../new_initrd_image
42155 blocks
sasha@sasha-linux:~/A/B$ cd ../
sasha@sasha-linux:~/A$ gzip -9 new_initrd_image
sasha@sasha-linux:~/A$ ls
B  initrd.img-2.6.24-16-generic  new_initrd_image.gz
sasha@sasha-linux:~/A$ mv new_initrd_image.gz initrd.img-2.6.24-16-generic-modified
sasha@sasha-linux:~/A$ ls
B  initrd.img-2.6.24-16-generic  initrd.img-2.6.24-16-generic-modified
sasha@sasha-linux:~/A$
```

## Booting with the new initrd

Changing `initrd` is always a risky business. When playing with matters of this
kind, mistakes are common and it is important to stay on the safe side. Adding a
new `GRUB` configuration is not such a big deal, but by all means do so when
trying to boot the brewed five minutes ago `initrd`. You’ll save yourself lots
of time reinstalling distributions and poking around with different rescue
systems to make your system boot again.

Have fun!
