---
title: "Direct IO in Python"
type: "post"
created_at: "2010-01-12T09:50:06"
original_url: "http://www.alexonlinux.com/direct-io-in-python"
categories: ["Programming Articles", "Short articles"]
tags: []
---

Doing file I/O of any kind in Python is really easy. You can start with plain*open()*and friends, working with Python’s file objects. by the way, Python’s*open()*resembles*C*‘s*fopen()*so closely that I can’t stop thinking that*open()*may be based on*fopen()*.

When its not enough, you can always upgrade to*open()*and*close()*from*os*module. Opening man page on*open()*(the system call – open(2)) reveals all those O_something options that you can pass to*os.open()*. But not all of them can be used in Python. For example, if you open a file with*O_DIRECT*and then try to write to it, you will end up with some strange error message.

```text
>>> import os
>>> f = os.open('file', os.O_CREAT | os.O_TRUNC | os.O_DIRECT | os.O_RDWR)
>>> s = ' ' * 1024
>>> os.write(f, s)
Traceback (most recent call last):
  File "", line 1, in
OSError: [Errno 22] Invalid argument
>>>
```

Invalid argument?. What invalid argument? Hey there’s nothing wrong with those arguments…

Reading open(2) man page further reveals that working with*O_DIRECT*requires that all buffers used for I/O should be aligned to 512 byte boundary. But how can you have a memory buffer aligned to 512 bytes in Python?

Apparently, there’s a way. Python comes with a module called*mmap*.*mmap()*is a system call that allows one to map portion of file into memory. All writes to memory mapped file, go directly to file despite it looks like you’re working with plain memory buffer. Same with reads.

There’s one interesting thing about*mmap*. It works with granularity of one memory page – 4kb that is. So every memory mapped buffer is naturally memory aligned to 4kb, thus to 512 byte boundary too. But hey, shouldn’t*mmap*map files?

Well, apparently*mmap*can be used for memory allocations. I.e. specifying -1 as file descriptor does just that – allocates RAM, as much as you tell it. So, this is what we do:

```text
>>> import os
>>> import mmap
>>>
>>> f = os.open('file', os.O_CREAT | os.O_DIRECT | os.O_TRUNC | os.O_RDWR)
>>> m = mmap.mmap(-1, 1024 * 1024)
>>> s = ' ' * 1024 * 1024
>>>
>>> m.write(s)
>>> os.write(f, m)
1048576
>>> os.close(f)
>>>
```

Note that*mmap*memory buffer object behaves like a file. I.e. you can write into the buffer and read from it – like I do in line 8. More on it in [official documentation](http://docs.python.org/library/mmap.html).

Have fun!:-)
