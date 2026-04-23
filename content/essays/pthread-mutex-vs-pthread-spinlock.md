---
title: "pthread mutex vs pthread spinlock"
date: "2009-05-17T14:16:41"
original_url: "http://www.alexonlinux.com/pthread-mutex-vs-pthread-spinlock"
categories: ["Programming Articles", "Short articles"]
tags: ["CPU", "mutex", "pthread", "speed", "spinlock", "synchronization", "thread"]
---

*Update 06/16/2009: On several occasions, commentators to this article pointed
out that this essay is somewhat incomplete. Therefore, before I continue, I
would like to make some things clear.*

*Before considering the code below, please note that spinlocks are totally
useless on uni-processor computers. This is due to a nature of spinlocks, which
I will describe in future essays.*

*Also, it is not the intent of this article to show that spinlocks better than
mutexes in all circumstances. Spinlocks perform better than mutexes in this
particular setup, on multi-processor computer. It does not mean that spinlocks
are good for you. Apply your own judgment when considering using materials
presented in this article for your needs. *

In this article I would like to demonstrate you how spinlocks are more efficient
than mutexes. I’ll demonstrate a program that does the following.

It builds a list of integers and then starts two threads, each removing entries
from the list. Since both threads work with the same list at the same time, list
has to be protected with synchronization mechanism of some kind.

Depending on whether the program has been compiled with USE_SPINLOCK or not, it
will use a spinlock or a mutex to protect the list. In any case, it will display
number of seconds that has passed from the moment threads has been started,
until they finish.

```text
#include <stdio.h>

#include <pthread.h>

#include <unistd.h>

#include <sys/syscall.h>

#include <errno.h>

#include <sys/time.h>



#include <list>



#define LOOPS 10000000



using namespace std;



list<int> the_list;



#ifdef USE_SPINLOCK

pthread_spinlock_t spinlock;

#else

pthread_mutex_t mutex;

#endif



pid_t gettid() { return syscall( __NR_gettid ); }



void *consumer(void *ptr)

{

    int i;



    printf("Consumer TID %lu\n", (unsigned long)gettid());



    while (1)

    {

#ifdef USE_SPINLOCK

        pthread_spin_lock(&spinlock);

#else

        pthread_mutex_lock(&mutex);

#endif



        if (the_list.empty())

        {

#ifdef USE_SPINLOCK

            pthread_spin_unlock(&spinlock);

#else

            pthread_mutex_unlock(&mutex);

#endif

            break;

        }



        i = the_list.front();

        the_list.pop_front();



#ifdef USE_SPINLOCK

        pthread_spin_unlock(&spinlock);

#else

        pthread_mutex_unlock(&mutex);

#endif

    }



    return NULL;

}



int main()

{

    int i;

    pthread_t thr1, thr2;

    struct timeval tv1, tv2;



#ifdef USE_SPINLOCK

    pthread_spin_init(&spinlock, 0);

#else

    pthread_mutex_init(&mutex, NULL);

#endif



    // Creating the list content...

    for (i = 0; i < LOOPS; i++)

        the_list.push_back(i);



    // Measuring time before starting the threads...

    gettimeofday(&tv1, NULL);



    pthread_create(&thr1, NULL, consumer, NULL);

    pthread_create(&thr2, NULL, consumer, NULL);



    pthread_join(thr1, NULL);

    pthread_join(thr2, NULL);



    // Measuring time after threads finished...

    gettimeofday(&tv2, NULL);



    if (tv1.tv_usec > tv2.tv_usec)

    {

        tv2.tv_sec--;

        tv2.tv_usec += 1000000;

    }



    printf("Result - %ld.%ld\n", tv2.tv_sec - tv1.tv_sec,

        tv2.tv_usec - tv1.tv_usec);



#ifdef USE_SPINLOCK

    pthread_spin_destroy(&spinlock);

#else

    pthread_mutex_destroy(&mutex);

#endif



    return 0;

}
```

Lets see how this little program works in greater detail.*main()*starts with
initialization of a mutex or a spinlock, in lines 67-71. Next it initializes the
list. Number of entries it will push into the list depends on LOOPS definition
from line 10. Finally, in lines 77-81 it measures current time and spawns two
threads. Then it waits for both threads to finish their job.

The thread, between lines 24 and 56, runs in a loop and pops entries from the
list. Once the list is empty, thread exits. Each iteration of the loop it locks
the mutex/spinlock and then unlocks it (lines 32-36 and 51-55).

Once both threads are over,*main()*will measure the time again and print
difference between two measurements. This difference is how we measure
effectiveness. The less time it took to run, the better.

Lets run the code and see how it performs, first with mutex and then with
spinlock.

```text
~/lab/mutex-vs-spinlock --> g++ -Wall -pthread main.cc

~/lab/mutex-vs-spinlock --> ./a.out

Consumer TID 19602

Consumer TID 19603

Result - 7.99794

~/lab/mutex-vs-spinlock --> g++ -DUSE_SPINLOCK -Wall -pthread main.cc

~/lab/mutex-vs-spinlock --> ./a.out

Consumer TID 19610

Consumer TID 19611

Result - 2.587424

~/lab/mutex-vs-spinlock -->
```

As we can see, the picture is clear. We can see that using spinlock, it took 2.5
seconds to complete the test. However when used mutex, it took almost 8 seconds
to complete. This is 3 times more time.

This proves that the spinlock is more effective in term of CPU consumption and
speed.
