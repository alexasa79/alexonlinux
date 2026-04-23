---
title: "Reverse SSH tunnel or connecting to computer behind NAT router"
type: "post"
created_at: "2008-05-13T14:18:13"
original_url: "http://www.alexonlinux.com/reverse-ssh-tunnel-or-connecting-to-computer-behind-nat-router"
categories: ["Howto", "System Administrator Articles"]
tags: ["connection", "firewall", "linux", "NAT", "office computers", "router", "server server", "session", "ssh", "tunnel", "vpn"]
---

### Introduction

Few days ago I encountered a problem. How do you connect to a computer behind NAT router? Any NAT router is also a firewall. Sometimes you do have access to firewall configuration and can set up port forwarding. Yet often it is complicated and even impossible. Common situation is when you want to connect to a computer in the office from home. Companies usually hide office computers behind NAT routers and firewalls. Hence you cannot connect to office computer as is.

This is exactly the problem I had to overcome. After googling for couple of minutes I found a solution called reverse SSH tunnel. Yet I could not find a guide that explains how to make it work from A to Z. So I decided to write one.

### Understanding the setup

In our basic setup we have a*Home Computer*. It runs Linux and can freely access the Internet.*Office Computer*is the Linux machine behind*NAT router*. We want to connect to*Office Computer*but can’t because of the*NAT router*.*Server*is additional Linux machine. It has to be accessible from both home and office computers via SSH.

![image](http://www.alexonlinux.com/wp-content/uploads/2008/05/reverse_tunnel_diagram.jpg)

### Preparations

First, we have to make sure that SSH server on*Server*has*GatewayPorts*option turned on. You most likely have openssh SSH server. If so, open /etc/ssh/sshd_config and make sure it has following line.

```text
GatewayPorts yes
```

If it’s missing, add it and restart SSH service.

Now this is important. Using method described here you can connect to different ports on*Office Computer*. However, if you want to connect to it via SSH you have to make sure that*GatewayPorts*is on on the*Office Computer*as well.

Also, to connect you need access to the*Office Computer*. I.e. you either have to ask someone to execute commands on*Office Computer*for you, or you have to run them yourself in advance.

### Connecting

This is the easy part.

Assuming you want to connect to port X on*Office Computer*, do the following.

On*Office Computer*do the following:

```text
ssh -R 6333:localhost:X user_on_server@server
```

*Server*will require regular SSH credentials (either certificate or password) and will open regular SSH session for you. This is the tunnel session. Keep it open as long as you want to stay connected to the*Office Computer*.

On*Home Computer*connect to port 6333 on*Server*as if it was port X on*Office Computer*. In case you want to connect to SSH port on*Office Computer*, set X to 22 (SSH port) in step 1 and do the following:

```text
ssh user_on_office_computer@server -p 6333
```

Again, you may be asked to identify yourself. Do it as you were connecting to*Office Computer*directly.

### Avoiding session expiration

As I mentioned in*Preparations*section of this guide, you can do step 1 in advance, before going home. Alternatively, you can ask someone to do the command for you. In case you prefer to do it yourself, you may want to make sure that tunnel connection you established won’t expire.

There are three options in /etc/ssh/sshd_config that control SSH session expiration. Once in a while SSH server sends keep-alive messages to connected clients. Temporary connectivity problem can cause it to disconnect certain SSH session, despite this is only a very temporary problem. Depending on the configuration of you SSH server, you may want to prevent these keep-alive messages. On the contrary you may want to increase interval between them or change number of lost keep-alive messages that indicate to SSH server that a connection to a client has been lost.

*TCPKeepAlive*configuration option enables or disables keep-alive messages. The default is yes (i.e. send keep-alives) and it is a good practice to keep it this way.

*ClientAliveInterval*specifies number of seconds between every keep-alive message. Depending on quality of connection between*Office Computer*and the*Server*we may want to set it to, let’s say 10.

*ClientAliveCountMax*controls number of lost keep-alive messages that cause SSH server to pull the plug. We want it relatively big, but not too big. With*ClientAliveInterval*equals 10, its a good idea to loose the connection after keep-alive messages fail for lets say 5 minutes – 300 seconds. This means we can make*ClientAliveCountMax*equals 30.
