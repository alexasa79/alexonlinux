---
title: "Few thoughts about Ubuntu servers and CentOS"
type: "post"
created_at: "2009-07-20T20:35:22"
original_url: "http://www.alexonlinux.com/few-thoughts-about-ubuntu-servers-and-centos"
categories: ["Blog"]
tags: ["centos", "distribution", "ubuntu", "vnc", "xinet.d"]
---

This Saturday I tried to configure VNC server to start in the background automatically at boot. You know, in Ubuntu you normally run VNC server when you need it and stop it when you don’t need it anymore.

I did it on RHES 4 once and it worked like a charm. Well… On Ubuntu it didn’t work like a charm. It took me a couple of hours to make it work – I found a guide that tied VNC server to xinet.d which supposed to start VNC server once someone accesses port 5900.

This isn’t a good setup, by the way. The problem is that there is a serious difference between, lets say, telnet server and VNC server. Once you start telnet server, it is ready to accept connections almost immediately. VNC server on the other hand, starts gnome (or KDE) and it takes time. So usually you’d get gray screen upon connecting and have to wait.

Anyway, this setup was the most straightforward thing I found so I gave it a try. It worked. One thing that left for me to do was rebooting the machine and making sure that VNC server works after boot. But it didn’t boot.

I have a root file-system and all the data on md based raid 1 (that is mirror). Eventually I couldn’t make it work, but I managed to mount it once and take all the valuable data from the disk. It took another two hours though. What a waste of time.

Then [I saw an article on lwn.net called “Why people don’t test development distributions”](http://lwn.net/Articles/340121/). Honestly it amused me, but it wasn’t an amusement of a good kind.

I am full time software engineer. I am also an active student for BS.c in Computer Science (after ten years of professional programming it’s time for me to learn programming, isn’t it?:-). I run this web-site and I have a couple of other pet projects that I work on at home. Finally, I have a family. So, why I am not testing development distributions?

Sorry, but I am not a kind of guy who would test development distributions. I wish I was such a person, seriously. I’d love to spend days poking around various programs and trying new stuff. But I am 30, not 14. I have more responsibilities and less time.

I’d just like to have a distribution that has passed all the testing and now fully operational. I’d like to have a distribution that works. Can I get one such distributions?

Here is the funny part. If I want to have such a distribution, I’d have to buy it because it is either RHES (either workstation or server version) or SLES (again, either workstation or server version) – both cost money.

I thought of Ubuntu as such a distribution, but more and more I am getting disappointed with it. Consider the issue with VNC server and inability to boot the server. I would expect the distribution I am looking for to be thought through and tested enough for these two problems not to appear. Yet they appeared.

I think I found a distribution that seems to be a good alternative to Ubuntu server. I am talking about CentOS. I am definitely going to give it a try today evening – it will replace Ubuntu server that wouldn’t boot anymore.

Yet although CentOS seems to be a good answer to what I am looking for, I wish there was a as stable as CentOS and yet one that has shorter release cycle.
