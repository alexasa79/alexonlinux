---
title: "Rethinking linked list insertion"
date: "2009-12-19T14:24:36"
original_url: "http://www.alexonlinux.com/rethinking-linked-list-insertion"
categories: ["Blog", "Code library", "Short articles"]
tags: []
---

There is one nice thing in looking for a new job. That is, you meet lots of new
people and have a chance to learn from them. For example in one of the companies
I was asked about something called anti-debugging. I didn’t have a clue what
that is and had to ask for an explanation. Apparently, this is a set of
techniques used to fool a debugger and make the code undebuggable.

Anyway, here’s something else that I learned during one of the interviews.

I was asked to implement insertion into a linked list in*C*. Each list node has
a number (*num*). Numbers in the list should be sorted in ascending order – node
with lowest number should be first. Here is my naive implementation.

```text
void list_insert(int num)

{

        list_node_t *n, *tmp, *prev;



        n = allocate_node();

        n->num = num;



        if (!head) {

                head = n;

                n->next = NULL;

        } else {

                tmp = head;

                prev = NULL;

                while (tmp) {

                        if (tmp->num >= n->num) {

                                if (prev == NULL) {

                                        head->next = n;

                                        n->next = NULL;

                                } else {

                                        n->next = tmp;

                                        prev->next = n;

                                }



                                break;

                        }



                        prev = tmp;

                        tmp = tmp->next;

                }



                if (!tmp) {

                        n->next = NULL;

                        prev->next = n;

                }

        }

}
```

Yeah, well it is pretty long, but that’s how you do it, right? You have to make
sure that the list is not empty (line 8 ) – if it is empty, then new node should
be placed at the head of the list. Then we have to find right place for the new
node and insert it into its position (lines 14-29). Finally, if we didn’t find a
good position for the new node, we should put the node at the end of the list
(lines 31-34).

When I showed this to the examiner he asked me to rethink the routine. In
particular he didn’t like number of*if*statements. After an hour of discussing
various optimizations, this is what we came up with.

```text
void list_insert(int num)

{

        list_node_t **tmp, *n;



        n = allocate_node();

        n->num = num;



        tmp = &head;

        while (*tmp) {

                if ((*tmp)->num >= n->num)

                        break;

                tmp = &(*tmp)->next;

        }



/*

        (*tmp) = n;

       n->next = (*tmp)->next;

*/



/*

        The code in the comment above is broken. Thanks to jagan 

        for pointing this out. Here's the right code.

*/

        n->next = *tmp;

        *tmp = n;

}
```

There are several things that make this version better.

First of all, instead of having a pointer to current node (*tmp*) and previous
node (*prev*), we have one pointer that corresponds to pointer to previous node.
This way we can always get to the current node via*next*field in the previous
node. Thus we don’t need two pointers anymore.

Also, this version uses pointer to pointer to node to traverse through the list.
We don’t insert the node in the while loop anymore. Purpose of the while loop is
to find right place for the new node. This spares*if*statement that tests if the
list is empty and*if*statement in the loop.

Finally, once*tmp*points to the right place, we insert the node.

Second version runs faster too. I did a small program that tests both versions
and it appears that the later version is something like 5% faster.
