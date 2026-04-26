---
title: "pthread_exit() in C++"
date: "2010-10-09T11:28:03"
original_url: "http://www.alexonlinux.com/pthread_exit-in-c"
categories: ["Blog", "Programming Articles", "Short articles"]
tags: ["C++", "exception", "programming", "pthread", "stack", "unwinding"]
---

Today I ran into an interesting problem that I would like to share. I am working
on multi-threaded code in C++. Here’s what happened.

I started a thread that looks like this:

```cpp
try {
    do_something()
} catch (...) {
    std::cout << "Got unknown exception" << std::endl;
}
```

The `do_something()` routine eventually called `pthread_exit()`.

Once I ran this piece of code, I instantly got an unknown exception
notification. Long story short, here’s what I found out.

When calling `pthread_exit()` in C++, it has to destruct all objects that has
been created on stack. This process called stack unwinding and this is exactly
what happens when you throw an exception. `pthread_exit()` utilizes this
feature of C++ to cleanup before shutting down the thread for good.

To do that `pthread_exit()` throws some obscure exception and catches it right
before ditching the thread. This way it cleans up all objects nicely. On the
other hand, catching … becomes impossible.
