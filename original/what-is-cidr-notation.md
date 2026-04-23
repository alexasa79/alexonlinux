---
title: "What is CIDR notation"
type: "post"
created_at: "2008-05-11T23:03:35"
original_url: "http://www.alexonlinux.com/what-is-cidr-notation"
categories: ["Short articles"]
tags: ["network", "short article"]
---

![image](http://www.alexonlinux.com/wp-content/uploads/2008/05/cidr.gif)

I mentioned this several times in my articles and included a link to [wikipedia’s definition of CIDR notation](http://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing). However only now I saw how complex the wiki’s definition is. From the other hand, I guess any formal definition of the subject would be complex and hard to understand. So I took the liberty to describe what CIDR notation is in two words.

First of all, in two words CIDR notation is a way to describe computer networks, or sub-networks to be more precise. I suppose you are familiar with terms sub-network and netmask. As you know, Internet is a network of sub-networks. Netmask is a way to describe your sub-network. I.e. one uses netmask to describe range of IP addresses that are part of the network. If you do logical AND between IP address and the netmask and you end up with a so called base network address. Base network address is the same for all subnet participants.

Although netmask allows you to declare subnets where for instance 192.168.0.100 and 193.168.23.129 are in the same subnet, the common practice is significantly different. Instead of tinkering higher bits of the netmask, people usually change lower bits of the netmask, one by one. As a result, most of the time we can identify a subnet by simply counting number of most significant ones in the netmask. I.e. netmask 255.255.255.0 contains 24 ones, out of 32.

You may count least significant zeros in the netmask. In that case you’ll have to subtract the result from 32.

To write subnet specification in CIDR notation, just write subnet base address followed by / and number of ones in the netmask. For instance, 192.168.0.0 netmask 255.255.255.0 in CIDR will look like this: 192.168.0.0/24. And if the netmask is 255.255.0.0, we will write 192.168.0.0/16. Finally, a more complex example, if netmask is 255.255.252.0, we will write 192.168.0.0/22.
