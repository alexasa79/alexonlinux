---
title: "Useful Linux Networking Commands"
type: "post"
created_at: "2007-12-23T17:22:30"
original_url: "http://www.alexonlinux.com/useful-linux-networking-commands"
categories: ["System Administrator Articles"]
tags: ["arp", "connection", "ethereal", "ethernet", "ethtool", "icmp", "ifconfig", "linux", "netstat", "network", "packets", "pid", "port", "protocol", "route", "routing"]
---

This article describes most useful Linux networking commands, as simple as it sounds.

The truth is that I am writing this article more for myself. I am rarely doing complex networking configurations. As a result, when I have to configure something, I often forget commands and their syntax. Often it takes hours to find out that the only reason why certain*route*command was not working is because I forgot to add some*netmask*parameter. Hence, this article.

At the moment I only have few commands described. I’ll add stuff at a time. In the meantime, enjoy it and if you have anything to add, please fill free to email me. My email address is alexander.sandler@gmail.com.

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
[ifconfig](#ifconfig)
[Turn on/off network interface](#turn_on/off_network_interface)
[Change interface IP address](#change_interface_ip_address)
[Add second IP address to an interface](#add_second_ip_address_to_an_interface)
[arp](#arp)
[List ARP table](#list_arp_table)
[Add new ARP entry](#add_new_arp_entry)
[Delete ARP entry](#delete_arp_entry)
[route](#route)
[Configure default gateway](#configure_default_gateway)
[Add routing table entry for specified network](#add_routing_table_entry_for_specified_network)
[Using network interface name instead of gateway](#using_network_interface_name_instead_of_gateway)
[Add routing table entry for specified host](#add_routing_table_entry_for_specified_host)
[Removing routing table entries](#removing_routing_table_entries)
[netstat](#netstat)
[List listening sockets and associated port numbers and process PID](#list_listening_sockets_and_associated_port_numbers_and_process_pid)
[Generate statistics about](#generate_statistics_about)
[ethtool](#ethtool)
[What driver is responsible for certain network interface](#what_driver_is_responsible_for_certain_network_interface)
[Figure out interface link speed](#figure_out_interface_link_speed)

# ifconfig [BACK TO TOC](#table_of_contents)

This command is number one command in the alphabet of Linux networking. It configures network interfaces. It features include

- Turning certain network interface on and off.
- Changing interface IP address.
- Changing netmask, MTU and other network parameters of the interface.
- Putting interface into promiscuous mode.

### Turn on/off network interface [BACK TO TOC](#table_of_contents)

Here are few simplest use scenarios.

```text
ifconfig <interface name> down
```

Will turn off specified network interface. Similarly

```text
ifconfig <interface name> up
```

Will turn specified network interface on.

### Change interface IP address [BACK TO TOC](#table_of_contents)

```text
ifconfig <network interface> <ip address>
```

Will turn specified network interface on and give it a IP address.

### Add second IP address to an interface [BACK TO TOC](#table_of_contents)

Another nice thing that you can do with*ifconfig*is specifying additional IP address for one of the interfaces. Think about it for a second. Why single physical interface should be limited to single IP address? What stops us from giving single interface several different IP addresses? And of course*ifconfig*is the tool that let you do the job.

As far as semantics concerned, it seems that*ifconfig*actually creates a new “virtual” interface. Yet, it is simply assigning a new IP address to given network interface. Here’s an example of doing so. Assuming we already have an interface named*eth0*, following command will create interface named*eth0:0*and assign an IP address to it.

```text
ifconfig eth0:0 <ip address>
```

# arp [BACK TO TOC](#table_of_contents)

This command is more advanced, yet still exceptionally useful when configuring networks. It observes and alters so called ARP table. ARP stands for Address Resolution Protocol. ARP table defines relationships between MAC address and IP address. In particular, for every IP address, it defines appropriate MAC address. This used when computer decides to send packet to certain IP address and it has to find MAC address for the IP address. This is when ARP table becomes useful. Computer checks if IP address is in the table and if so picks MAC address from it. If IP address is not in the table, computer uses ARP protocol to find it.*arp*command used to observe and manually alter ARP table entries.

### List ARP table [BACK TO TOC](#table_of_contents)

In its basic form, when invoked, it prints content of the ARP table.

```text
$ arp
Address             HWtype  HWaddress           Flags Mask       Iface
192.168.2.174       ether   00:11:25:9B:7F:74   C                eth0
192.168.2.2         ether   00:17:65:C7:10:45   C                eth0
```

In this example, ARP table on my computer contains two entries. Note the*HWtype*column. It is common understanding that MAC address refers to Ethernet MAC address, but its not necessarily true. There are many L2 protocols and some have their own MAC address structure. For more information about L2 and protocols that belong to this layer see [OSI model on Wikipedia](http://en.wikipedia.org/wiki/OSI_model).

### Add new ARP entry [BACK TO TOC](#table_of_contents)

There are two things that you would probably like to do with ARP table; add and remove entries. This is how you add a new entry.

```text
arp -s <ip address> <hardware address>
```

Again, hardware address is mostly Ethernet MAC address, but it is not always necessarily true.

### Delete ARP entry [BACK TO TOC](#table_of_contents)

```text
arp -d <ip address>
arp -d <hardware address>
```

Both forms of this command delete the specified ARP address. First uses hostname or IP address to identify the ARP entry that we would like to delete. Second uses hardware address to identify appropriate ARP entry.

# route [BACK TO TOC](#table_of_contents)

This is another one of the most useful commands available for you in your toolbox. It manages routes between your computer and other computers and networks.

### Configure default gateway [BACK TO TOC](#table_of_contents)

One of the most important task that you can accomplish with this command is setting default gateway. This is how you do it.

```text
route add default gw <ip address>
```

Here,*ip address*is the address of the default gateway.

### Add routing table entry for specified network [BACK TO TOC](#table_of_contents)

With following command you can add a static route to either a network or a specified host. This is how you do it.

```text
route add -net <network address> netmask <netmask> gw <ip address>
route add -net <network address> netmask <netmask> dev <network interface>
```

These two commands add a new static route to a network. The*network address*should end with 0 e.g 192.168.10.0. Otherwise*route*will return an error. Another way to specify the sub-network is by using the [http://www.alexonlinux.com/short-articles/what-is-cidr-notation](http://www.alexonlinux.com/short-articles/what-is-cidr-notation)[CIDR notation](http://www.alexonlinux.com/short-articles/what-is-cidr-notation). In this case you don’t need to specify the netmask. For example

```text
route add -net 192.168.101.0/24 gw 192.168.102.1
```

Note that in both cases you need a complete network specifications – either using netmask or using [CIDR notation](http://www.alexonlinux.com/short-articles/what-is-cidr-notation).

### Using network interface name instead of gateway [BACK TO TOC](#table_of_contents)

Interesting thing to notice here is that you can specify that packets to given IP address should be transmitted via certain network interface. This works with conjunction with ARP table. For example.

```text
route add -net 192.168.101.0/24 dev eth1
```

### Add routing table entry for specified host [BACK TO TOC](#table_of_contents)

Another kind of routes that you can add with*route*command is route to certain host. This is how you do it.

```text
route add -host <ip address> gw <gateway>
route add -host <ip address> dev <network interface>
```

The principle is the same, although instead of specifying the network you specify a single host. For example.

```text
route add -host 192.168.100.100 gw 192.168.102.5
```

### Removing routing table entries [BACK TO TOC](#table_of_contents)

When you want to remove a route, you can do it by specifying*del*instead of*add.*Here are several examples of commands removing routes.

```text
route del -host 192.168.100.100
route del -net 192.168.101.0/24
route del -net 192.168.101.0 netmask 255.255.255.0
```

Note that when removing a route, there is no need to specify the gateway or the network interface that being used to reach that network or a host. The network or a host identifiers are enough to remove the route.

# netstat [BACK TO TOC](#table_of_contents)

### List listening sockets and associated port numbers and process PID [BACK TO TOC](#table_of_contents)

This is a very powerful information providing tool. It can show lots of network related information. For instance, you would like to know if certain process is listening on a certain port. Easy!

```text
$ netstat -l -p -n
```

Will print list of sockets being listened to accompanied by a process PID and name and port number that being listened to. Note that you need super-user rights to see the list PIDs. In the command above, -l causes*netstat*to list sockets that being listened to – i.e. servers running on the computer and waiting for someone to connect to them from outside. -p causes*netstat*to produce names of the processes and their PID and -n causes*netstat*to use numeric values for port numbers, instead of numbers from /etc/protocols.

### Generate statistics about [BACK TO TOC](#table_of_contents)

Another nice thing that*netstat*can do for you is to generate statistics about traffic your Linux box received and transmitted. The catch here is that statistics printed per protocol. I.e. you can see number of ICMP packets received. You can do it with -i option.

```text
$ netstat -i
```

# ethtool [BACK TO TOC](#table_of_contents)

### What driver is responsible for certain network interface [BACK TO TOC](#table_of_contents)

Have you ever wondered what is the name of the driver powering certain network interface. Answering this question can be a real pain in the butt. Luckily,*ethtool*is here to answer.

```text
$ ethtool -i <interface name>
```

Will tell you what driver is behind given interface, it’s version and firmware version. Note that running*ethtool*requires superuser**privileges.

### Figure out interface link speed [BACK TO TOC](#table_of_contents)

Another handy thing you can do with*ethtool*is to see the speed of the network interface. You can do it with…

```text
$ ethtool <interface name>
```
