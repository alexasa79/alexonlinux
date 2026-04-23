---
title: "2 reasons why small package repository is better than large"
type: "post"
created_at: "2009-07-26T16:10:19"
original_url: "http://www.alexonlinux.com/2-reasons-why-small-package-repository-is-better-than-large"
categories: ["Blog"]
tags: ["centos", "deb", "package", "rpm", "ubuntu"]
---

I am in the middle of CentOS and Ubuntu comparison frenzy. It started with [an attempt to assert quality of Linux distributions made for busy people](http://www.alexonlinux.com/few-thoughts-about-ubuntu-servers-and-centos). Today I am considering packaging.

When comparing Ubuntu and CentOS packaging systems, first thing that crosses my mind is that, well, size matters. Ubuntu has nearly 70000 packages. CentOS has around 6000.

Obviously, it is very handy to have every possible package just couple of clicks away. Instead of looking for the package, understanding its version system and available architecture. Instead of looking for the vendor’s web-site, seeing all the ads, etc. What you do is just open Synaptic manager, enter the name of the program, or just a couple of keywords describing what you need. Then you do couple of clicks and you’re done.

But when I started using this system I found that there’s something broken in it. There are several things that bother me.

Yes, most of the programs are easy to install, but still, some programs are not in the repository. Others are outdated. Here is one example.

## Non mainstream programs – meet EAGLE

I am a BS.c student. Last semester I was studying Digital Design. I do my home assignments on computer. This includes digital designs I have to submit as part of the home assignments. So, naturally I was looking for a program for designing circuits. After trying a couple of programs I found one that did the job for me. The name of the program is EAGLE**in case you wonder.

However, note how I found it. First I tried three or four circuit design programs from repository. I didn’t like any of them so I googled for it. I found one program that worked for me.

It appeared that the program is in the repository and I already tried it. Yet the repository version is so outdated that I didn’t like it when I looked at it first time. But when I downloaded the latest version from vendor’s web-site, the program was much better. Eventually I used the latest version.

This is a good example of how centralized repository isn’t perfect. Well… Obviously programs like EAGLE are not mainstream programs. Not to mention this is a commercial program. This can explain why repository version is outdated. But from other point of view, being out of the main stream, means that centralized package repository begins to work against you.

I have no doubt that the most popular programs are uptodate in Ubuntu’s repository. Furthermore, something tells me that there are around 5000-6000 such programs – the number of packages in CentOS’s repository. As for the rest of programs in Ubuntu’s repository, it seems that you’d go to vendor’s web-site and download the latest and the greatest version anyway.

## The newest and the hottest – meet Firefox

Another issue is when there is a new version of certain piece of some popular software.

Take Firefox. I’ve been using Firefox 3.5 since it was Firefox 3.1b1. Obviously, when final release version has arrived I was anxious to install it as soon as possible.

Well, you can’t expect new versions of software to land in Ubuntu’s repository instantanoisly. Same happened to Firefox 3.5. As a matter of fact, I think it is still not there – although cannot be absolutely sure about it because I didn’t check.

Luckily, there are some good people on the face of this planet. Someone created a launchpad project with the latest version of Firefox in it. So all I had to do was to install another package source and an appropriate GPG key (or is it PGP?). Obviously it didn’t go as smoothly as I wanted it to go. The launchpad installation didn’t remove older version of Firefox and it was conflicting with the new version. Took me some time to get over it.

When I am thinking about it right now, it seems that it would definitely take less time to install official version, without trying to incorporate Synaptic. I’d probably go on and remove the default version of Firefox because, well, I’d know that nobody will do it for me. Then I’d simply install the official version and add the menu shortcuts manually.

So, here again Synaptics comes as spoiler. It is not its fault really, but Synaptic places the bar very high, perhaps too high, and it is very easy to get disappointed.

So perhaps, many packages can be just too many. What do you think?
