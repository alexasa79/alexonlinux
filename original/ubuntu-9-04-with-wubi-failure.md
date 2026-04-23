---
title: "Ubuntu 9.04 with Wubi – Failure"
type: "post"
created_at: "2009-05-10T22:03:20"
original_url: "http://www.alexonlinux.com/ubuntu-904-with-wubi-failure"
categories: ["Blog", "Opinion", "Short articles"]
tags: ["bug", "disk", "failure", "israel", "linux", "network", "security", "ubuntu", "wireless", "wubi"]
---

Once every year or so, I get so frustrated with Windows Desktop that I decide to install Linux. I am a big fun of Ubuntu Linux. I use it for many things, this includes a server platform for this web-site. So most natural choice for me was to try Ubuntu 9.04, the latest version. I installed it on my Laptop computer using a program called [Wubi](http://wubi-installer.org/).

Wubi is a program that installs Ubuntu Linux on top of installed Windows. I already had a Windows installation on my laptop, that I didn’t want to destroy. This is why I’ve chosen Wubi. It places root file-system in a file on Windows partition. Because of this feature, you don’t even need a partition to install Ubuntu.

## What got me into this

What got me into Linux desktop frenzy this time, is Vista’s slowness. We all know various virtues of Microsoft’s operating systems. But installing Linux desktop instead… Silly me. It took me just four hours to figure out that I am better with slowness. Four hours I usually don’t have.

I am full of respect to developers of Linux. I work with Linux and develop for it for many years and I think this is a great server platform, unmatched by any other OS. But, Linux desktop is unfortunately isn’t too mature to be a serious match for Windows as a Desktop OS.

Knowing this from my previous attempts to install Linux desktop, I tried a less destructive option out of all. That is, Wubi doesn’t change your existing Windows installation. It install Ubuntu Linux as if it was another Windows program.

## Installing Wubi

Problems started with Wubi itself. I live in Israel and although I use English version of Vista, Wubi installation has decided that I am better with Hebrew. Entire installation procedure was in Hebrew.

Next, despite I explicitly told Wubi that I want English version of Ubuntu, it installed Hebrew version. I checked on Wubi’s web-site and it appeared someone reported this particular bug just few days before. And it already had a solution – developers presented a new revision of Wubi which wasn’t yet publicly available, but solved the problem. The installation interface language remained Hebrew, but at least it installed English version of Ubuntu.

Now in case you wonder why I had to reinstall entire operating system just because of interface language, I’ll explain you. You see, I am not very familiar with Ubuntu’s graphical interface and I didn’t know how to configure wireless network. Hebrew interface made it even more complicated for me, so I decided to get things right form the start and not to begin tackling problems on unfamiliar ground.

On the other hand, because I didn’t have internet access, I could not just install English support it as I would do otherwise.

## Now to Ubuntu

My next task, after installing the Linux itself, was to configure wireless network. The installation program did detect both wired and wireless card. However, the network interfaces configuration program didn’t show the wireless interface – only the wired. Luckily, simply pressing Add solved the problem. New dialog, popped up, asking me what is my SSID.

I am lucky to have some background in wireless networking, otherwise I would not know what SSID is. In case you’re wondering, this is the name of your wireless network. Anyway, it appeared that I’ve forgotten name of my wireless network and I had to use my cell. phone (which luckily supports wi-fi) to find the name. Not to mention I’ve absolutely forgotten that I’ve used WPA2-PSK security for my network. I had to choose it manually too, but before that I had to investigate it with my cell. phone.

I must say that Ubuntu could ship a program that scans for wireless networks, but it just wasn’t there.

On the bright side, once I entered right values for SSID and encryption, it got connected immediately.

## The breaking point

The next thing I planned to do was mounting my Windows partitions. Somehow mounting my C: drive wasn’t that difficult. The desktop was empty. I right clicked on it, created a new directory and then double clicked on it. It opened gnome file explorer. Then I pressed the computer button and here they were, my CD-ROM and C: drive. Clicking on C: drive, created a C: drive icon on the desktop and I could safely delete the directory I created, knowing that I can always open gnome explorer by clicking on C: drive icon.

Now I know that there are several ways of opening gnome explorer, but I just couldn’t find them.

Anyway, note that I have two partitions and gnome explorer only showed me one of them. It appeared to me that something is wrong with D: drive and I should try to mount it. I went to Add/Remove programs and added a program called*Disk Management*. It seemed logical to me that I need some program that manipulates disks, so I searched for*disk*and found that*Disk Management*program. However, once I started it, it reported that I don’t have disks at all.

This was the breaking point. Playing around with Ubuntu was fun, but I had to stop and go back to the world of productivity – where at least sometimes things work.

## Conclusion

Linux is a great operating system and like I mentioned I feel lots of respect to developers of Ubuntu and Linux for the job they are doing. This is especially true because I owe my income to Linux, for the last decade. Linux has given me a profession and I am grateful for that. However it seems that, regrettably, Ubuntu, one of the the undoubtful leaders among Linux distributions, is still too immature as a Desktop solution. Too many things are not obvious. Too many things just don’t work out of the box. Yes I could find a solution for everything, but I am just too busy person to search solutions for everything.
