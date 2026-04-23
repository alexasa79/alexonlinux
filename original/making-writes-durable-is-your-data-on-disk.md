---
title: "Making writes durable – is your data on disk?"
type: "post"
created_at: "2011-09-19T18:26:03"
original_url: "http://www.alexonlinux.com/making-writes-durable-is-your-data-on-disk"
categories: ["Blog", "Programming Articles", "Short articles"]
tags: []
---

[Here is](http://www.evanjones.ca/durable-writes.html) an interesting article written by [Evan Jones](http://www.evanjones.ca/). The article explains how you can be guaranteed when your data is on disk.

In case you’re wondering, when write(), fwrite() or any other library call that writes data to disk reports success you are not guaranteed that the data is actually on the disk. In fact, in Linux, write() reports success when data is in dirty cache. Then, special kernel thread kicks in and makes sure that the data is on disk.

Depending on circumstances, it may take some time until writer kernel thread will finish writing. Anyway, in his post Evan talks about how to make sure that the data is actually stable on disk.
