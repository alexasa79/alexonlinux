---
title: "How inheritance, encapsulation and polymorphism work in C++"
date: "2008-09-18T18:15:09"
original_url: "http://www.alexonlinux.com/how-inheritance-encapsulation-and-polymorphism-work-in-cpp"
categories: ["Programming Articles"]
tags: ["C++", "call", "code", "CPU", "encapsulation", "functions", "identifier", "inheritance", "mangling", "memory", "method", "new", "OOD", "OOP", "polymorphism", "progming"]
---

# Introduction

Inheritance, encapsulation and polymorphism are undoubtedly the cornerstones of
OOP/OOD in general and C++ in particular.

When programming C, it is very easy to remember how things work. You know that
when you add an `int` variable to a structure it mostly grows by four bytes. You
know that `long` is either four or eight bytes long depending on the architecture
you’re working with.

Things are less obvious when moving to C++. OOP brings more abstractions to the
program. As a result you are no longer sure if a+b sums two numbers or calls
some overloaded operator method that concatenates contents of two files
together.

In this article, I would like to give you a short insight into what’s going on
behind the scenes. In particular we’ll see how the three whales of OOP work in
C++.

Things that I am going to show in this article may differ from compiler to
compiler. I will talk mostly about g++ (version 4.2.3). Note however, that same
ideas apply everywhere.

# Encapsulation

As you know, encapsulation is a principle by which same entity, the object,
encapsulates data and methods that manipulate the data. You may be surprised to
find out that underneath, class methods are just plain functions.

## How methods work

In C++ there’s one fundamental difference between plain functions and class
methods. Class methods receive one additional argument and that is the pointer
to the object whose data the method is expected to manipulate. I.e. first
argument to a method is pointer to `this`.

To speed things up, C++ developers used single CPU register (ECX/RCX on
x86/x86_64) to pass pointer to `this`, instead of passing it via stack as if it
was a regular function argument (no longer true in x86_64).

Otherwise, objects know nothing about methods that operate on them.

## How overloading works

Another thing that we have to take care of in C++ is how to distinguish
between `some_function()` and `some_class::some_function()`. Or
between `some_class::some_function( int )` and `some_class::some_function()` I.e.
what’s the difference between two methods with the same name that receive
different number and type of arguments? What is the difference between method
and function that has same name?

Obviously, out of linker, compiler and preprocessor, linker is the one that
should be aware of the above difference. This is because we may
have `some_function()` in some distant object file. Linker is the component that
should find this distant function and interconnect the call to the function and
the actual function. Linker uses function name as a unique identifier of the
function.

To make things work, g++ and any other modern compiler, mangles the name of the
method/function and makes sure that:

1. Mangled method name includes name of the class it belongs to (if it belongs
   to any class).
2. Mangled method name includes number and type of arguments method receives.
3. Mangled method name includes namespace it belongs to.

With these three, `some_class::some_function()` and `some_function()` will have
totally different mangled name. See the following code sample.

```cpp
namespace some_namespace
{
    class some_class
    {
    public:
        some_class() { }
        void some_method() { }
    };
};
class some_class
{
public:
    some_class() { }
    void some_method() { }
};
void some_method()
{
    int a;
}
```

`g++` will turn:

- `void *some_class::some_method()` into `_ZN10some_class11some_methodEv`
- `void some_namespace::some_class::some_method()` into
  `_ZN14some_namespace10some_class11some_methodEv`
- `void some_method()` into `_Z11some_methodv`

Adding integer argument to `void some_method()` will turn it
from `_Z11some_methodv` to `_Z11some_methodi`.

### How mangling solves the problem

So when you create two methods with same name, but with different arguments,
compiler turns them into two functions with different names. Later, when linker
links the code together it doesn’t know that these are two methods of the same
class. From linkers standpoint, these are two different functions.

## Structure and size of the object

You probably already know that C++ class and good old C structures are nearly
the same thing. Perhaps the only difference is that all class members are
private unless specified otherwise. On the contrary, all structure members are
public.

When looking at the memory layout of the object, it is very similar to C
structure.

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/object_structure1-c0f00e8d60.png" >}})

Differences begin when you add virtual methods. Once you add virtual methods to
the class, compiler will create virtual methods table for the class. Then it
will place pointer to the table in the beginning of each instance of this class.

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/object_structure2-d8a64cb716.png" >}})

So, bear in mind that once your class has virtual methods, each object of this
class will be four or eight bytes (depends on whether you have 64-bit support or
not) bigger.

Actually, pointer to the virtual methods table does not have to be at the
beginning of the object. It is just handy to keep it at the beginning, so g++
and most of the modern compilers do it this way.

Adding virtual methods to the class will also increase amount of RAM your
program consumes and its size on your hard drive.

# How inheritance and polymorphism work

Lets say we have two classes. A and B. Class B inherits from class A.

```cpp
#include <iostream>
using namespace std;
class A
{
public:
    A() { a_member = 0; }
    int a_member;
};
class B : public A
{
public:
    B() : A() { b_member = 0; };
    int b_member;
};
int main()
{
    A *a = new B;
    a->a_member = 10;
    return 0;
}
```

The interesting thing to notice here is that `a` actually points to instance of
class B. When dereferencing `a_member`, we’re actually
dereferencing `a_member` that defined in class A, but belongs to class B (via
inheritance). To make this happen, compiler has to make sure that common part of
both classes (`a_member` in our case) located at the same offset in the object.

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/a_b1-0534206b8c.png" >}})

Now what if we have some virtual methods.

## How basic polymorphism works

Let’s change our example a bit and add some virtual methods.

```cpp
#include <iostream>
using namespace std;
class A
{
public:
    A() { a_member = 0; }
    virtual int reset() { a_member = 0; }
    void set_a_member( int a ) { a_member = a; }
    int get_a_member() { return a_member; }
protected:
    int a_member;
};
class B : public A
{
public:
    B() : A() { b_member = 0; };
    virtual int reset() { a_member = b_member = 0; }
    virtual void some_virtual_method() { }
    void set_b_member(int b ) { b_member = b; }
    int get_b_member() { return b_member; }
protected:
    int b_member;
};
int main()
{
    B *b = new B;
    A *a = b;
    b->set_b_member( 20 );
    b->set_a_member( 10 );
    a->reset();
    cout << b->get_a_member() << " " << b->get_b_member() <<
        endl;
    return 0;
}
```

If you compile and run this program it will obviously print “0 0”. But how, you
may ask. After all we did `a->reset()`. Without our understanding of polymorphism
we could think that we’re calling method that belongs to class A.

The reason it works is because when compiler sees code that dereferences pointer
to A it expects certain internal object structure and when it dereferences
pointer to B it expects different object structure. Let us take a look at both
of them.

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/a_b2-f66e52e93a.png" >}})

However even more important here is the structure of the virtual methods tables
of both classes.

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/a_b_virtuals-b1b162ddb5.png" >}})

It is because of the virtual methods table structure compilers knows what
virtual method to call. When it generates the code that dereferences pointer to
A, it expects that first method in the virtual methods table of the object will
be pointer to right `reset()` routine. It doesn’t really care if the pointer
actually points to B object. It will call first method of the virtual methods
table anyway.

## How multiple inheritance works

Multiple inheritance makes things much more complicated. The problem is that
when class C inherits from both A and B, we should have both members of class A
and class B in the instance of class C.

```cpp
#include <iostream>
using namespace std;
class A
{
public:
    A() { a_member = 0; }
protected:
    int a_member;
};
class B
{
public:
    B() { b_member = 0; }
protected:
    int b_member;
};
class C : public A, public B
{
public:
    C() : A(), B() { c_member = 0; }
protected:
    int c_member;
};
int main()
{
    C c;
    A *a1 = &c;
    B *b1 = &c;
    A *a2 = reinterpret_cast<A *>( &c );
    B *b2 = reinterpret_cast<B *>( &c );
    printf( "%p %p %p\n", &c, a1, b1 );
    printf( "%p %p %p\n", &c, a2, b2 );
    return 0;
}
```

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/inheritance1-6ffea1c9ce.png" >}})

Once we cast pointer to class C into class B, we cannot keep the value of the
pointer as is because first fields in the object occupied by fields defined in
class A (`a_member`). Therefore, when we do casting we have to do a very special
kind of casting – the one that changes the actual value of the pointer.

If you compile and run above code snippet, you will see that all the values are
the same except for b1, which should be 4 bytes bigger than other values.

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/inheritance2-8bad0425fe.png" >}})

This is what (C style casting in our case) casting does – it increments the
value of the pointer to make sure that it points to the beginning of the,
inherited from B, part of the object.

In case you wonder what other types of casting will do, here is a short
description.

### Difference between different casting types

There are five types of casting in C++.

1. reinterpret_cast<>()
2. static_cast<>()
3. dynamic_cast<>()
4. const_cast<>()
5. C style cast.

I guess you know already what const_cast<>() does. Also, it is only a compile
time casting. C style cast is same as static_cast<>(). This leaves us with three
types of casting.

1. reinterpret_cast<>()
2. static_cast<>()
3. dynamic_cast<>()

From the above example we learn that reinterpret_cast<>() does nothing to the
pointer value and leaves it as is.

static_cast<>() and dynamic_cast<>() both modify value of the pointer. The
difference between two is that the later relies on RTTI to see if the casting is
legal – it looks inside the object to see if it truly belongs to the type we’re
trying to cast from. static_cast<>() on the other hand, simply increments the
value of the pointer.

## Polymorphism and multiple inheritance

Things getting even more complicated when we have virtual methods in each one of
the classes A, B and C that we already met. Let’s add following virtual methods
to the classes.

```cpp
virtual void set_a( int new_a ) { a_member = new_a; }
```

To class A.

```cpp
virtual void set_b( int new_b ) { b_member = new_b; }
```

To class B and

```cpp
virtual void set_c( int new_c ) { c_member = new_c; }
```

To class C.

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/inheritance3-523d2db577.png" >}})

You could have assumed that even in this case class C objects will have only one
virtual tables methods, but this is not true. When you static_cast class C
object into class B object, class B object must have its own virtual tables
method. If we want to use same casting method as with regular objects (that is
adding few bytes to the pointer to reach right portion of the object), then we
have no choice but to place another virtual tables method in the middle of the
object.

As a result, you can have many different virtual methods tables for the same
class. The above diagram shows very simple case of inheritance and the truth is
that it does not get more complicated than this. Take a look at the following,
more complex, class hierarchy.

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/hierarchy1-97b25b870c.png" >}})

It may surprise you, but structure of the class X object will be quiet simple.
In our previous example inheritance hierarchy had two branches. This one has
three:

1. A-C-F-X
2. D-G-X
3. B-E-H-X

All end up with X of course. They are a little longer than in our previous
example, but there is nothing special about them. The structure of the object
will be the following:

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/classx-59322c14d9.png" >}})

As a rule of thumb, g++ (and friends) calculates the branches that lead to the
target class, class X in our case. Next it creates a virtual methods table for
each branch and places all virtual methods from all classes in the branch into
virtual methods table. This includes pointer to virtual methods of the class
itself.

If we project this rule onto our last example. A-C-F-X branch virtual methods
table will include pointers to virtual methods from classes A, C, F and X. Same
with other two branches.

### What if we try something even more complicated

The thing is that you can’t. Lets say we try to create even more complicated
hierarchy by changing class D from our previous example to inherit from class C.

![image]({{< relurl "assets/2008-09-18T181509 How inheritance encapsulation and polymorphism work in C/hierarchy2-93030afbca.png" >}})

This will immediately create ambiguous inheritance and the compiler will not
hesitate to tell you that this is what happened. This is because now class X
will have all members of classes A and C twice. Once it will have it via A-C-F-X
branch and once via A-C-D-G-X branch. It will not tell you that there’s a
problem immediately. Instead, once you will try to reference one of the members
of X inherited from either A or C, g++ will tell you that it has two variations
of the same member/method and that it does not know which one of them to call.

This what would be g++ output if you try to compile [this
file](http://www.alexonlinux.com/wp-content/uploads/2008/09/main.cc).

```cpp
main.cc: In function 'int main()':
main.cc:110: error: request for member 'set_a' is ambiguous
main.cc:29: error: candidates are: virtual void A::set_a(int)
main.cc:29: error:                 virtual void A::set_a(int)
```

All this because I was trying to do `x.set_a( 20 );` in line 110.

## Few words about C++ constructors

I guess you know what constructors are good for. In light of what we’ve seen,
you may ask yourself, who is building all those virtual methods tables and who
writes right pointer into the object.

Obviously compiler builds all the virtual methods tables. And constructor is the
one who fills in the right virtual methods table. And this is another reason why
you cannot call constructor directly – you don’t want to mess up with virtual
methods tables.

# Conclusion

For now, I think we had some very nice insight of what’s going on inside of the
objects you create. Hope you find it useful. In case you have something to say,
please leave comments here or send me emails to
[alexander.sandler@gmail.com](mailto:alexander.sandler@gmail.com).
