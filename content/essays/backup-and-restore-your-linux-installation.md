---
title: "Backup and restore your Linux installation"
date: "2009-04-08T16:18:40"
original_url: "http://www.alexonlinux.com/backup-and-restore-your-linux-installation"
categories: ["Howto", "System Administrator Articles"]
tags: ["backup", "compression", "disk", "hard disk", "ide", "partition", "restore", "scsi"]
---

# Introduction

Backing up Linux installation and restoring it, is perhaps one of the most
fundamental tasks that every system administrator has to deal with.

Here are some important points about backup methods that we will discuss in this
article.

- This article is about backing up from a command line.
Incremental and periodic backups are good for some things. Yet when it comes to
an operating system installation, the whole point of backing up your system is
to save you some time reinstalling it, in case something goes wrong. Hence,
spending couple of hours configuring incremental and periodical backup for your
system just to save you an hour or two reinstalling, in case something goes
wrong, seems rather irrational.
- We will talk about how to save disk space and backup your system even if the
  hard disk that will hold the backup is smaller than hard disk with the
  installation.

If these bullets talk to you, then you’re reading the right article.

# Creating the backup

## What to backup

The actual command that does the backup is quiet simple. However, before backing
up we have to decide what to backup. Here are our options.

- We can backup content of the entire hard disk. We can backup content of the
  Linux installation partition.

What is good for you depends on a structure of a partition table on the hard
disk that contains Linux installation.

One common configuration (and my favorite) is when you have only two partitions
on the hard disk, one for Linux installation and the other for swap. In this
case it is probably wiser to backup your entire hard disk. Indeed, hard disk
space occupied by swap partition will be wasted, but on the other hand restoring
Linux installation from full hard disk backup is much easier. Easier means less
commands to execute to restore the installation and this usually translates into
smaller chances of unsuccessful data restoration.

Another common configuration is when you have several partitions on the hard
disk. In this case, we may want to backup only the partition that contains Linux
installation. The command that does the backup is nearly the same, in this case.
But restoring the data will be more difficult. The chances are that you will not
have any problem whatsoever, so don’t let those couple of extra commands to
scare you.

Bottom line is that it depends on how much information you want to backup. If
your hard disk, in addition to Linux installation, occupied by some data, it is
probably wiser to backup only the Linux partition. In any case I’ll demonstrate
you how to backup both, entire hard disk and the partition.

## Figuring out device file

Second thing you have to figure out is the device file that represents hard disk
or partition that you want to backup. Usually, `mount` command without any
arguments should give you the answer. Have a look:

```text
alex ~ -> mount
/dev/sda1 on / type ext3 (rw,relatime,errors=remount-ro)
tmpfs on /lib/init/rw type tmpfs (rw,nosuid,mode=0755)
/proc on /proc type proc (rw,noexec,nosuid,nodev)
sysfs on /sys type sysfs (rw,noexec,nosuid,nodev)
varrun on /var/run type tmpfs (rw,nosuid,mode=0755)
varlock on /var/lock type tmpfs (rw,noexec,nosuid,nodev,mode=1777)
udev on /dev type tmpfs (rw,mode=0755)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
devpts on /dev/pts type devpts (rw,noexec,nosuid,gid=5,mode=620)
alex ~ ->
```

`mount` command, without any arguments, gives you a list of mounted file-systems
and corresponding device files. For each file-system, it tells you `<device
file> on <directory name> type <fs type>`. Since we are backing up Linux
installation, we are looking for device file that mounted on root directory
(`/`). In my case this is `/dev/sda1`.

Note that usually device files with number and the end represent a single
partition. If you want to know device file of the entire hard disk, strip the
number off. For instance, `/dev/sda1` represents first partition on `/dev/sda`.

In case you’re still not sure what is the correct device file, device files that
start with `/dev/sd` usually stand for SCSI and USB disks. Device files that
start with `/dev/hd` stand for IDE disks. And remember, if you want to backup
Linux partition, use device file whose name ends with a number. For entire hard
disk, use device file whose name ends with a letter.

## Preparations

Before you make actual backup, you have to make sure that the hard disk or a
partition you are backing up is not in use by any programs. This is important
because if your hard disk is in the middle of something while being backed up,
this will inevitably create a data corruption when you restore it. Depending on
what kind of things you do with your hard disk, the corruption can be quiet
serious.

The best way to avoid a corruption is to boot from a Live Linux CD (Knoppix, or
Ubuntu Desktop installation CD). If you know that your hard disk is not heavily
used, you may try to backup live, mounted hard disk. In this case, try to bring
down services that may use the hard disk while its being backed up.

If you’re backing up mounted hard disk or a partition, run `sync` before doing
the backup. This will flush the data from memory buffers to disks (Linux keeps
portions of information from hard disks in memory to speed up hard disk access),
reducing chances of data corruption even further.

Prepare the media that will contain the backup. This may be NFS mount or another
hard disk. Just make sure it is accessible.

## Actual backup

One of the issues with backups is that usually you need as much disk space for
the backup as the size of the hard disk or a partition you’re backing up.
Obviously, you can compress the backup, but normally you still first create
backup and then compress it.

Luckily, there’s a way to backup and compress data on the fly, so that you need
as much free space as a **compressed** backup will occupy. This is how you do
it:

```text
alex ~ -> dd if=/dev/sda | bzip2 -c > /media/sdb/sda.bz2
```

Lets try to understand how it works.

First we use `dd` to read data from /dev/sda. When you read something from a
device file, Linux kernel returns you the content of the actual disk. Same thing
happens if you read from device file that represents a partition. Only this
time, Linux returns you the content of the partition.

Usually we run `dd` with at least two arguments: `if` specifies input file, and
`of` specifies output file. It appears that if skipping one of them, `dd` will
use standard output or standard input instead. Hence `dd` command we use here,
sends contents of the device to standard output.

Output of `dd` command, being sent via pipe to `bzip2` command. `bzip2` is a
compression program. When called with `-c` command line switch, it compresses
whatever it reads from its standard input and sends the result to its standard
output. This is why we send `bzip2`’s output to /media/sdb/sda.bz2 file. This is
the file that will contain the backup once the command finishes.

Note that the file should not be on the disk or partition that we backup. For
that reason, I mounted additional hard disk to /media/sdb directory.

# Restoring from backup

## Preparations

First of all, you will need a Live Linux CD. Knoppix CD or Ubuntu LiveCD should
do the job. It is needed because you need a Linux to restore the backup, but you
cannot use Linux installed on your hard drive because, well, you are going to
erase it with a restored backup.

When restoring the Linux installation from backup, your life will be so much
easier if you use same hard disk and partition. Even if it is a different hard
disk, try replacing old one with the new one and not add it as additional disk.
The reason for this is device files allocation.

When Linux kernel detects several hard disks in your computer, it allocate
device files for them. Device files allocation are /dev/sda for first disk,
/dev/sdb for second disk, etc. When you install Linux on one of them, it will
reference itself by its device file. But here is the catch. Name of the device
file that represent certain hard disk is position dependent. I.e. if you switch
in places first and second disks in your computer, disk that has been
represented by sda until now will be represented by sdb and disk that has been
represented by sdb will be represented by sda. But, internally, Linux
installation on any of them would still refer to itself by old name. As a
result, you probably won’t be able to boot your system.

Bottom line is that you have to make sure that hard disk that you restore your
Linux installation to, being represented by the same device file as before. I.e.
if when you created the backup, your Linux installation was on /dev/sda, make
sure that now, when you restore it, you are restoring to device that will be
represented by /dev/sda when you boot your system.

## Restoring

Boot from your Linux CD. Once there, mount device that has the backup. Figure
out what device file will hold your Linux installation. Remember that if you add
new disks, device files that represent your old disks may shift.

Now to the actual command.

### Restoring entire hard disk

This is actually the simplest case.

First, we start with mounting the disk that contains the backup. In my case this
is /dev/sdb.

```text
knoppix@Microknoppix:~$ mount /media/sdb
```

Next we restore the data.

```text
knoppix@Microknoppix:~$ bzip2 -c -d /media/sdb/sda.bz2 | dd of=/dev/sda
```
First of all, I’ve been using Knoppix CD to restore the system. First command
mounts /dev/sdb, the disk that contains the backup. Second command is the one
that acutually restores the Linux installation.

As with backup command, it doesn’t use extra disk space. It extracts the archive
that contains the installation and writes it to the disk, all on the fly. You
are already familiar with `bzip2`’s `-c` command line switch. It tells `bzip2`
to use standard input or output. `-d` command line switch tells it to decompress
the data. Because of `-c`, it redirect its output to `dd` that picks the data up
and writes it to /dev/sda.

You can boot your restored system right after the above command finishes.

### Restoring single partition

This is a little trickier. Things are very easy when restoring entire hard disk.
You don’t have to care about partition table and boot loader. Your backup
contains everything you need for a happy and working Linux system. All you have
to do is to write the data to the disk and you are done.

When restoring single partition, you have to take care of everything. You have
to create partition table. You have to install boot loader. However, despite
obvious drawbacks, backing up and then restoring single partition has some very
nice advantages compared to entire disk backup.

First, backing up a single partition requires less disk space. Second you have
an option to restore your installation to a larger partition. Lets an example
session that demonstrates both data restoration, partition resizing and boot
loader installation.

Once again, we start with mounting the disk that contains the backup.

```text
knoppix@Microknoppix:~$ mount /media/sdb
```

Demonstrating how to create a partition table is slightly out of scope of this
article, so lets assume that we already have partition table ready. We will
restore the backup to /dev/sda1.

```text
knoppix@Microknoppix:~$ bzip2 -c -d /media/sdb/sda1.bz2 | dd of=/dev/sda1
```

Now the data is where it should be. Lets see how we can resize the partition.

For the sake of this article, I’ve been experimenting with a small VMware based
computer. So I use rather small disks. In this case, partition I’d backed up is
8GB long, but /dev/sda1 is 10GB long. So after we’ve restored the data on the
partition, we have to resize the file-system on it, to utlize entire partition.
Otherwise, it would think that it is still 8GB long.

```text
knoppix@Microknoppix:~$ resize2fs /dev/sda1
resize2fs 1.41.3 (12-Oct-2008)
Please run 'e2fsck -f /dev/sda1' first.
knoppix@Microknoppix:~$ fsck -y -f /dev/sda1
.
.
.
knoppix@Microknoppix:~$ resize2fs /dev/sda1
resize2fs 1.41.3 (12-Oct-2008)
Resizing the filesystem on /dev/sda1 to 2409742 (4k) blocks.
The filesystem on /dev/sda1 is now 2409742 blocks long.
```

As you can see, `resize2fs`, the tool I’ve been using to resize the file-system
has asked me to run `e2fsck` first. `e2fsck` is a tool that checks file-systems
for errors and fixes them – it is similar to `chkdsk` tool on Windows. Its
output was rather long, so I skipped it – errors it has found are a result of me
doing backup of a mounted file-system. Luckily, since I stopped all processes
that may access the disk, when I backed it up, no data was corrupted and errors
found by `e2fsck` were superficial.

Once `fsck` was over, I could do `resize2fs`. Note that without any arguments
`resize2fs` resizes a file-system to a maximum available size – this is exactly
what we wanted.

There’s one thing left to do. That is to install GRUB. In theory, with certain
GRUB configurations you may skip this step and try to boot your restored Linux
installation right away. However, based on my experience, you better do this
step and make sure everything works no matter what configuration you have. So,
here’s what we do.

We start with mounting the newly restored file-system. However, to be able to
mount the partition, we have to create a temporary mount point directory. So,
this is what we do.

```text
knoppix@Microknoppix:~$ mkdir /tmp/sda1
knoppix@Microknoppix:~$ sudo mount /dev/sda1 /tmp/sda1/
```

And now we can install GRUB. This is how we do it.

```text
knoppix@Microknoppix:~$ sudo grub-install --root-directory=/tmp/sda1 /dev/sda
```

This command installs GRUB on /dev/sda. `--root-directory` command line switch
tells `grub-install` to use kernel images and configuration from specified
directory. We want to tell `grub-install` to use kernel images and configuration
from the Linux installation that we’ve just restored. This is why I specified
/tmp/sda1 as root directory.

Finally, we want to unmount the device and reboot. This is what we do:

```text
knoppix@Microknoppix:~$ umount /tmp/sda1
knoppix@Microknoppix:~$ sudo reboot
```
This is it. Now, if everything goes well, your system should boot into restored
Linux installation. Just remember to remove the Live CD from the CD-ROM, before
you boot.
