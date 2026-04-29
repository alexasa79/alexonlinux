---
title: "How to handle SIGSEGV, but also generate a core dump"
date: "2009-02-08T00:03:43"
original_url: "http://www.alexonlinux.com/how-to-handle-sigsegv-but-also-generate-core-dump"
categories: ["Blog", "Howto", "Short articles"]
tags: []
---

Recently I ran into this problem. How do you capture `SIGSEGV` with a signal
handler and still generate a core file?

The problem is that once you have your own signal handler for `SIGSEGV`, Linux
will not call default signal handler which generates the core file. So, once you
got `SIGSEGV`, consider all that useful information about about origin of the
exception, lost.

Luckily, there’s a solution. Here’s what I did.

You start with registering a signal handler. Once you get the signal, inside of
the signal handler, set signal handler for the signal to `SIG_DFL`. Then send
yourself same signal, using `kill()` system call. Here’s a short code snippet
that demonstrates this little trick in action.

```c
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
#include <signal.h>
void sighandler(int signum)
{
    printf("Process %d got signal %d\n", getpid(), signum);
    signal(signum, SIG_DFL);
    kill(getpid(), signum);
}
int main()
{
    signal(SIGSEGV, sighandler);
    printf("Process %d waits for someone to send it SIGSEGV\n",
        getpid());
    sleep(1000);
    return 0;
}
```

Note that this code doesn’t actually cause a segmentation fault. To simulate
segmentation fault, I did `kill -11 <pid>` from the command line. This is what
happened.

```text
$ ls
sigs.c
$ gcc sigs.c
$ ./a.out
Process 2149 waits for someone to send it SIGSEGV
Process 2149 got signal 11
Segmentation fault (core dumped)
$ ls
a.out*  core  sigs.c
```

Obviously, without lines 9 and 10 in the code, there would not be core file.

By the way, you can use this technique to handle any core generating exception –
`SIGILL`, `SIGFPE`, etc.
