---
title: "MSI-X – the right way to spread interrupt load"
date: "2009-11-18T09:46:11"
original_url: "http://www.alexonlinux.com/msi-x-the-right-way-to-spread-interrupt-load"
categories: ["Blog", "Programming Articles", "System Administrator Articles"]
tags: []
---

When considering ways to spread interrupts from one device among multiple cores,
I can’t not to mention MSI-X. The thing is that MSI-X is actually the right way
to do the job.

Interrupt affinity, which I discussed [here]({{< relref
"essays/why-interrupt-affinity-with-multiple-cores-is-not-such-a-good-thing.md"
>}}) and [here]({{< relref
"essays/smp-affinity-and-proper-interrupt-handling-in-linux.md" >}}), has a
fundamental problem. That is inevitable CPU cache misses. To emphasise this,
think about what happens when your computer receives a packet from the network.
Packet belongs to some connection. With interrupt affinity the packet would land
on core X, while the chances are that previous packet on the same TCP connection
has landed on core Y (X ≠ Y).

Handing the packet would require kernel to load TCP connection object into X’s
cache. But, this is so ineffective. After all, the TCP connection object is
already in Y’s cache. Wouldn’t it be better to handle second packet on core Y as
well?

This is the problem with interrupt affinity. From one point of view we want to
spread interrupts to even the load on cores. From another point of view, doing
simple round robin isn’t enough. The little fella that decides where each
interrupt goes, should be able to look into the packet and depending on what TCP
connection it belongs to, send the interrupt to core that handles all packets
that belong to this connection.

Ideally, NICs should be able to:

1. Look into packets and identify connections.
2. Direct interrupt to core that handles the connection.

Apparently, this functionality already here. Devices that support MSI-X do
exactly this.

## Meet MSI-X

MSI-X is an extension to MSI. MSI replaces good old pin based interrupt delivery
mechanism.

> Each IO-APIC chip (x86 permits up to 5) has 24 legs, each connected to one or
> more devices. When IO-APIC receives an interrupt, it redirects the interrupt
> to one of the local-APICs. Each local-APIC connected to a core that receives
> an interrupt.

MSI provides a kind of protocol for interrupt delivery. Instead of raising
signal on pins, PCI cards send a message over MSI and IO-APIC translates the
message into right interrupt. Theoretically this means that each device can have
number of interrupt vectors. In reality, plain MSI does not support this, but
MSI-X does.

Modern high-end network cards that support MSI-X, implement multiple tx-rx
queues. Each queue tied up to an interrupt vector and each NIC has plenty of
them. I checked Intel’s 82575 chipset. With igb driver compiled properly, it has
up to eight queues, four rx and four tx. Broadcom’s 5709 chipset provides eight
queues (and eight interrupt vectors), each handling both rx and tx.

In kernel 2.6.24, kernel developers introduced new member of struct sk_buff
called queue_mapping. This member tells incoming NIC driver what queue to use
when transmitting the packet.

Before transmitting the packet, kernel decides what queue to use for this packet
(`dev_queue_xmit()` in net/core/dev.c). It uses two techniques to do so. First,
kernel can ask NIC driver to provide a queue number for the packet. This
functionality, however, is optional in NIC drivers and at the moment both Intel
and Broadcom drivers don’t provide it. Otherwise, kernel uses a simple hashing
algorithm that produces 16 bit number from two ip addresses and (in case of TCP
or UDP) two port numbers. All this happens in function named `simple_tx_hash()`
in net/core/dev.c.

When receiving packets, things are even easier because NIC firmware and the
driver decide what queue to use to introduce the packet to the kernel.

Using this simple technique kernel and modern NIC’s can verify that packets that
belong to certain connection land on certain queue. Using interrupt affinity
binding techniques you can bind certain interrupt vector to certain core
(writing to smp_affinity, etc). Thus you can spread interrupts among multiple
cores and yet make sure there are no cache misses.
