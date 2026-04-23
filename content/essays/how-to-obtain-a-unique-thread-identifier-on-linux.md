---
title: "How to obtain a unique thread identifier on Linux"
date: "2008-03-25T21:35:18"
original_url: "http://www.alexonlinux.com/how-to-obtain-unique-thread-identifier-on-linux"
categories: ["Howto", "Short articles"]
tags: ["call", "getpid", "gettid", "identifier", "linux", "pid", "posix", "pthread", "syscall", "system", "thread", "tid"]
---

![Thread ID]({{< relurl "assets/2008-03-25T213518 How to obtain a unique thread identifier on Linux/threadid.thumbnail-bfb0d59dfd.jpg" >}}) From some reason this topic never got enough attention in libc. POSIX threads library does addresses this issue, however what starts in POSIX library stays in POSIX library. *pthread_self()* and friends will get you an identifier that is unique accross your program, but not accross your system. Although thread is a system object, the system is unaware of the identifier POSIX library allocated for the thread. Thus the thread identifier allocated by the POSIX library does identify your thread within boundaries of your program, yet every-one else knows nothing about this identifier and its meaning.

On the contrary, Linux identifies threads with PID like number called TID. These numbers are system-wide. Tools like *htop* understand them and allow you to obtain information for each and every thread.

In Linux, there’s a system call that will return a TID of calling thread. The name of the system call is *gettid()*. From some reason it is not implemented in *glibc*. Probably it is because it is Linux specific system call. Anyway you have to use *syscall()* to call it. Here’s a sample code that does exactly this.

```c
#include <stdio.h>
#include <linux/unistd.h>
#include <sys/syscall.h>
#include <unistd.h>

pid_t gettid( void )
{
    return syscall( __NR_gettid );
}

int main()
{
    printf( "My TID is %d\n", (int)gettid() );
    return 0;
}
```
