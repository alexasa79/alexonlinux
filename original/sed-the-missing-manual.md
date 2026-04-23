---
title: "sed – the missing manual"
type: "post"
created_at: "2008-07-16T08:28:54"
original_url: "http://www.alexonlinux.com/sed-the-missing-manual"
categories: ["Programming Articles", "System Administrator Articles"]
tags: ["modify", "regular expression", "replace", "script", "sed", "shell"]
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

# Introduction [BACK TO TOC](#table_of_contents)

*sed*is an exceptionally powerful and often overlooked tool. Its most common use is in scripts, where we want to replace part of the string matching certain pattern. While this is the most common use, it’s far from being its only use.

In this manual I’ll try to describe*sed*‘s most useful features.

# Why*sed*rules?[BACK TO TOC](#table_of_contents)

As with most of the Unix command line utilities,*sed*reads data from the standard input and writes the result into the standard output. One thing that I like about*sed*is that it doesn’t have many command line switches. Actually, I often use only one of them. We’ll talk about it a little later in this manual.

*sed*is special. Special because it turns some common and quiet complex tasks into simple. For instance, what if you want to delete last line in a file? I can think of at least four ways to achieve this, but*sed*is the only way to do this with one command. And how about deleting lines 5 through 10? You can write bash script that does the job of course. Yet same effect can be achieved with single*sed*command.

And of course its most common use. That is to find and replace a pattern with some other pattern. It is absolutely irreplaceable. The later used so widely, so I guess I have no choice but to start with it.

# *sed*simple case – search and replace [BACK TO TOC](#table_of_contents)

Let’s say we have a file with numbers. Each number occupies a single line in the file. I’ll use this file as a sample input file in this article. Obviously, you’ll have your own input information and you will do your own stuff with it, but for the sake of the demonstration, let’s think our input file contains plain numbers. By the way, you can produce the file with

```text
$ seq 20 > file
```

command. This will print numbers from 1 to 20, one in a line.

*sed*accepts commands as command line last argument. It is common practice to place*sed*‘s commands into single quotes, to tell the shell it should not try to interpret and manipulate*sed*‘s command.

*sed*commands designated with single characters, followed by optional argument. Let’s see a sample*sed*command. Since we’re talking about search and replace, this is the command we’ll see.

```text
$ cat file | sed 's/<search pattern>/<replace pattern>/[optional switches]'
```

The search and replace command is in single quotes. Both patterns are regular expressions, meaning that . will be interpreted as any character, etc. You may omit optional switches at the end. Let’s see some examples of*sed*‘s search and replace in action.

```text
$ cat file | sed 's/1/x/'
```

This is perhaps the simplest case of search and replace. This particular command replaces all instances of 1 digit with x character. You’re right. Not very handy. Let’s try something more complicated and perhaps meaningful.

```text
$ cat file | sed 's/1/x/'
```

This command replaces every instance of 1 character with x, affecting all numbers between 10 and 19 and 1. Well, this is not exactly true. This command changes 11 into x1, instead of changing it into xx. This is wrong, isn’t it?

The truth is that unless explicitly told to replace all occurrences of the search pattern with replace pattern,*sed*will replace only first occurance. I.e. 11 will turn into x1 instead of xx. This is where optional switches become handy. You can use*g*switch to tell*sed*to replace all occurrences of the search pattern in each line. This is how:

```text
$ cat file | sed 's/1/x/g'
```

Unlike previous command, this one will cause 11 to be replaced with xx.

Now let’s see few search and replace commands that envolve regular expressions.*sed*supports common regular expression syntax out of the box.

## Search and replace with regular expressions [BACK TO TOC](#table_of_contents)

There are plenty of resources describing regular expressions on the web and I assume that you possess some degree of knowledge in regular expression syntax. Yet,[here](http://www.regular-expressions.info/) is a wonderful resource on regular expressions that I myself often use.

```text
$ cat file | sed 's/^1./-/'
```

This command replaces every two digit number starting with 1, with dash character. I.e. it will replace numbers 10-19 with ‘-‘. The ‘^’ character that you see at the front of the search pattern indicates that following characters should be first characters in the line of text.

Here’s another, more complex example.

```text
$ cat file | sed 's/^\(.\)$/1\1/'
```

This example is more interesting because it demonstrates one of the more powerful feature of regular expressions and that is grouping. The sample*sed*command above places 1 before all one character long numbers. I.e numbers 1-9 will turn to 11-19.

# *sed*‘s other half [BACK TO TOC](#table_of_contents)

*sed*accepts several different commands. We’ve seen only one of them, but the rest are no less useful than search and replace.

In general, sed commands consist of two parts. First part specifies what line of input to manipulate. Second part of the command specifies the actual manipulation. The command may be search and replace that we’ve already seen. Or it may be simply delete one of the input lines or print it twice. Oh and you can run several*sed*commands one after another for each input line.

It is true that search and replace is perhaps the most common*sed*command, but other commands combined with addressing features of*sed*, are no less useful.

# Generic*sed*command [BACK TO TOC](#table_of_contents)

Generic*sed*command looks like this:

```text
sed '[address] <command>[;[address] <command>]
```

Note that I used square brackets for address. That is because address is optional (common designation of optional argument) – when we did search and replace we didn’t specify any address.

You can specify several*sed*commands one after another, delimited with semicolon.*sed*will apply commands on every line of input, command by command, line by line.

The additional two*sed*commands that I would like to explain here are ‘d’ and ‘p’ – the delete and print commands. The truth is that I rarely use any other*sed*command. Combined with*sed*‘s powerful addressing, these two and perhaps search and replace are the commands that you will use the most.

## *sed*addresses [BACK TO TOC](#table_of_contents)

The idea behind addressing in*sed*is to let you specify what lines of input you want to alter. This is a unique feature because no other command line utility allows you to modify very specific line of text in the input with such ease. Throughout this section of this article, I’ll use the ‘d’ command to demonstrate use of addresses. This command deletes the line. So if we tell*sed*to modify only the 10th line and then do ‘d’ command it will delete the line from the output.

### Simple addressing, by line number [BACK TO TOC](#table_of_contents)

You can specify a number of line that we want to alter. As you remember, each*sed*command consists of address followed by a command, delimited by a space character. Let’s see few examples.

```text
$ cat file | sed '10 d'
```

This command will delete 10th line in the input file, meaning that we will see all numbers but number 10.

In case you want to specify last line of the input file, you can use $ sign as address specification. Following example will print numbers 1 through 19.

```text
$ cat file | sed '$ d'
```

### Complex addressing [BACK TO TOC](#table_of_contents)

You can specify a range of lines. To do this, you specify first line of the range and the last one with comma in between.

```text
$ cat file | sed '1,9 d'
```

Will print lines 10 through 20. Next example on the other hand, will print lines 1 to 9.

```text
$ cat file | sed '10,$ d'
```

Now here’s something neat. You can also tell*sed*that address lines appear starting line X every Y lines. To do this, you specify X~Y as an address. Here’s an example.

```text
$ cat file | sed '1~2 d'
```

This will print the even numbers out of 1-20 range. On the contrary, following command will print only the odd numbers.

```text
$ cat file | sed '0~2 d'
```

Finally, we can specify addresses using regular expressions. You can do this by specifying regular expression in between two slash characters.

```text
$ cat file | sed '/^1./ d'
```

This command will delete all two character lines starting with 1. I.e. it will print numbers 1-9 and 20. Here’s another regular expression example.

```text
$ cat file | sed '// d'
```

# Putting it all together [BACK TO TOC](#table_of_contents)

Last command that I would like to demonstrate you is ‘p’ command. As you could have guessed, it prints input line as is. There’s one caveat in using it.*sed*will print the input line (or what may have left of it) anyway, so when telling it to print the line it will do it twice. It is easy to overcome this problem is using -n command line switch – remember I mentioned a command line switch that I use from time to time, this is it:D

Let’s see few examples of the ‘p’ command in action.

```text
$ cat file | sed 'p'
```

As expected, this command will simply print every line of text twice. Let’s see something more complex.

```text
$ cat file | sed -n '1,5 p'
```

In this command I used the addressing feature of*sed*. It will print all numbers from 1 to 5. Finally, let’s try to put it all together.

```text
$ cat file | sed -n '/^.$/ d; /^2./ d; /^1./ s/1/2/; p'
```

What you see here is three*sed*commands in a row. First one deletes all lines of text one character long. This will delete all numbers from 1 to 9. Next, it deletes all two digit numbers that start with 2. This will delete number 20. Finally, it searches for all two digit numbers starting from 1 and replaces 1 with 2. Eventually, we use ‘p’ command to print the result. Last ‘p’ command needed only because we used -n command line switch. Eventually it will print numbers 20 to 29.

Here’s another a slightly complex example, that does however exactly the same – prints numbers 20 through 29.

```text
$ cat file | sed '1,9 d; $ d; s/1/2/g;'
```

This concludes this introductionary article on*sed*. Hope you found it interesting. If you have further questions, drop me an [email](mailto:alexander.sandler@gmail.com) or leave a comment here.
