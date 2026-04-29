---
title: "How less processes its input"
date: "2010-04-28T15:37:37"
original_url: "http://www.alexonlinux.com/how-less-processes-its-input"
categories: ["Articles", "Blog", "Programming Articles", "Short articles"]
tags: ["curses", "error stream", "file descriptor", "input", "input stream", "less", "linux", "more", "output stream", "tty"]
---

Here’s an interesting bit I ran into few days ago. I got curious how is that
`less` (or `more`) can read file contents from standard input and yet it is able
to process input that comes from user. Both of them come from standard input,
yet these are quiet heterogeneous streams of information. So, how can it be?

At first, I thought `less` reads entire input first. This would make standard
input stream free to process key presses from the user. So I decided to check
this out. I created a 1Gb long text file and ran `less` on it. I expected `less`
to take some time to show file contents, but it showed first lines of the file
instantly. Also, it didn’t consume 1Gb of RAM as I expected.

The conclusion is obvious. `less` does not read entire input buffer before
letting user to interact with itself. Then how?

Here’s what `less` does. It separates input file stream from user input stream.
Both inputs initially come via standard input stream, so `less` separates
between them. First it duplicates the standard input stream. This allocates a
new file descriptor. Then it closes old file descriptor, freeing file descriptor
0 for use. Then it opens `/dev/tty`. When opening a file, Linux uses next
available file descriptor. File descriptor used as standard input is 0, so when
`less` opens `/dev/tty` again, file descriptor of the newly opened file has
value 0.

Eventually, it ends up with the new input coming via standard input stream file
descriptor (0), and old input still available via file descriptor that it
duplicated in the beginning. It reads the input file from the duplicated file
descriptor, and uses curses on standard input stream.

You may be wondering what `/dev/tty` is and what it has to do with standard
input streams. This is really fascinating stuff.

As you know, in Linux, everything is a file. So is terminal. Linux uses device
files to represent various system devices. `/dev/tty` is a file that represents
terminal of the current process. When process reads from `/dev/tty` it becomes
its input. When program writes to `/dev/tty` it becomes its standard output or
standard error stream.

So, when `less` reopens `/dev/tty`, it actually recreates standard input. Older
descriptor, one that has been duplicated, can no longer accept new input, but
`less` still can use it to read what it has been written into it already.
