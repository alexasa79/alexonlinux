---
title: "SlickEdit Macros"
type: "post"
created_at: "2008-01-25T22:14:08"
original_url: "http://www.alexonlinux.com/slickedit-macros"
categories: ["Resources"]
tags: ["editor", "macro", "module", "script", "slick-c", "slickedit"]
---

![SlickEdit Logo](http://www.alexonlinux.com/wp-content/uploads/2008/01/vse.thumbnail.gif)

Many years ago I started working with an editor named Visual SlickEdit. At a time it was the most advanced editor for software development. Despite years have passed, I believe it is still one of the best editors available for programmers.

Among its advantages is exceptionally powerful macro language. Many people don’t know this but SlickEdit is actually a thousands lines of code written with SlickEdit’s macro language and an interpretor that interprets these lines to create this powerful tool. Hence enormous number of features already built into SlickEdit can be extended into endless number of different abilities.

Over the years I collected number of macros for SlickEdit. Some of them I wrote myself, while others I found on the internet. Each I find exceptionally useful and use on a daily basis. I would like to present these macros, so that you’ll be able to enjoy them as well as I do.

Before I begin this review, I’d like to ask you to send me your favorite macros. I’d love to try them and post them here. In particular, I’m very much interested in macros that increase productivity. You can leave a link to your macros in comments here on this page (I’m moderating comments so I can keep the link hidden if you want) or send them to my email – alexander.sandler@gmail.com. Thank you!

# Table of Contents

[Introduction](#introduction)
[Kernel support](#kernel_support)
**[ptrace()](#ptrace())
[Starting to debug](#starting_to_debug)
[Debugger-debuggee synchronization](#debugger-debuggee_synchronization)
[A new debugger was born](#a_new_debugger_was_born)
[The magic behind INT 3](#the_magic_behind_int_3)
[Breakpoints hands on](#breakpoints_hands_on)
[Single steps](#single_steps)
[Conclusion](#conclusion)
[Highlight parens](#highlight_parens)
[Project Toolbar Extension](#project_toolbar_extension)
[OLS – Open Local Symbol](#ols_–_open_local_symbol)
[Open Project File](#open_project_file)
[Comment and Uncomment Selection](#comment_and_uncomment_selection)

# Highlight parens [BACK TO TOC](#table_of_contents)

This pearl is from Slick-C magician, Mr. chrisant. You can often see him posting cool stuff on SlickEdit’s forums. This macro highlights parens. It does a much better job than build into SlickEdit highlighting feature. One image worth a southand words so take a look at the screen-shots below.

You can get it [here](http://www.alexonlinux.com/wp-content/uploads/2008/05/highlightparens.e) and on [SlickEdit’s forum thread](http://community.slickedit.com/index.php?topic=3236.msg13282#msg13282).

Installation is easy. Just load it via Macro->Load Module menu and assign a keyboard shortcut to HighlightParens command.

Remember that pressing the shortcut several times in a row brings different results. Just try it.

![image](http://www.alexonlinux.com/wp-content/uploads/2008/01/vse.gif)

# Project Toolbar Extension [BACK TO TOC](#table_of_contents)

This macro is from Slick-C maestro, Mr. Graeme from SlickEdit’s forum.

It adds a bunch of very useful actions to project’s context menu. After installing the macro, when you right-click somewhere in the project toolbar and go into “More” option, inside you’ll find plenty of additional stuff. This includes:

- You can add a file directly into sub-directory in the project, instead of looking for it with the browser.
- Explore folder containing file or directory you right-clicked on.
- Change current directory to one you right-clicked on.
- Copy into clipboard the name of the directory or a file.

Grab the macro [here](http://www.alexonlinux.com/wp-content/uploads/2008/05/projecttbextra.e). You can also download it from appropriate [thread on SlickEdit’s forum](http://community.slickedit.com/index.php?topic=3459.0). It works on SlickEdit 2008 out of the box. If you want to use it with SlickEdit 2007 and SlickEdit 11, open the file in editor, comment definition of SLICK_V13 and uncomment definition of SLICK_V12 or SLICK_V11 respectively.

Installation is easy as a breathe. Load the macro via Macro->Load Module menu and you’re done.

In case you still have some doubts, check out these screen-shots.

![image](http://www.alexonlinux.com/wp-content/uploads/2008/01/vse.gif)

# OLS – Open Local Symbol [BACK TO TOC](#table_of_contents)

This is perhaps that most advanced macro in my collection. Once triggered, it opens a list of symbols available in currently opened file and allows easily search for certain symbol. The catch is with the way you search. You often remember only a word or two out of symbol name. Conventional search methods would be less effective here because you do not remember the full name. What OLS allows you to do is to find a symbol by only a small fraction of its name. It is exceptionally handy when you are used to work with keyboard. In that case you would press a keyboard shortcut to run the macro, type few letters comprised in the symbol name and hit enter to open the symbol. Alternative is to either few trial and errors with regular search or tediously scanning list of symbols for the right one.

Originally I wrote and maintained this macro, until couple of month ago I posted it in SlickEdit’s forum. Then it was immediately picked by hs2 (sorry, don’t know his real name). He rewrote the macro almost completely, fixing few problems and adding tons of new features. He’s still maintaining the macro.

You can download the latest version of the macro form [http://www.alexonlinux.com/wp-content/uploads/2008/01/hotfix_se1203_ols403tagwin_patch.zip](http://www.alexonlinux.com/wp-content/uploads/2008/01/hotfix_se1203_ols403tagwin_patch.zip)[here](http://www.alexonlinux.com/wp-content/uploads/2008/05/open_local_symbol.e)[http://www.alexonlinux.com/wp-content/uploads/2008/01/hotfix_se1203_ols403tagwin_patch.zip](http://www.alexonlinux.com/wp-content/uploads/2008/01/hotfix_se1203_ols403tagwin_patch.zip). You can also download it from a [thread on SlickEdit’s web-site](http://community.slickedit.com/index.php?topic=2245.0), but it requires registration. This version should work with SlickEdit 2007 and SlickEdit 2008. In case you have problems with the macro, you can leave a comment here or drop a note on [SlickEdit’s forum](http://community.slickedit.com/index.php?topic=2245.0).

Installing the macro is simple. You can use Macro->Load Module menu to load the macro. Next assign a keyboard shortcut to*ols*and you’re done.

And here are some screen-shots.

![image](http://www.alexonlinux.com/wp-content/uploads/2008/01/vse.gif)

# Open Project File [BACK TO TOC](#table_of_contents)

This is pearl in my collection. This time it allows you to search for and open one of the files in currently active project. Search principle used here is similar to one used in OLS macro above. There are few differences though. It interprets last word of the search pattern as a file name, while first words interpreted as path.

If you are friendly with your keyboard, this will definitely increase your productivity.

Again, latest version is [here](http://www.alexonlinux.com/wp-content/uploads/2008/05/open_project_file.e)[http://www.alexonlinux.com/wp-content/uploads/2008/01/open_project_file_v105.zip](http://www.alexonlinux.com/wp-content/uploads/2008/01/open_project_file_v105.zip) or [here](http://community.slickedit.com/index.php?topic=2336.0)– later requires registration. Problems can be reported on this page or on [forum](http://community.slickedit.com/index.php?topic=2336.0).

Installation is via Load Module menu. Again, this version is for SlickEdit 2007 and SlickEdit 2008.

![image](http://www.alexonlinux.com/wp-content/uploads/2008/01/vse.gif)

# Comment and Uncomment Selection [BACK TO TOC](#table_of_contents)

Another macro in my collection is*comment and uncomment selection*. Its origin is unknown. I remember having it for at least several years. It does what it name implies – comments and uncomments selected lines of code. The comments are C++ // type of comments.

You can get it [here](http://www.alexonlinux.com/wp-content/uploads/2008/01/comment_selection.e).

To install it ismply load it via*Macro*,*Load Module*menu. After loading it, assign a keyboard shortcut to*comment-selection*and*uncomment-selection*.
