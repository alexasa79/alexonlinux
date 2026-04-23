---
title: "My next programming language"
type: "post"
created_at: "2010-08-22T23:04:43"
original_url: "http://www.alexonlinux.com/my-next-programming-language"
categories: ["Blog", "Opinion", "Programming Articles"]
tags: ["bazaar", "CVS", "evolution", "future", "mercurial", "programming", "programming language", "python", "subversion", "version control system"]
---

This week-end I’ve been playing with various version control systems. Until now, I’ve been doing all my home codings with subversion. I’ve written [about bazaar in the past](bazaar-for-subversion-users-part-1-the-basics), but it seems to me that [bazaar isn’t going anywhere](http://stackoverflow.com/questions/995636/popularity-of-git-mercurial-bazaar-vs-which-to-recommend) and it busts any piece of motivation that I have to continue writing about it.

Version control that I did try is git. This is a very popular version control system and for a good reason. Comparing git and subversion brought me to a conclusion that git is really a very consequence of how things work in the world. Thing about git is that it is a distributed version control while subversion is not. You can make a distributed version of subversion, but it won’t be subversion anymore.

Distributivity is one thing, but there are more. Take the standard trunk/branches/tags layout that you have to create in subversion – version control could do it for you, as git/bazaar/mercurial do. At first, after working with CVS for some time, having an option to have non-standard layout seemed cool for some time. But then it appeared completely useless.

This brings a notion of evolution into version control systems and I bet there’s similar process with programming languages. I think we can already starting drawing a programming language that will replace Python.

Yep, Python isn’t perfect. I thought I’d compile a list of things that shall be different in ought to be programming language that comes after Python.

1. Passing*self*to methods is counter-productive. Using*self*to access members is super counter productive. Yet this is how Python works. Without this, it won’t be Python anymore.
2. Same thing with*global*. Every program has this one global variable that every other class and function use. So, every entity that uses that variable has to declare it with*global*keyword. Utterly counter-productive.
3. Starting every private method and field with __ (double under-score) is ugly. The way it changes method name prepending it with a class name is even uglier. It is a really hackish way to handle this problem. I understand that this is the Python way of doing things, but it feels wrong.
4. Another hackish thing are decorators. Make an option to have static methods, class methods and properties and decorators are gone. No one would need them anymore, and it will be one bit easier to master Python.
5. You name it.

*Disclaimer (can’t get along without one this time:-)): This post may seem like one criticizing Python and it does in some ways, but I doubt these can be fixed in something called Python (unless Guido van Rossum brews it and calls it P**ython 4). In the meantime I love Python and use it on a daily basis.*
