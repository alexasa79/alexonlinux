---
title: "Call a constructor or allocate an object in-place"
date: "2010-07-04T22:40:10"
original_url: "http://www.alexonlinux.com/call-a-constructor-or-allocate-an-object-in-place-2"
categories: ["Blog", "Howto", "Programming Articles", "Short articles"]
tags: ["C++", "memory management", "new"]
---

Since I joined Dell, my main field of research and work has somewhat changed.
Now I am mostly working with C++ and file-systems. This world is not entirely
new to me, but apparently I have a lot of stuff to learn.

Today I’d like to talk about one nice trick that I learned few days ago.

When working with large software systems, memory management becomes an
imperative. In C, you can easily allocate a large chunk of memory and allocate
structure right on that buffer. This is by far more difficult in C++, because
compiler has to call consturctor.

Apparently, you can, in a way, directly call object’s constructor . I.e. you can
allocate an object, on specified memory region, without actually allocating this
region.

This is how you do it.

```text
char* s = new char[1024];



SomeClass* p = new (s) SomeClass;

```

First new operator just allocates 1024 bytes. This is good old allocation as we
know it. Note the special syntax of the second new operator. It allocates the
new object on memory specified in brackets. Basically, this calls SomeClass’s
constructor using s as storage.

*One thing that I don’t know how to do is how to call destructor on the object –
i.e. how to delete an object in place.*
