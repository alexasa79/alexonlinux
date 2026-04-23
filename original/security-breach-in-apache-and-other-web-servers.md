---
title: "Security breach in Apache and other web-servers"
type: "post"
created_at: "2009-07-06T23:27:09"
original_url: "http://www.alexonlinux.com/security-breach-in-apache-and-other-web-servers"
categories: ["Blog"]
tags: ["apache", "exploit", "security", "web server"]
---

Apparently, there is a serious breach in Apache’s security. Attacker can launch a denial of service attack on Apache based web-site causing it to stop responding.

It seems to be at least a couple of years old, yet it has no fix. The idea behind the exploit is very simple. Exploit script opens a connection, but instead of requesting the data, receiving the data and disconnecting, it sends HTTP headers by small portions. It sends the HTTP request portion by portion, once every period of time. The period of time can vary from one-two seconds, to couple of minutes. Obviously, this prolongs the connection to the server.

It is known that Apache supports limited number of concurrent users. Therefore, opening a significant number of such slow connections should bring the web-server to a state where it cannot serve new clients anymore.

The problem lies in Apache’s architecture. It limits the number of open connections by assigning a process or a thread to take care of every client, even if the client sends one packet per minute.

Solving a problem of this kind requires serious redesign on Apache’s side and unfortunately takes time. Therefore there is no bullet-proof solution for this problem yet.

You can find more details here:[http://lwn.net/Articles/338407/](http://lwn.net/Articles/338407/)

However, Apache
