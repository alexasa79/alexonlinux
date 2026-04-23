---
title: "“Linux Tips and Tricks”, cracking passwords and security"
type: "post"
created_at: "2009-07-15T22:31:18"
original_url: "http://www.alexonlinux.com/linux-tips-and-tricks-cracking-passwords-and-security"
categories: ["Blog"]
tags: ["Carla Schroder", "cracking", "Linux Today", "password", "security", "selinux"]
---

Carla Schroder of Linux Today has posted a nice list of her Linux tips and tricks,[here](http://blog.linuxtoday.com/blog/2009/07/a-collection-of.html).

One tip I could not make work is [Cracking Passwords](http://www.serverwatch.com/tutorials/article.php/3770046). The program simply refused to identify my passwords file. I found that it might be because it doesn’t support this kind of encryption or something like that.

This reminded me of another tool I’ve played with a couple of years ago. It is called Ophcrack and it is available from [http://ophcrack.sourceforge.net/](http://ophcrack.sourceforge.net/).

This beauty cracks Windows passwords. In its most convenient form it is a bootable Linux CD. Once it boots, it automatically detects Windows installation and begins its work. I didn’t believe it, but it took it less then a minute to crack a password on my Windows XP machine. This is despite I use non-dictionary, letters and digits strong password – it is not very strong though.

Linux proponents always mention viruses, trojans and other pieces of nasty software that swarm on Windows machines. This is the most obvious advantage Linux security model has over security model in Windows. But the real power of Linux security is in things like password protection, file access permissions, user management and SELinux. Windows has it too, but in Linux you have it all right on your desktop system or on your VPS and for free.

Back to password cracking, I tried to find a utility that can crack password of Ubuntu 9.04 and I didn’t find one. Then I thought, why on earth someone would need such a utility (for legal reasons I mean). After all, it is so simple to boot Linux into single user mode and run*passwd*.
