---
title: "6 things that I miss in bash"
type: "post"
created_at: "2009-06-09T20:20:36"
original_url: "http://www.alexonlinux.com/6-things-that-i-miss-in-bash"
categories: ["Blog", "Opinion", "Reviews", "Short articles"]
tags: ["bash", "command", "enhancement", "linux", "scp", "shell", "software"]
---

What is the most frequently used piece of software on your computer? Here’s one program that holds one of the highest place in my list of most frequently used programs. I am talking about…*bash*.

In case you don’t know, this is the program behind large portion of the Linux command line. It is the program that actually makes majority of work turning Linux command line into such a magnificent tool it is.

As for use frequency, on my computer the only program that beats it is perhaps a web browser. I use it more often than mail client, text processor or just any other program.

Now, one thing that entertains me is that there is absolutely no hype around*bash*. I mean, you probably know that next version of Firefox coming tomorrow (I am writing this on June 9th, 2009). But do you know when next version of*bash*is coming? Do you even know what is the version of*bash*that you currently use? Well, you are not alone – I have no clue either:-)

One thing that concerns me is that*bash*almost didn’t change for the last ten years. I mean the only new feature that, to my knowledge, it didn’t support ten years ago is*bash_completion*– that is the advanced version of plain completion that it does to files. I could be wrong about this of course, but one thing is certain. Whatever the changes are, they are unnoticeable.

So, I thought that I’d compile a list of features that I would like to see in the upcoming version of*bash*. Now really, if only one of them would become a reality, I’d chew my pair of orange Crocs (I do have a pair of orange Crocs), put it on video and post it on youtube. Alright, I won’t do that. But it would still be very nice to see these happening.

The list:

### 1 – History sharing

I often open multiple shells. It would be really nice to be able to synchronize history between them. Right now, it seems that*bash*writes history file when it shuts down. If you open another session after history has been saved, you can access commands that you’ve typed in in the previous session. Otherwise, the history between two sessions is completely independent. Not good.

### 2 – Completion of directory and file names based on their usage

I think that 90% of*cd*‘s that I do are all destined to the same directory. Why on earth I see the list of possible destination for*cd*in alphabetical order every time I press TAB?

### 3 – Completion of make targets

I know this has already been implemented. But I am wondering why it isn’t part of*bash_completion*package on Ubuntu. OpenSuSE is no better – it does completion only to some*yast*stuff.

### 4 – Show a browseable and searchable list of files when hitting TAB key twice

I guess you all know that. Single TAB key completes a word if it can make a single match. Double TAB shows a list of choices for completion. In case the list is too long, it builds a long list and pipes it through*more*.

What I would like to see is a browseable and searchable list. One that I can browse with arrow keys. I also would like to be able to enter portion of the file name and in that case*bash*should filter out everything that doesn’t match the criteria I’ve entered.

### 5 – Completion of*scp*, on remote host

I guess it happened to all of us. Copying file to a remote computer with*scp*, is always difficult because you actually have to remember the path on remote computer. Wouldn’t it be great if*bash*could complete remote paths as well?

Now, I know this is very difficult to implement. Basically you have to spawn*ssh*with*ls*command, wait for it to complete and parse the results. Oh and there is a password thing. You gotta take care of password prompt that*ssh*may produce. Have no idea how to solve this issue. I do see a couple of options, but all of them are far from being ideal.

### 6 – Fix typos

This one is simple. As long as I don’t hit the TAB key, no need to fix anything. Once I hit the TAB key, shell should check if the command I’ve entered makes sense and if not try to fix it. Good example of what could make sense are file names.*vi <filename>*probably means that you want to edit a file. If the file does not exist and yet there’s another file with almost identical name, fix it. Same with*cd*. You don’t*cd*into directories that don’t exist. So once shell detects an attempt to do so and the user asks for help (by pressing the TAB key), shell can fix the typo and make the user smile.

This is it. I hope to see any of these happening one day. In the meantime, enjoy the list and by all means leave comments with your ideas of*bash*enhancements.
