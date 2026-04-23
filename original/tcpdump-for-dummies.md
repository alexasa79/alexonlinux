---
title: "tcpdump for Dummies"
type: "post"
created_at: "2008-05-18T16:29:11"
original_url: "http://www.alexonlinux.com/tcpdump-for-dummies"
categories: ["System Administrator Articles"]
tags: ["arp", "connection", "debug", "destination", "ethereal", "ethernet", "expression", "ftp", "http", "icmp", "network", "packets", "port", "protocol", "source", "ssh", "synchronization", "tcp", "tcpdump", "telnet", "unix", "wireshark"]
---

# Table of contents

[Introduction to the series](#introduction_to_the_series)
[Introduction to the article](#introduction_to_the_article)
[Way of working with Bazaar](#way_of_working_with_bazaar)
[Demo setup description](#demo_setup_description)
[Directory and user configuration](#directory_and_user_configuration)
[The basics](#the_basics)
[Creating a project](#creating_a_project)
[Checking-out the project](#checking-out_the_project)
[Adding files to the project](#adding_files_to_the_project)
[Committing files](#committing_files)
[Few words about revision numbers in Bazaar](#few_words_about_revision_numbers_in_bazaar)
[Local commits or offline commits](#local_commits_or_offline_commits)
[Committing local commits to remote branch](#committing_local_commits_to_remote_branch)
[Multi-user environment](#multi-user_environment)
[Making modifications to files and viewing differences](#making_modifications_to_files_and_viewing_differences)
[Committing non-up-to-date file](#committing_non-up-to-date_file)
[Merging with the latest version of the file](#merging_with_the_latest_version_of_the_file)
[Introduction](#introduction)
[What reference counting needed for?](#what_reference_counting_needed_for?)
[This is how we will use atomic variables to count references to objects](#this_is_how_we_will_use_atomic_variables_to_count_references_to_objects)
[The naive approach](#the_naive_approach)
[The RCU approach](#the_rcu_approach)
[Where atomic variables coming from?](#where_atomic_variables_coming_from?)
[Conclusion](#conclusion)
[Introduction](#introduction)
[What do we do with command line options](#what_do_we_do_with_command_line_options)
**[optparsebasics](#optparse_basics)
[Adding options](#adding_options)
[Specifying help string for an option](#specifying_help_string_for_an_option)
**[Tellingoptparseto parse arguments](#telling_optparse_to_parse_arguments)
[Putting it together](#putting_it_together)
**[optparsecookbook](#optparse_cookbook)
[Support for a standalone command line options](#support_for_a_standalone_command_line_options)
[Support for mandatory (required) options.](#support_for_mandatory_(required)_options.)
[Support for options with one or more arguments](#support_for_options_with_one_or_more_arguments)
[Option destination types](#option_destination_types)
[Dependencies between options](#dependencies_between_options)
[Help screen customizations](#help_screen_customizations)
[Grouping options](#grouping_options)
[Changing programs usage string](#changing_programs_usage_string)
[Telling option’s default value](#telling_option’s_default_value)
[Better argument description](#better_argument_description)
[Adding program description](#adding_program_description)
[Adding epilog](#adding_epilog)
[Program version string](#program_version_string)
[Conclusion](#conclusion)
[Introduction](#introduction)
[What are signals?](#what_are_signals?)
[Signal as interrupt](#signal_as_interrupt)
[Signal masks](#signal_masks)
[What signals are good for](#what_signals_are_good_for)
[Signals that report exceptions](#signals_that_report_exceptions)
[Other uses of signals](#other_uses_of_signals)
[Types of signals](#types_of_signals)
[Handling exception signals](#handling_exception_signals)
[SIGKILL and SIGSTOP](#sigkill_and_sigstop)
[SIGKILL](#sigkill)
[SIGSTOP](#sigstop)
[Registering signal handler](#registering_signal_handler)
**[signal()](#signal())
[Ignoring signals and restoring original signal handler function](#ignoring_signals_and_restoring_original_signal_handler_function)
**[sigaction()](#sigaction())
**[sigaction()in action](#sigaction()_in_action)
[Conclusion](#conclusion)
[Quick links](#quick_links)
[Introduction](#introduction)
[Creating the backup](#creating_the_backup)
[What to backup](#what_to_backup)
[Figuring out device file](#figuring_out_device_file)
[Preparations](#preparations)
[Actual backup](#actual_backup)
[Restoring from backup](#restoring_from_backup)
[Preparations](#preparations)
[Restoring](#restoring)
[Restoring entire hard disk](#restoring_entire_hard_disk)
[Restoring single partition](#restoring_single_partition)
[Introduction](#introduction)
**[Howscpworks](#how_scp_works)
**[You can run commands on a remote computer usingssh](#you_can_run_commands_on_a_remote_computer_using_ssh)
**[Back toscp](#back_to_scp)
[Creating our own SSH based application](#creating_our_own_ssh_based_application)
[The idea](#the_idea)
[The code](#the_code)
[Discussion](#discussion)
[Demonstration](#demonstration)
[Conclusion](#conclusion)
[Introduction](#introduction)
[Part 1. Basics](#part_1._basics)
[Intro](#intro)
[Connecting to remote host – simple case](#connecting_to_remote_host_–_simple_case)
[RSA/DSA host fingerprint](#rsa/dsa_host_fingerprint)
[What happens when host fingerprint changes](#what_happens_when_host_fingerprint_changes)
[How to handle expected host fingerprint change](#how_to_handle_expected_host_fingerprint_change)
[Executing command on a remote computer](#executing_command_on_a_remote_computer)
[Securely copying files to and from a remote computer](#securely_copying_files_to_and_from_a_remote_computer)
[Copying multiple files](#copying_multiple_files)
[Part 2. Encryption](#part_2._encryption)
[Login without entering password?](#login_without_entering_password?)
[How modern cryptography works](#how_modern_cryptography_works)
[What are keys](#what_are_keys)
[Public/private key](#public/private_key)
[How actual encryption works](#how_actual_encryption_works)
[SSH identities](#ssh_identities)
[How to generate identity files](#how_to_generate_identity_files)
[How to install identity file](#how_to_install_identity_file)
[Installing identity files manually](#installing_identity_files_manually)
[Part 3. Advanced SSH](#part_3._advanced_ssh)
[X forwarding](#x_forwarding)
[Introduction](#introduction)
[Remote X Windows server configuration](#remote_x_windows_server_configuration)
[How SSH fixes the situation](#how_ssh_fixes_the_situation)
[What if -Y doesn’t work](#what_if_-y_doesn’t_work)
[Configuration](#configuration)
[Allowing login as root](#allowing_login_as_root)
[X forwarding](#x_forwarding)
[Other options](#other_options)
[Conclusion](#conclusion)
[Introduction](#introduction)
[How atomic variables work](#how_atomic_variables_work)
[Atomic variables size limitations](#atomic_variables_size_limitations)
[Use cases](#use_cases)
[The real thing…](#the_real_thing…)
[Time to see some action](#time_to_see_some_action)
[Precautions](#precautions)
[Conslusion](#conslusion)
[Introduction](#introduction)
[Encapsulation](#encapsulation)
[How methods work](#how_methods_work)
[How overloading works](#how_overloading_works)
[How mangling solves the problem](#how_mangling_solves_the_problem)
[Structure and size of the object](#structure_and_size_of_the_object)
[How inheritance and polymorphism work](#how_inheritance_and_polymorphism_work)
[How basic polymorphism works](#how_basic_polymorphism_works)
[How multiple inheritance works](#how_multiple_inheritance_works)
[Difference between different casting types](#difference_between_different_casting_types)
[Polymorphism and multiple inheritance](#polymorphism_and_multiple_inheritance)
[What if we try something even more complicated](#what_if_we_try_something_even_more_complicated)
[Few words about C++ constructors](#few_words_about_c++_constructors)
[Conclusion](#conclusion)
[Introduction](#introduction)
[What 64-bit support mean?](#what_64-bit_support_mean?)
[What the difference between the 32-bit and 64-bit anyway?](#what_the_difference_between_the_32-bit_and_64-bit_anyway?)
[General purpose registers](#general_purpose_registers)
[What additional registers good for?](#what_additional_registers_good_for?)
[So how good 64-bit really is?](#so_how_good_64-bit_really_is?)
[What about OS and software?](#what_about_os_and_software?)
[Does that mean that paying extra money for 64-bit Windows XP/Vista worth it?](#does_that_mean_that_paying_extra_money_for_64-bit_windows_xp/vista_worth_it?)
[How about Linux?](#how_about_linux?)
[Load PE/COFF symbols](#load_pe/coff_symbols)
[Introduction](#introduction)
[Download](#download)
[Installation and use](#installation_and_use)
[Same script but in a standalone version](#same_script_but_in_a_standalone_version)
[Introduction](#introduction)
[The obvious](#the_obvious)
[Memory leaks](#memory_leaks)
[Hibernation](#hibernation)
[The less obvious](#the_less_obvious)
[I/O cache](#i/o_cache)
[Bottom line](#bottom_line)
[Introduction](#introduction)
[Understanding the kernel installation](#understanding_the_kernel_installation)
[Kernel binary](#kernel_binary)
[Kernel version number](#kernel_version_number)
[Kernel modules](#kernel_modules)
[Linux boot process explained](#linux_boot_process_explained)
[Initial ram-disk](#initial_ram-disk)
[Mounting root file-system](#mounting_root_file-system)
[init and services](#init_and_services)
[init levels](#init_levels)
[Services](#services)
[Booting Linux with broken init scripts](#booting_linux_with_broken_init_scripts)
[Conclusion](#conclusion)
[Introduction](#introduction)
**[Whysedrules?](#why_sed_rules?)
**[sedsimple case – search and replace](#sed_simple_case_–_search_and_replace)
[Search and replace with regular expressions](#search_and_replace_with_regular_expressions)
**[sed‘s other half](#sed‘s_other_half)
**[Genericsedcommand](#generic_sed_command)
**[sedaddresses](#sed_addresses)
[Simple addressing, by line number](#simple_addressing,_by_line_number)
[Complex addressing](#complex_addressing)
[Putting it all together](#putting_it_all_together)
[Introduction](#introduction)
[The theory](#the_theory)
[Measurements](#measurements)
[Implementation](#implementation)
[Meet the hardware](#meet_the_hardware)
[Implementation details](#implementation_details)
[The code](#the_code)
[The results](#the_results)
[Conclusions](#conclusions)
[Postscript](#postscript)
[Introduction](#introduction)
[Few words about initrd](#few_words_about_initrd)
[Few words about history](#few_words_about_history)
[Back to the real thing](#back_to_the_real_thing)
[Changing it](#changing_it)
[Packing it back](#packing_it_back)
[Booting with the new initrd](#booting_with_the_new_initrd)
[Introduction](#introduction)
**[tcpdumpuses](#tcpdump_uses)
[Invocation](#invocation)
[Simple filtering](#simple_filtering)
**[Readingtcpdump‘s output](#reading_tcpdump‘s_output)
[Invocation continued](#invocation_continued)
[Choosing an interface](#choosing_an_interface)
[Turning off name resolution](#turning_off_name_resolution)
[Limiting number of packets to intercept](#limiting_number_of_packets_to_intercept)
[Saving captured data](#saving_captured_data)
[Changing packet size in the capture file](#changing_packet_size_in_the_capture_file)
[Reading from capture file](#reading_from_capture_file)
[Looking into packets](#looking_into_packets)
[Seeing Ethernet header for each packet](#seeing_ethernet_header_for_each_packet)
[Controlling time stamp](#controlling_time_stamp)
[Controlling verbosity](#controlling_verbosity)
[Printing content of the packet](#printing_content_of_the_packet)
[Packet filtering](#packet_filtering)
[Packet matching](#packet_matching)
[More qualifiers](#more_qualifiers)
[Specifying addresses](#specifying_addresses)
[Other qualifiers](#other_qualifiers)
[Complex filter expressions](#complex_filter_expressions)
[Repeating qualifiers](#repeating_qualifiers)
[Afterword](#afterword)

# Introduction [BACK TO TOC](#table_of_contents)

In this article I would like to talk about one of the most useful tools in my networking toolbox and that is tcpdump. Unfortunately mastering this tool completely is not an easy task. Yet stuff you do the most is relatively simple and may become a good springboard when diving into more complex topics.

# *tcpdump*uses [BACK TO TOC](#table_of_contents)

tcpdump is a packet sniffer. It is able to capture traffic that passes through a machine. It operates on a packet level, meaning that it captures the actual packets that fly in and out of your computer. It can save the packets into a file. You can save whole packets or only the headers. Later you can “play” recorded file and apply different filters on the packets, telling tcpdump to ignore packets that you are not interested to see.

Under the hood, tcpdump understands protocols and host names. It will do all in its power to see what host sent each packet and will tell you its name instead of the IP address.

It is exceptionally useful tool for debugging what might have caused certain networking related problem. It is an excellent tool to learn new things.

# Invocation [BACK TO TOC](#table_of_contents)

Invoking tcpdump is easy. First thing that you have to remember is that you should either be logged in as root or be a sudoer on the computer – sudoer is someone who is entitled to gain administrator rights on computer for short period of time using*sudo*command.

Running tcpdump without any arguments makes it capture packets on first network interface (excluding lo) and print short description of each packet to output. This may cause a bit of a headache in case you are using network to connect to the machine. If you are connected with SSH or telnet (rlogin?), running tcpdump will produce a line of text for each incoming or outgoing packet. This line of text will cause SSH daemon to send a packet with this line, thus causing tcpdump to produce another line of text. And this will not stop until you do something about it.

## Simple filtering [BACK TO TOC](#table_of_contents)

So first thing that we will learn about tcpdump is how to filter out SSH and telnet packets. We will study the basics of tcpdump filtering later in this guide, but for now just remember this syntax.

```text
# tcpdump not port 22
```

“not port 22” is a filter specification that tells tcpdump to filter out packets with IP source or destination port 22. As you know port 22 is SSH port. Basically, when you tell tcpdump something like this, it will make tcpdump ignore all SSH packets – exactly what we needed.

Telnet on the other hand, uses port 23. So if you are connecting via telnet, you can filter that out with:

```text
# tcpdump not port 23
```

Clear and simple!

## Reading*tcpdump*‘s output [BACK TO TOC](#table_of_contents)

By default tcpdump produces one line of text per every packet it intercepts. Each line starts with a time stamp. It tells you very precise time when packet arrived.

Next comes protocol name. Unfortunately, tcpdump understands very limited number of protocols. It won’t tell you the difference between packets belonging to HTTP and for instance FTP stream. Instead, it will mark such packets as IP packets. It does have some limited understanding of TCP. For instance it identifies TCP synchronization packets such as SYN, ACK, FIN and others. This information printed after source and destination IP addresses (if it IP packet).

Source and destination addresses follow protocol name. For IP packets, these are IP addresses. For other protocols, tcpdump does not print any identifiers unless explicitly asked to do so (see -e command line switch below).

Finally, tcpdump prints some information about the packet. For instance, it prints TCP sequence numbers, flags, ARP/ICMP commands, etc.

Here’s an example of typical tcpdump output.

```text
17:50:03.089893 IP 69.61.72.101.www > 212.150.66.73.48777: P 1366488174:1366488582
(408) ack 2337505545 win 7240 <nop,nop,timestamp 1491222906 477679143>
```

This packet is part of HTTP data stream. You can see meaning of each and every field in the packet description in tcpdump’s manual page.

Here’s another example

```text
17:50:00.718266 arp who-has 69.61.72.185 tell 69.61.72.1
```

This is ARP packet. It’s slightly more self explanatory than TCP packets. Again, to see exact meaning of each field in the packet description see tcpdump’s manual page.

## Invocation continued [BACK TO TOC](#table_of_contents)

Now, when we know how to invoke tcpdump even when connecting to the computer over some net, let’s see what command line switches are available for us.

### Choosing an interface [BACK TO TOC](#table_of_contents)

We’ll start with a simple one. How to dump packets that arrived and sent through a certain network interface. -i command line argument does exactly this.

```text
# tcpdump -i eth1
```

Will cause tcpdump to capture packets from network interface*eth1*. Or, considering our SSH/telnet experience:

```text
# tcpdump -i eth1 not port 22
```

Finally, you can specify*any*as interface name, to tell tcpdump to listen to all interfaces.

```text
# tcpdump -i any not port 22
```

### Turning off name resolution [BACK TO TOC](#table_of_contents)

As we debug networking issues, we may encounter a problem with how tcpdump works out of the box. The problem is that it tries to resolve every single IP address that it meets. I.e. when it sees an IP packet it asks DNS server for names of the computers behind IP address. It works flawlessly most of the time. However, there are two problems.

First, it slows down packet interception. It’s not a big deal when there are only few packets, but when there are thousands and tens of thousands it introduces a delay into the process. Amount of delay can be different, depending on the traffic.

Another, much more serious problem occurs when there is no DNS server around or when DNS server is not working properly. If this is the case, tcpdump spends few seconds trying to figure out two hostnames for each IP packet. This means virtually stopping intercepting the traffic.

Luckily there is a way around. There is an option that causes tcpdump to stop detecting hostnames and that is -n.

```text
# tcpdump -n
```

And here are few variations of how you can use this option in conjunction with options that we have learned already.

```text
# tcpdump -n -i eth1
# tcpdump -ni eth1 not port 22
```

### Limiting number of packets to intercept [BACK TO TOC](#table_of_contents)

Here are few more useful options. Sometimes amount of traffic that goes in and out of your computer is very high, while all you want to see is just few packets. Often you want to see who sends you the traffic, but when you try to capture anything with tcpdump it dumps so many packets that you cannot understand anything. This is the case when -c command line switch becomes handy.

It tells tcpdump to limit number of packets it intercepts. You specify number of packets you want to see. tcpdump will capture that number of packets and exit. This is how you use it.

```text
# tcpdump -c 10
```

Or with options that we’ve learned before.

```text
# tcpdump -ni eth1 -c 10 not port 22
```

This will limit number of packets that tcpdump will receive to 10. Once received 10 packets, tcpdump will exit.

### Saving captured data [BACK TO TOC](#table_of_contents)

One of the most useful tcpdump features allows capturing incoming and outgoing packets into a file and then playing this file back. By the way, you can play this file not only with tcpdump, but also with WireShark (former Ethereal), the graphical packet analyzer.

You can do this with -w command line switch. It should be followed by the name of the file that will contain the packets. Like this:

```text
# tcpdump -w file.cap
```

Or adding options that we’ve already seen

```text
# tcpdump -ni eth1 -w file.cap not port 22
```

### Changing packet size in the capture file [BACK TO TOC](#table_of_contents)

By default, when capturing packets into a file, it will save only 68 bytes of the data from each packet. Rest of the information will be thrown away.

One of the things I do often when capturing traffic into a file, is to change the saved packet size. The thing is that disk space that is required to save the those few bytes is very cheap and available most of the time. Spending few spare megabytes of your disk space on capture isn’t too painful. On the other hand, loosing valuable portion of packets might be very critical.

So, what I usually do when capturing into a file is running tcpdump with -s command line switch. It tells tcpdump how many bytes for each packet to save. Specifying 0 as a packet’s snapshot length tells tcpdump to save whole packet. Here how it works:

```text
# tcpdump -w file.cap -s 0
```

And with conjunction with options that we already saw:

```text
# tcpdump -ni eth1 -w file.cap -s 0 -c 1000 not port 22
```

Obviously you can save as much data as you want. Specifying 1000 bytes will do the job for you. Just keep in mind that there are so called jumbo frames those size can be as big as 8Kb.

### Reading from capture file [BACK TO TOC](#table_of_contents)

Now, when we have captured some traffic into a file, we would like to play it back. -r command like switch tells tcpdump that it should read the data from a file, instead of capturing packets from interfaces. This is how it works.

```text
# tcpdump -r file.cap
```

With capture file, we can easily analyze the packets and understand what’s inside. tcpdump introduces several options that will help us with this task. Lets see few of them.

## Looking into packets [BACK TO TOC](#table_of_contents)

There are several options that allow one to see more information about the packet. There is a problem though. tcpdump in general isn’t giving you too much information about packets. It doesn’t understand different protocols.

If you want to see packet’s content, it is better to use tools like Wireshark. It does understand protocols, analyzes them and allows you to see different fields, not only in TCP header, but in layer 7 protocols headers.

tcpdump is a command line tool and as most of the command line tools, its ability to present information is quiet limited. Yet, it still has few options that control the way packets presented.

### Seeing Ethernet header for each packet [BACK TO TOC](#table_of_contents)

-e command line switch, causes tcpdump to present Ethernet (link level protocol) header for each printed packet. Lets see an example.

```text
# tcpdump -e -n not port 22
```

### Controlling time stamp [BACK TO TOC](#table_of_contents)

There are four command line switches that control the way how tcpdump prints time stamp. First, there is -t option. It makes tcpdump not to print time stamps. Next comes -tt. It causes tcpdump to print time stamp as number of seconds since Jan. 1st 1970 and a fraction of a second. -ttt prints the delta between this line and a previous one. Finally, -tttt causes tcpdump to print time stamp in it’s regular format preceeded by date.

### Controlling verbosity [BACK TO TOC](#table_of_contents)

-v causes tcpdump to print more information about each packet. With -vv tcpdump prints even more information. As you could guess, -vvv produces even more information. Finally -vvvv will produce an error message telling you there is no such option:D

### Printing content of the packet [BACK TO TOC](#table_of_contents)

-x command line switch will make tcpdump to print each packet in hexadecimal format. Number of bytes that will be printed remains somewhat a mystery. As is, it will print first 82 bytes of the packet, excluding ethernet header. You can control number of bytes printed using -s command line switch.

In case you want to see ethernet header as well, use -xx. It will cause tcpdump to print extra 14 bytes for ethernet header.

Similarily -X and -XX will print contents of packet in hexadecimal and ASCII formats. The later will cause tcpdump to include ethernet header into printout.

# Packet filtering [BACK TO TOC](#table_of_contents)

We already saw a simple filter. It causes tcpdump to ignore SSH packets, allowing us to run tcpdump from remote. Now lets try to understand the language that tcpdump uses to evaluate filter expressions.

## Packet matching [BACK TO TOC](#table_of_contents)

We should understand that tcpdump applies our filter on every single incoming and outgoing packet. If packet matches the filter, tcpdump aknownledges the packet and depending on command line switches either saves it to file or dumps it to the screen. Otherwise, tcpdump will ignore the packet and account it only when telling how many packets received, dropped and filtered out when it exits.

To demostrate this, lets go back to*not port 22*expression. tcpdump ignores packets that either sourced or destined to port 22. When such packet arrives, tcpdump applies filter on it and since the result is false, it will drop the packet.

## More qualifiers [BACK TO TOC](#table_of_contents)

So, from what we’ve seen so far, we can conclude that tcpdump understands a word*port*and understands expression negation with*not*. Actually, negating an expression is part of complex expressions syntax and we will talk about complex expressions a little later. In the meantime, lets see few more packet qualifiers that we can use in tcpdump expressions.

We’ve seen that*port*qualifier specifies either source or destination port number. In case we want to specify only the source port or only the destination port we can use*src port*or*dst port*. For instance, using following expression we can see all outgoing HTTP packets.

```text
# tcpdump -n dst port 80
```

We can also specify ranges of ports.*portrange*,*src portrange*and*dst portrange*qualifiers do exactly this. For instance, lets see a command that captures all telnet and SSH packets.

```text
# tcpdump -n portrange 22-23
```

### Specifying addresses [BACK TO TOC](#table_of_contents)

Using*dst host*,*src host*and*host*qualifiers you can specify source, destination or any of them IP addresses. For example

```text
# tcpdump src host alexandersandler.net
```

Will print all packets originating from alexandersandler.net computer.

You can also specify Ethernet addresses. You do that with*ether src*,*ether dst*and*ether host*qualifiers. Each should be followed by MAC address of either source, destination or source or destination machines.

You can specify networks as well. The*net*,*src net*and*dst net*qualifiers do exactly this. Their syntax however slighly more complex than those of a single host. This is due to a netmask that has to be specified.

You can use two basic forms of network specifications. One using netmask and the other so called [CIDR notation](http://www.alexonlinux.com/short-articles/what-is-cidr-notation). Here are few examples.

```text
# tcpdump src net 67.207.148.0 mask 255.255.255.0
```

Or same command using [CIDR notation](http://www.alexonlinux.com/short-articles/what-is-cidr-notation).

```text
# tcpdump src net 67.207.148.0/24
```

Note the word*mask*that does the job of specifying the network in first example. Second example is much shorter.

### Other qualifiers [BACK TO TOC](#table_of_contents)

There are several useful qualifiers that don’t fall under any of the categories I already covered.

For instance, you can specify that you are interested in packets with specific length.*length*qualifier does this.*less*and*greater*qualifiers tell tcpdump that you are interested in packets whose length is less or greater than value you specified.

Here’s an example that demonstrates these qualifiers in use.

```text
# tcpdump -ni eth1 greater 1000
```

Will capture only packets whose size is greater than 1000 bytes.

**

## Complex filter expressions [BACK TO TOC](#table_of_contents)

As we already saw we can build more complex filter expressions using tcpdump filters language. Actually, tcpdump allows exceptionally complex filtering expressions.

We’ve seen*not port 22*expression. Applying this expression on certain packet will produce logical true for packets that are not sourced or destined to port 22. Or in two words,*not*negates the expression.

In addition to expression negation, we can build more complex expressions combining two smaller expression into one large using*and*and*or*keywords. In addition, you can use brackets to group several expressions together.

For example, lets see a tcpdump filter that causes tcpdump to capture packets larger then 100 bytes originating from google.com or from microsoft.com.

```text
# tcpdump -XX greater 100 and \(src host google.com or src host microsoft.com\)
```

*and*and*or*keywords in tcpdump filter language have same precedence and evaluated left to right. This means that without brackets, tcpdump could have captured packets from microsoft.com disregarding packet size. With brackets, tcpdump first makes sure that all packets are greater than 100 bytes and only then checks their origin.

Note the backslash symbol (“\”) before brackets. We have to place them before brackets because of shell. Unix shell has special understanding of what brackets used for. Hence we have to tell shell to leave these particular brackets alone and pass them as they are to tcpdump. Backslash characters do exactly this.

Talking about precedence, we have to keep in mind that in tcpdump’s filter expression language*not*has higher precedence than*and*and*or*. tcpdump’s manual page has very nice example and emphasizes the meaning of this.

```text
not host vs and host ace
```

and

```text
not (host vs or host ace)
```

are two different expressions. Because*not*has higher precedence over*and*and*or*, filter from the first example will capture packets not to/from vs, but to/from ace. Second filter example on the other hand will capture packets that are not to/from vs and to/from ace. I.e. first will capture packet from ace to some other host (but not to vs). Yet second example won’t capture this packet.

### Repeating qualifiers [BACK TO TOC](#table_of_contents)

To conclude this article, I would like to tell you one more thing that may become handy when writing complex tcpdump filter expressions.

Take a look at the following example.

```text
# tcpdump -XX greater 100 and \(src host google.com or microsoft.com\)
```

We already saw this example, with one little exception. In previous example we had a*src host*qualifier before microsoft.com and now its gone. The thing is that if we want to use same qualifier two times in a row, we don’t have to specify it twice. Instead we can just write qualifier’s parameter and tcpdump will know what to do.

This makes tcpdump filter expression language much easier to understand and much more readable.

# Afterword [BACK TO TOC](#table_of_contents)

I hope you found this article useful. In case you have questions, suggestions or you would like to share your appreciation to the author;-), don’t hesitate to mail me to alexander.sandler@gmail.com
