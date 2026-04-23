---
title: "Multithreaded simple data type access and atomic variables"
date: "2008-12-23T13:55:29"
original_url: "http://www.alexonlinux.com/multithreaded-simple-data-type-access-and-atomic-variables"
categories: ["Programming Articles"]
tags: ["atomic", "linux", "multithreaded", "mutex", "pthread", "semaphore", "spinlock", "thread"]
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

# Introduction [BACK TO TOC](#table_of_contents)

In this article I would like to continue subject I started in my previous two essays ([essay 1]({{< relref "essays/do-you-need-a-mutex-to-protect-an-int.md" >}}) and [essay 2]({{< relref "essays/pthread-spinlocks.md" >}})). Question I am trying to answer is what is the most efficient, yet safe way of accessing simple data type variables from two or more threads. I.e. how to change a variable from two threads at the same time, without screwing its value.

[In my first essay]({{< relref "essays/do-you-need-a-mutex-to-protect-an-int.md" >}}) I’ve shown how easy it is to turn variable value into garbage by modifying it from two or more threads.[In my second essay]({{< relref "essays/pthread-spinlocks.md" >}}) I am talking about spinlocks, a recent addition into*pthread*library. Spinlocks indeed can help to solve the problem. Yet spinlocks more suitable for protecting small data structures rather than simple data types such as*int*and*long*. Atomic variables, on the other hand, are perfect for the later task.

Key thing about atomic variables is that once someone starts reading or writing it, nothing else cannot interrupt the process and come in the middle. I.e. nothing can split the process of accessing atomic variable into two. This is why they called atomic.

On the practical side, atomic variables are the best solution for the problem of simultaneous access to a simple variable from two or more threads.

# How atomic variables work [BACK TO TOC](#table_of_contents)

This is actually quiet simple. Intel x86 and x86_64 processor architectures (as well as vast majority of other modern CPU architectures) has instructions that allow one to lock FSB, while doing some memory access. FSB stands for Front Serial Bus. This is the bus that processor use to communicate with RAM. I.e. locking FSB will prevent from any other processor (core), and process running on that processor, from accessing RAM. And this is exactly what we need to implement atomic variables.

Atomic variables being widely used in kernel, but from some reason no-one bothered to implement them for user-mode folks. Until gcc 4.1.2.

# Atomic variables size limitations [BACK TO TOC](#table_of_contents)

From practical considerations, gurus at Intel did not implement FSB locking for every possible memory access. For instance, for quiet some time, Intel processors allow memcpy() and memcmp() implementation with one processor instruction. But locking FSB while copying large memory buffer can be too expensive.

In practice you can lock FSB while accessing 1, 2, 4 and 8 byte long integers. Almost transparently, gcc allows you to do atomic operations on*int*‘s,*long*‘s and*long long*‘s (and their unsigned counterparts).

# Use cases [BACK TO TOC](#table_of_contents)

Incrementing a variable and knowing that no-one else screws its value is nice, but not enough. Consider following piece of pseudo-code.

```text
decrement_atomic_value();

if (atomic_value() == 0)

    fire_a_gun();
```

Let us imagine that the value of an atomic variable is 1. What happens if two threads of execution try to execute this piece of pseudo-C simultaneously?

Back to our simulation. It is possible that thread 1 will execute line 1 and stop, while thread 2 will execute line 1 and continue executing line 2. Later thread 1 will wake up and execute line 2.

![two_threads]({{< relurl "assets/2008-12-23T135529 Multithreaded simple data type access and atomic variables/two_threads-1d8b30a3c0.png" >}})

When this happens, no one of the threads will run*fire_a_gun()*routine (line 3). This is obviously wrong behavior and if we were protecting this piece of code with a mutex or a spinlock this would not have happened.

> In case you’re wondering how likely something like this to happen, be sure that this is very likely. When I first started working with multithreaded programing I was amazed to find out that despite our intuition tells us that scenario I described earlier is unlikely, it happens overwhelmingly often.

As I mentioned, we could solve this problem by giving up on atomic variables and using spinlock or mutex instead. Luckily, we can still use atomic variables.*gcc*developers have thought about our needs and this particular problem and offered a solution. Lets see actual routines that operate atomic variables.

# The real thing…[BACK TO TOC](#table_of_contents)

There are several simple functions that do the job. First of all, there are twelve (yes, twelve – 12) functions that do atomic add, substitution, and logical atomic or, and, xor and nand. There are two functions for each operation. One that returns value of the variable before changing it and another that returns value of the variable after changing it.

Here are the actual functions:

```text
type __sync_fetch_and_add (type *ptr, type value);

type __sync_fetch_and_sub (type *ptr, type value);

type __sync_fetch_and_or (type *ptr, type value);

type __sync_fetch_and_and (type *ptr, type value);

type __sync_fetch_and_xor (type *ptr, type value);

type __sync_fetch_and_nand (type *ptr, type value);
```

These are functions that return value of the variable before changing it. Following functions, on the other hand, return value of the variable after changing it.

```text
type __sync_add_and_fetch (type *ptr, type value);

type __sync_sub_and_fetch (type *ptr, type value);

type __sync_or_and_fetch (type *ptr, type value);

type __sync_and_and_fetch (type *ptr, type value);

type __sync_xor_and_fetch (type *ptr, type value);

type __sync_nand_and_fetch (type *ptr, type value);
```

*type*in each of the expressions can be one of the following:

- int
- unsigned int
- long
- unsigned long
- long long
- unsigned long long

These are so called built-in functions, meaning that you don’t have to include anything to use them.

# Time to see some action [BACK TO TOC](#table_of_contents)

Back to the example I started in the [first essay]({{< relref "essays/do-you-need-a-mutex-to-protect-an-int.md" >}}) I mentioned earlier.

To remind you, this small program opens several of threads. Number of threads is as number of CPUs in the computer. Then it binds each one of the threads to one of the CPUs. Finally each thread runs a loop and increments a global integer 1 million times.

```text
#include <stdio.h>

#include <pthread.h>

#include <unistd.h>

#include <stdlib.h>

#include <sched.h>

#include <linux/unistd.h>

#include <sys/syscall.h>

#include <errno.h>



#define INC_TO 1000000 // one million...



int global_int = 0;



pid_t gettid( void )

{

	return syscall( __NR_gettid );

}



void *thread_routine( void *arg )

{

	int i;

	int proc_num = (int)(long)arg;

	cpu_set_t set;



	CPU_ZERO( &set );

	CPU_SET( proc_num, &set );



	if (sched_setaffinity( gettid(), sizeof( cpu_set_t ), &set ))

	{

		perror( "sched_setaffinity" );

		return NULL;

	}



	for (i = 0; i < INC_TO; i++)

	{

//		global_int++;

		__sync_fetch_and_add( &global_int, 1 );

	}



	return NULL;

}



int main()

{

	int procs = 0;

	int i;

	pthread_t *thrs;



	// Getting number of CPUs

	procs = (int)sysconf( _SC_NPROCESSORS_ONLN );

	if (procs < 0)

	{

		perror( "sysconf" );

		return -1;

	}



	thrs = malloc( sizeof( pthread_t ) * procs );

	if (thrs == NULL)

	{

		perror( "malloc" );

		return -1;

	}



	printf( "Starting %d threads...\n", procs );



	for (i = 0; i < procs; i++)

	{

		if (pthread_create( &thrs[i], NULL, thread_routine,

			(void *)(long)i ))

		{

			perror( "pthread_create" );

			procs = i;

			break;

		}

	}



	for (i = 0; i < procs; i++)

		pthread_join( thrs[i], NULL );



	free( thrs );



	printf( "After doing all the math, global_int value is: %d\n",

		global_int );

	printf( "Expected value is: %d\n", INC_TO * procs );



	return 0;

}
```

To compile and run, throw this snippet into a file and run:

```text
gcc -pthread "file name"
```

Then run./a.out`to execute the program.

Note lines 36 and 37. Instead of simply incrementing the variable, I use built-in function*__sync_fetch_and_add()*. Running this code obviously produces expected results – i.e. value of*global_int*is 4,000,000 as expected (number of CPUs in the machine multiply 1 million – in my case this is a 4 core machine). Remember that [when I ran this code snippet leaving line 36 as is]({{< relref "essays/do-you-need-a-mutex-to-protect-an-int.md" >}}), the result was 1,908,090 and not 4,000,000 as we’d expect.

# Precautions [BACK TO TOC](#table_of_contents)

When using atomic variables, some extra precautions have to be taken. One serious problem with atomic variable implementation in*gcc*is that it allows you to do atomic operations on regular variables. I.e. there is no clear distinction between atomic variables and regular variables. There is nothing that prevents you from incrementing value of the atomic variable with*__sync_fetch_and_add()*as I just demonstrated and later in the code doing same thing with regular ++ operator.

Obviously this might be a serious problem. Things tend to be forgotten and it is a matter of time until someone in your project or even you yourself will modify value of the variable using regular operators, instead of atomic functions that*gcc*has.

To address this problem, I strongly suggest wrapping around atomic functions and variables with either ADT in C or C++ class.

# Conslusion [BACK TO TOC](#table_of_contents)

This article concludes a series or articles and essays where we investigate and study newest techniques in the world of multithreaded programming for Linux. Hope you’ll find these essays and article useful. As usual, in case you have further questions please don’t hesitate to email me to alexander.sandler@gmail.com.
