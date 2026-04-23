---
title: "Python for bash replacement"
type: "post"
created_at: "2010-12-26T18:25:37"
original_url: "http://www.alexonlinux.com/python-for-bash-replacement"
categories: ["Blog", "Opinion", "Programming Articles", "Short articles", "System Administrator Articles"]
tags: ["awk", "bash", "CLI", "ipython", "piping", "programming", "python", "redirections", "sed", "shell"]
---

When I started learning Python, I was looking for a programming language that would replace BASH, AWK and SED. I am a C/C++ programmer and as such I better invest my time into studying C and C++. Instead, every time I needed some complex script I opened up a book on BASH and refreshed my knowledge. And since bumping into boundaries of what BASH can do is relatively easy, I always opened awk/sed book few minutes later.

Actually, this is quiet common. Once in a while I see my colleagues, just like myself, open up a book on BASH. The problem is that because we don’t actively program BASH, the knowledge and experience that we gain from this experience wear out over time. So next time we approach, so we have to repeatedly study BASH stuff over and over again. And again, this is not only BASH I am talking about, but also AWK and SED.

It is utterly broken state of affairs and I wish there was a solution. Unfortunately there is no solution yet. The good thing is that with some effort the solution may arise. I am talking about Python programming language.

Needless to say that Python can do everything that BASH can do. However, it was never designed as shell environment and as such it is hardly convenient.

For instance, running external commands is easy. You should use subprocess module to run the command and there you go, you have both return value and the output. But this is miles away from convenience of simply typing the command and hitting enter.

Another issue is input/output redirections and piping. Regular shell does this with ease. Python obviously does this as well, but not without a hassle of importing the right module and creating the right object, etc.

On the other hand things are not that bad. For instance implementing command line should be somewhat easy in Python because it has native support for completion (which it uses in its own command line interface).

There is a project that makes few steps in the right direction. I am talking about IPython of course. Unfortunately, I doubt that IPython will ever be able to replace BASH. It was never their goal. Even though IPython developers implemented some features that make IPython command line a little down to earth, I am in doubt they will continue moving in this direction. Also, I must say that IPython evolves quiet slowly.

What do you think? Will Python ever be able to replace BASH?
