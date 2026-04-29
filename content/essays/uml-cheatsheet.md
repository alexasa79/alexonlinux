---
title: "UML cheatsheet"
date: "2011-09-19T18:48:44"
original_url: "http://www.alexonlinux.com/uml-cheatsheet"
categories: ["Blog", "Code library", "Howto", "Programming Articles", "Resources", "Short articles"]
tags: ["cheatsheet", "class diagram", "drawing", "inheritance", "UML", "uml diagram", "uml reference"]
---

Every once in awhile, I have to draw a UML diagram. I rarely do serious designs
with UML, however sometimes I do need to depict some piece of code in a diagram
and UML seems to be the best notation around.

Unfortunately, various sources of information on UML tend to over-complicate
things. I am not software architect and drawing UMLs is not my job. So my UML
skills are poor by definition. Moreover, I am happy with this situation and
don’t see it changing in the future (even if I get promoted;-)).

So from time to time I need a simple UML reference card. Simple search finds
references [like this one](http://www.holub.com/goodies/uml/), which are
excellent if you are serious about UML, and I am not.

Eventually, I decided to write a short UML class diagram reference card for
myself. I hope you will enjoy it as well.

## Inheritance

![image]({{< relurl "assets/2011-09-19T184844 UML cheatsheet/child_inherits_from_parent-32e4b4e855.png" >}})

So, this is how classes inherit one from another. Here the Child class inherits
from the Parent class.

## Use

![image]({{< relurl "assets/2011-09-19T184844 UML cheatsheet/user_uses_resource-f3d687d061.png" >}})

This is how the User class uses the Resource class.

## Contains and manages

![image]({{< relurl "assets/2011-09-19T184844 UML cheatsheet/whole_part_managed-512a43292f.png" >}})

Here, the Whole class contains and manages the Part class. This type of relation
can be extended to one of the following:

- One to One One to Many Many to One Many to Many

## References

![image]({{< relurl "assets/2011-09-19T184844 UML cheatsheet/whole_part_unmanaged-be04f39fff.png" >}})

Here, the Whole class references to the Part class, but does not manage it.
Again, can be extended with:

- One to One One to Many Many to One Many to Many

This is enough information for now. I’ll probably extend it over time. In any
case, please post your corrections and suggestions.
