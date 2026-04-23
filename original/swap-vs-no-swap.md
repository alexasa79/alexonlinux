---
title: "Swap vs. no swap"
type: "post"
created_at: "2008-08-21T11:43:25"
original_url: "http://www.alexonlinux.com/swap-vs-no-swap"
categories: ["Opinion", "System Administrator Articles"]
tags: ["cache", "hibernate", "io", "kernel", "leaks", "linux", "memory", "partition", "performance", "RAM", "speed", "swap", "virtual memory"]
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

# Introduction [BACK TO TOC](#table_of_contents)

This short article deals with simple question. How exactly lack of swap partition affects Linux’s performance. What would happen if you turn the swap off?

# The obvious [BACK TO TOC](#table_of_contents)

## Memory leaks [BACK TO TOC](#table_of_contents)

The obvious price one would have to pay for turning the swap off is lack of so called virtual memory. The term virtual memory refers to several different things really. What I mean is that when a program leaks memory, the memory it has leaked will remain unused as long as the program still running.

On the contrary, when swap is on, operating system copies memory that is not in use to the swap partition, by that freeing actual memory. So when one of the programs has memory leaks, memory that being lost by the program finds its way to hard drive instead of continuing to take precious memory.

I never heart of a program that claims that it has no memory leaks. Every program looses memory. It is a matter of time until it will ran out of memory and then the program will crash. Swap is not an ultimate solution for this problem because swap space can run out too, yet it significantly prologues live of the individual processes and the overall system.

## Hibernation [BACK TO TOC](#table_of_contents)

It is being referred to as hibernation and perhaps few other ways. At the bottom line this is a method to fast turn on and off the computer.

Instead of turning off all services and programs and then initializing them again, operating system suspends execution of all processes, then writes all used memory to swap space and then turns off the computer.

When you turn your computer back on, instead of starting a brand new session from scratch, operating system restores memory from swap and resumes all programs that were running, without reinitializing them.

> By the way, one of the reasons why recommended swap space size is twice the size of the RAM that is in the computer is to let the operating system to accommodate all your RAM in swap partition – to allow hibernation of course.

Obviously, when you don’t have swap partition, you cannot do hibernation anymore.

# The less obvious [BACK TO TOC](#table_of_contents)

## I/O cache [BACK TO TOC](#table_of_contents)

Linux uses all available memory to do I/O cache – that is to save portions of the hard disk space and to serve it straight from the memory avoiding relatively long disk access. This is why for instance when you copy several large files from one place to another several times in a row, second copy takes significantly fewer time then the first. This is also the reason why, in Linux, it takes a second to write a megabyte to a floppy disk, a device known for its slowliness – the data being written to the memory and not to an actual disk.

Also, disks optimized to read and write large chunks of data. Average program on the contrary reads and writes small chunks of data. To speed up the process, Linux collects several small read and write requests into bigger thus increasing disk performance. This however requires memory.

What many people don’t realize is that Linux uses all available memory and always tries to free even more memory for caching. When it sees a piece of memory that some program did claim, but doesn’t use very often, it will copy it to swap partition and use the actual memory for caching. Once the program will try to do something with this memory piece, Linux will detect this and read the contents of the memory piece from swap partition back to the real RAM.

> By the way, this is the reason why when you minimize a program and after a while restore it, it takes it a few seconds to become fully functional – Linux had moved pieces of its memory to swap partition and now this memory has to be restored. Reading data from disk takes more time than actual memory access, thus the delay you see when you restore the program. You can change how hard the operating system tries to free memory for cache by changing value in the /proc/sys/vm/swappiness. The value varies between 0 and 100. Value of 100 means that operating system will not wait much time to move memory to cache. Note that whatever swappiness value you have, Linux tries to keep your system stable and will move pieces of memory into cache if it thinks it is necessary.

The real issue here is that this mechanism should be very balanced. Linux is optimized to use all available memory for caching. When it doesn’t have enough memory, time it takes to access data on disks will rise! Since all programs leak memory, over the time Linux will have less and less memory for caching and disk access speed will drop.

# Bottom line [BACK TO TOC](#table_of_contents)

Bottom line is that, without swap:

1. Your system will be less stable.
2. Your system will not be able to hibernate.
3. Disk access speed in your system will be slower compared to a system that has swap partition. Moreover, disk access speed will drop in the course of time.

In case you have further questions, please email me to [alexander.sandler@gmail.com](mailto:alexander.sandler@gmail.com).
