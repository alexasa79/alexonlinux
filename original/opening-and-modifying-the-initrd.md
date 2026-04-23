---
title: "Opening and modifying the initrd"
type: "post"
created_at: "2008-06-01T14:26:33"
original_url: "http://www.alexonlinux.com/opening-and-modifying-the-initrd"
categories: ["Howto", "Programming Articles", "System Administrator Articles"]
tags: ["boot", "init", "initrd", "kernel", "linux", "module", "script"]
---

## Table of contents

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

## Introduction [BACK TO TOC](#table_of_contents)

Ever wondered what’s inside of the*initrd*file? This article tells you how to look into the*initrd*and even modify it.

## Few words about initrd [BACK TO TOC](#table_of_contents)

Linux uses the*initrd*or*initial ram-disk*during the boot process. Linux kernel is very modular as you know. While the kernel main file contains only the most needed stuff, rest of the kernel, drivers included, reside in separate files – the kernel modules.

It would be impossible to create a single kernel binary image that would suit all the hardware configurations out there. Instead, kernel supports the*initrd*.*initrd*is a virtual file-system that contains drivers (kernel modules) needed to boot the system. For instance, very often a SCSI controllers drivers reside inside of the*initrd*. Kernel needs a SCSI controller driver to boot the operating system, but it does not include it, nor it can read it from hard-disk (you’d need a driver for the hard-disk, right?). And this is when the*initrd*becomes very handy.

BIOS routines that read the actual kernel from the disk into RAM, do the same job with*initrd*. When Linux kernel boots, long before trying to mount the real root file-system, it loads*initrd*into memory and makes it a temporary root file-system.

See how handy this is.*initrd*itself requires no drivers whatsoever, because BIOS handles all the work of loading it into memory. On the other hand, it contains all the drivers Linux needs to boot. And you can easily rebuild it without changing the kernel.

After loading*initrd*into RAM, the kernel runs a script named*init*that resides in*initrd*‘s root directory. The script contains commands that would load all required kernel modules. And only after that Linux tries to mount the real root file-system.

## Few words about history [BACK TO TOC](#table_of_contents)

Content of the*initrd*file and its format has significantly changed over last couple of years. Something like four years ago, it was a common practice to create a real RAM-disk with a fixed size, format it with ext2 file-system and write some data to it.

To look into it, you had to open it up with*gzip*and then mount using*loopback*device (*mount -o loop*).

Today things are totally different. Kernel configuration option that configures the size of*initrd*has gone. It wasn’t really convenient because your system was limited to certain*initrd*size. Instead kernel adapts itself to*initrd*, no matter what is it’s size.

## Back to the real thing [BACK TO TOC](#table_of_contents)

Like the kernel,*initrd*is compressed to save disk space. Unlike the kernel, it can be easily decompressed. The tool we’ll use to decompress it is, nothing fancy*gzip*. Same good old*gzip*that we use so often.

Now before we begin it is a good idea to create a directory where we’ll work. After all, internal structure of*initrd*is quiet complex and we don’t want to mix contents the initrd with contents of your, let’s say, home directory. So, do*mkdir*and*cd*to create our clean environment. We’ll call this directory A. To make things even cleaner, place*initrd*file into your newly created directory and an additional directory in it. This is directory B. In that directory we will have the contents of the*initrd*. Eventually, you should have a layout similar to this one.

![image](http://www.alexonlinux.com/wp-content/uploads/2008/05/initrd-directory-tree2.png)

Let’s start decompressing. Enter directory A and copy*initrd*that you would like to open into the directory. Then, rename it so that it would have .gz extension. The thing is that*initrd*is*gzip*compressed archive. Since*gzip*refuses do decompress something that doesn’t have .gz extension, we have to rename the file.

Next we have to decompress the file.*gzip -d <file name>*does the job for us. Next step is to open up the*cpio*archive. Yes, modern*initrd*is a*cpio*archive. We can do that with*cpio -i < <file name>*, but before we do that, we have to enter directory B specifying file name with double dots indicating file is in the parent directory – the A directory.

```text
sasha@sasha-linux:~/A$ cp /boot/initrd.img-2.6.24-16-generic .
sasha@sasha-linux:~/A$ mv initrd.img-2.6.24-16-generic initrd.img-2.6.24-16-generi
c.gz
sasha@sasha-linux:~/A$ gzip -d initrd.img-2.6.24-16-generic.gz
sasha@sasha-linux:~/A$ ls
B/  initrd.img-2.6.24-16-generic
sasha@sasha-linux:~/A$ cd B/
sasha@sasha-linux:~/A/B$ cpio -i < ../initrd.img-2.6.24-16-generic
42155 blocks
sasha@sasha-linux:~/A/B$ ls -F
bin/  conf/  etc/  init*  lib/  modules/  sbin/  scripts/  usr/  var/
sasha@sasha-linux:~/A/B$
```

In this example you can see me opening default*initial ram-disk*image from my Ubuntu 8.04 installation. We can see that the*initrd*opened up into a nice directory tree that resembles your root directory structure. In the heart of the*initrd*structure is the*init*script that does most of the job of loading right modules when system boots.

The content of the*init*script is different from distribution to distribution. The main difference is in approach. In some distributions developers preferred to keep as many initializations as possible out of the*initrd*. In other distributions developers didn’t care that much about keeping*initrd*small and fast. In general both approaches has a place under the sun. First approach based on the fact that*initrd*is a limited environment, on the contrary to Linux when its fully loaded. Thus when Linux is fully loaded, you can do more complex stuff with less effort. Second approach on the other hand, sees in*initrd*an environment that works faster than “big” Linux, so it uses*initrd*‘s fastness to do some initializations.

Ubuntu’s*initrd*image based upon first approach. It uses a shell program named*busybox*– the shell environment originally designed for embedded systems and known for its small memory footprint and good performance.*initrd*in OpenSuSE 10.2 on the other hand uses*bash*shell – same shell as you use regularly. This is a clear example of the second approach.

Another interesting input to look at, is the fact that*init*script in Ubuntu 8.04 is ~200 lines long, while in OpenSuSE 10.2 it is ~1000 lines long.

## Changing it [BACK TO TOC](#table_of_contents)

Once you have it opened up, you can see things inside of it and even make some modifications. As I already explained, structure of the*initial ram-disk*changes from distribution to distribution. However, all distributions share few common things. For instance, disregarding the distribution and a particular*initrd*format,*lib/modules/*directory always contains kernel modules that*initrd*loads at boot time. You may swap one module with another without anyone even noticing.

Number of modules, their names, etc controlled via*init*script in distribution dependent form. Therefore, no matter what distribution of Linux you have,*init*script is the key to understanding how*initrd*works. Apprehend the*init*script, and you will have full control over your*initrd*, it’s contents and what it does.

## Packing it back [BACK TO TOC](#table_of_contents)

Assuming you’re done playing around with*initrd*contents and you want to pack it back. Here is what you do.

First you have to pack*cpio*archive. Remember the B directory we’ve created. This is where it becomes handy. We want to keep contents of the*initrd*as clean as possible. The A-B separation allows us to keep the original*initrd*image out of the way when packing it back.

This is how we do that. First, we should enter the B directory. From there, run following command:

```text
find | cpio -H newc -o > ../new_initrd_file
```

This will create a new*initrd*file named*new_initrd_file*inside of directory A.

Next enter directory A and pack the*cpio*archive with*gzip*. Here’s the command that should do the job.

```text
gzip -9 new_initrd_file
```

This will pack the*initrd*in*new_initrd_file*into new_initrd_file.gz archive. Finally rename the file into whatever you want to call it. Remember that getting rid of .gz extension is a common practice, although not a necessity.

This is how complete session will look like on Ubuntu:

```text
sasha@sasha-linux:~$ cd A/B/
sasha@sasha-linux:~/A/B$ find | cpio -H newc -o > ../new_initrd_image
42155 blocks
sasha@sasha-linux:~/A/B$ cd ../
sasha@sasha-linux:~/A$ gzip -9 new_initrd_image
sasha@sasha-linux:~/A$ ls
B  initrd.img-2.6.24-16-generic  new_initrd_image.gz
sasha@sasha-linux:~/A$ mv new_initrd_image.gz initrd.img-2.6.24-16-generic-modified
sasha@sasha-linux:~/A$ ls
B  initrd.img-2.6.24-16-generic  initrd.img-2.6.24-16-generic-modified
sasha@sasha-linux:~/A$
```

## Booting with the new initrd [BACK TO TOC](#table_of_contents)

Changing*initrd*is always a risky business. When playing with matters of this kind, mistakes are common and it is important to stay on the safe side. Adding a new*GRUB*configuration is not such a big deal, but by all means do so when trying to boot the brewed five minutes ago*initrd*. You’ll save yourself lots of time reinstalling distributions and poking around with different rescue systems to make your system boot again.

Have fun!
