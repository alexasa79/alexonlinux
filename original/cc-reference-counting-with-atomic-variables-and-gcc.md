---
title: "C/C++ reference counting with atomic variables and gcc"
type: "post"
created_at: "2009-05-27T13:08:51"
original_url: "http://www.alexonlinux.com/cc-reference-counting-with-atomic-variables-and-gcc"
categories: ["Howto", "Programming Articles"]
tags: ["atomic", "C++", "CPU", "multithreaded", "mutex", "performance", "programming", "spinlock", "synchronization", "thread"]
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

## Introduction [BACK TO TOC](#table_of_contents)

Lets say we have a data structure that manages objects and we would like to manipulate the data structure and the objects from two or more threads. To achieve maximum performance we have to distinguish between mechanism that we use to protect the data structure itself, and the mechanism that we use to protect actual objects.

## What reference counting needed for?[BACK TO TOC](#table_of_contents)

To explain why two mechanisms provide best performance and atomic variables aid us, consider following scenario.

First thread (the manipulator) has to find a particular object in the data structure and change it. Second thread (the eraser) deletes expired objects. From time to time, first thread tries to manipulate an object that second thread tries to delete. This is a classical scenario that can be found in almost any multithreaded program.

Obviously two threads have to work with some sort of mutual exclusion mechanism. Lets say we protect entire data structure with a single mutex. In this case, manipulator thread has to hold the mutex locked for as long as it takes it to find an object and to manipulate it. This means that eraser thread won’t be able to access the data structure for as long as manipulator thread works. If all manipulator thread does is searching for entries and manipulates them, then eraser thread just won’t be able to access the data structure.

Depending on circumstances, this can be quiet devastating for the system. And, as I stated earlier, the only way to solve this problem is to split between mechanisms that protect the data structure and actual objects.

If we do so, manipulator thread will hold the mutex only when it searches for the object. Once it has the object it can release the mutex that protects the data structure, allowing eraser thread to do its job.

But then how can we make sure that the eraser thread does not delete the very same object that first thread modifies?

We could use another mutex to protect contents of actual object. There is one important question that we have to ask ourselves here. How many mutexes we need to protect object’s contents?

If we use one mutex for all objects, then we run into the same bottle-neck that we’ve just avoided. If, on the other hand, we use mutex per object, then we run into slightly different trouble.

Assuming we’ve created a mutex per object. How do we manage mutexes for objects? We can put a mutex into the object itself, but this will create another problem. If eraser thread decides to delete the object, but a moment before it does, manipulator thread decides to check the object and tries to lock its mutex. Since the mutex has already been taken by eraser thread, manipulator will fall asleep. Yet right after manipulator falls asleep, eraser will delete the object and its mutex, leaving manipulator sleeping on non-existing object. Ouch.

There are couple of things that we can do actually. One of them is implementing reference counting on objects.[Yet we have to protect the reference counter itself](do-you-need-mutex-to-protect-int). Luckily thanks to atomic variables we don’t need a mutex to protect the counter.

## This is how we will use atomic variables to count references to objects [BACK TO TOC](#table_of_contents)

First, we initialize our object’s reference counter to 1. When manipulator thread begins using it, it should increase the reference counter by one. When it has finished with the object, it should decrease the reference counter. I.e. as long as manipulator uses the object it should keep the reference counter incremented.

Once eraser thread decides to delete certain object, it should first delete the object from the data structure. It should hold the mutex that protects the data structure to do that. Next it has to decrease object’s reference counter by one.

Now remember that we’ve initialized the reference counter to 1. So if the object is not in use, its reference counter should become zero. If its zero, we can safely delete the object. This is because since the object is no longer in the data structure, we can be sure that first thread won’t use it anymore.

If its reference counter is bigger than one. In this case we should wait until threads reference counter becomes zero. But, how?

Answering this question can be quiet tricky. I usually consider one of two approaches. The naive or an approach I call the RCU approach.

### The naive approach [BACK TO TOC](#table_of_contents)

The naive approach goes like this. We create a list of objects that we want to delete. Every time our eraser thread wakes up, it runs through the list and deletes all object whose reference counter is zero.

Depending on circumstances, there might be a problem with this solution. The list of objects that we want to delete may grow and running through entire list can hog the CPU. Depending on how often we delete objects this can be good enough solution, but if its not, we have to consider RCU approach.

### The RCU approach [BACK TO TOC](#table_of_contents)

RCU is another synchronization mechanism. Its being used primary in Linux kernel. You can read about it [here](http://lwn.net/Articles/305782/). I call this approach the RCU approach, because it has some similarity to how RCU, the synchronization mechanism, works.

The idea is to assume that it takes manipulator thread some time to work with the object. I.e. manipulator keeps using the object for certain period of time at most. After that period of time, the object should no longer be in use and eraser thread should be able to delete it.

Lets say that it takes manipulator thread to do its manipulations 1 minute at most. I am exaggerating on purpose here. When eraser thread tries to delete the object, all it has to do is to grab a mutex or a [spinlock](pthread-spinlocks) that protects the data structure that contains the objects and remove the object from the data structure.

Next it has to get current time and save it in the object. Object should have methods that allows it to remember its deletion time. Then eraser thread has to append it to the end of deleted objects list. This is a special list that contains all objects that we want to delete – just as in our naive approach.

![list](http://www.alexonlinux.com/wp-content/uploads/2009/05/list.png)

Note that appending objects to the end of the list, makes it sorted by the time when we’ve deleted objects. Earlier objects in the list are those with earlier deletion time.

Next, eraser thread has to return to the beginning of the list, grab an object and check if one minute has passed since it was removed from the data structure. If so, it should check its reference counter and make sure that its indeed 0. If not, it should update its deletion time to current time and append it to the end of the list. Note that normally, this shouldn’t happen. If its reference counter is 0, then the thread should remove the object from the list and delete it.

To demonstrate you it works, take a look at the figure above. Lets say the time now is 15:35:12. This is more than one minute after we’ve deleted the first object. Therefore, once eraser wakes up and checks the list, it will instantly see that the first object in the list has been deleted more than a minute ago. This is the time for it to delete the object from the list and check the next object.

It will check second object, see that its in the list less than one minute and will keep it in the list. Now, here is the interesting property of this approach. Eraser thread doesn’t have to check the rest of the list. Because we always append objects to the end of the list, the list is sorted and eraser thread can be sure that the rest of the objects shouldn’t be deleted neither.

So instead of passing through entire list, as we did in naive approach, we can use timestamps to build a sorted list of objects and check only few objects at the beginning of the list. Depending on the circumstances, this will save huge amount processing time.

## Where atomic variables coming from?[BACK TO TOC](#table_of_contents)

Starting version 4.1.2, gcc has built-in support for atomic variables. They work on majority of architectures, but before using them, please check if your architecture supports them.

There’s a set of functions that manipulate atomic variables.

```text
type __sync_fetch_and_add (type *ptr, type value);
type __sync_fetch_and_sub (type *ptr, type value);
type __sync_fetch_and_or (type *ptr, type value);
type __sync_fetch_and_and (type *ptr, type value);
type __sync_fetch_and_xor (type *ptr, type value);
type __sync_fetch_and_nand (type *ptr, type value);
```

```text
type __sync_add_and_fetch (type *ptr, type value);
type __sync_sub_and_fetch (type *ptr, type value);
type __sync_or_and_fetch (type *ptr, type value);
type __sync_and_and_fetch (type *ptr, type value);
type __sync_xor_and_fetch (type *ptr, type value);
type __sync_nand_and_fetch (type *ptr, type value);
```

There’s no need to include any header file to use these functions. If your architecture doesn’t support them, you will receive a linker error as if you were calling a non-existing function.

Each one of these functions manipulates a variable of certain*type*.*type*can be either char, short, int, long, long long or their unsigned counterparts.

It is a good idea to wrap these functions with something that hides implementation details. This can be class that represents atomic variable or a abstract data type.

Finally, I have a nice example of how to use atomic variables in [multithreaded simple data type access and atomic variables](multithreaded-simple-data-type-access-and-atomic-variables) article.

## Conclusion [BACK TO TOC](#table_of_contents)

I hope I’ve found this interesting. In case you have further questions, please send me emails to alex@alexonlinux.com
