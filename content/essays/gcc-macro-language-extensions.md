---
title: "gcc macro language extensions"
date: "2012-02-09T00:28:41"
original_url: "http://www.alexonlinux.com/gcc-macro-language-extensions"
categories: ["Blog", "Programming Articles"]
tags: ["C++", "concatenation", "debug macro", "define", "expression", "macro", "macros with variable number of arguments", "preprocessor", "string", "stringification", "stringify", "token", "tricks", "variadic macros"]
---

One of the great things about gcc and in particular its C/C++ preprocessor is
various extensions that it has. In this essay I would like to briefly describe
three of them. One allows to turn C/C++ token into a string. Here token is
anything that you can pass as an argument to a macro. Second allows you
concatenate two tokens to create new expression. The last one allows C/C++
macros with variable number of arguments.

# Stringifying a token

Its amazing how useful this is. Take following code for example.

```cpp
std::cout << "obj.member1: " << obj.member1 << std::endl;
std::cout << ", obj.member2: " << obj.member2 << std::endl;
std::cout << ", obj.member3: " << obj.member3 << std::endl;
std::cout << ", obj.member4: " << obj.member4 << std::endl;
std::cout << ", obj.member5: " << obj.member5 << std::endl;
std::cout << ", obj.member6: " << obj.member6 << std::endl;
std::cout << ", obj.member7: " << obj.member7 << std::endl;
std::cout << ", obj.member8: " << obj.member8 << std::endl;
std::cout << ", obj.member9: " << obj.member9 << std::endl;
std::cout << ", obj.member10: " << obj.member10 << std::endl;
std::cout << ", obj.member11: " << obj.member11 << std::endl;
std::cout << ", obj.member12: " << obj.member12 << std::endl;
std::cout << ", obj.member13: " << obj.member13 << std::endl;
std::cout << ", obj.member14: " << obj.member14 << std::endl;
```

Wouldn’t you give a kidney just not to write name of every single member
of `obj` twice? Well, it appears that this can be done. Watch this:

```cpp
#define PMEM(mem) #mem ": " << mem
#define PCMEM(mem) ", " #mem ": " << mem
```

Now you can do the following:

```cpp
std::cout << PMEM(obj.member1) << std::endl;
std::cout << PCMEM(obj.member2) << std::endl;
std::cout << PCMEM(obj.member3) << std::endl;
std::cout << PCMEM(obj.member4) << std::endl;
std::cout << PCMEM(obj.member5) << std::endl;
std::cout << PCMEM(obj.member6) << std::endl;
std::cout << PCMEM(obj.member7) << std::endl;
std::cout << PCMEM(obj.member8) << std::endl;
std::cout << PCMEM(obj.member9) << std::endl;
std::cout << PCMEM(obj.member10) << std::endl;
std::cout << PCMEM(obj.member11) << std::endl;
std::cout << PCMEM(obj.member12) << std::endl;
std::cout << PCMEM(obj.member13) << std::endl;
std::cout << PCMEM(obj.member14) << std::endl;
```

These two macros will do most of the job for you. Unfortunately, they cannot
write the code for you, so you will have to write names of members of `obj` at
least once. `#` operator does one simple thing. Whatever you use it on turns
into a string. Just in case you’re wondering, I am using here another gcc’s
feature – string concatenation. gcc allows you to take two immediate strings and
concatenate them. First I turned expression `obj.member1` into a string using
`#` operator and then I concatenated it with `": "`. Note that stringification
of tokens only works inside of macro. Writing something like this:

```cpp
std::cout << #some_token << std::endl;
```

will produce compilation error and for a good reason. Another interesting thing
is the fact that you can turn anything into a string, even if it is not a valid
C/C++ expression. Take a look at the code below:

```cpp
#define DPRINT(a) #a
std::cout << DPRINT(a + b) << std::endl;
std::cout << DPRINT(hello world) << std::endl;
```

This code will print two strings, first is `a + b` and second is `hello world`.
This is despite the fact that `hello world` is not a valid C/C++.

# Token concatenation

Using this feature you can construct new C/C++ tokens using existing tokens. For
instance, if you have a large structure and you want to write a function for
every member of the structure. One way to do that is by writing the code
manually. But I guess you don’t need me for that.

```cpp
struct some_struct {
    int member1;
    bool member2;
    unsigned long member3;
};
#define ADD_GETTER(TYPE, MEMBER) \
    TYPE get_ ## MEMBER(struct some_struct& st) { \
        return st.MEMBER; \
}
ADD_GETTER(int, member1);
ADD_GETTER(bool, member2);
ADD_GETTER(unsigned long, member3);
```

Lets analyze this piece of code for second. First I defined a structure
called `some_struct`. Next, I wanted a macro that defines getter function for
every member of `some_struct`. I added `ADD_GETTER` macro for that. Then I
called it three times in a row providing type of the field in `some_struct` and
name of the member.

Calling a macro for member1 expanded to following piece of code:

```cpp
int get_member1(struct some_struct& st)
{
    return st.member1;
}
```

Notice how it created name of the function. This is concatenation operation in
action. `##` makes gcc and g++ preprocessor concatenate two
tokens, `get_` and `member1` into single token. `##` operator removes all space
characters between two tokens. Another thing that it does is eliminating white
space and punctuation characters between two tokens. This is especially useful
when implementing macros with variable number of arguments.

# Macros with variable number of arguments

You can define a macro with variable number of arguments following way:

```cpp
#define VMACRO(argument1, argument2, ...) do_something()
```

The three dots as last argument of the macro tells compiler that this is a
variadic macro. I.e. this is a macro that receives variable number of arguments.
To get access to arguments, you have to use special keyword `__VA_ARGS__`. Like
this:

```cpp
#define VMACRO(argument1, argument2, ...) do_something(__VA_ARGS__)
```

In this example I am ignoring `argument1` and `argument2` and passing remaining
arguments to `do_something()` routine. When I first learned about this feature,
I immediately tried to use it for debug printouts macros. This is the code that
I’ve written.

```c
#include <stdio.h>
#define DPRINT(format, ...) printf("DEBUG: " format, __VA_ARGS__)
int main()
{
    DPRINT("hello world");
}
```

Note that strings have to be immediate values. For instance calling
`DPRINT(format, "...");` where `format` is pointer to string will not work
because gcc cannot concatenate `format` with “DEBUG” string. Anyway, I wanted
to address something different. You will be surprised to learn that this code
doesn’t compile. This is because after preprocessing this code turns into
something that is not valid C/C++. This is how `main` will look like after
preprocessing:

```c
int main()
{
    printf("DEBUG: " "hello world", );
}
```

Note the comma character after “hello world”. The thing is that empty token is
valid token in gcc, so passing nothing as argument translates into nothing.
There is a workaround for this problem. That is using concatenation operation.
Lets change our implementation of `DPRINT` a little.

```c
#include <stdio.h>
#define DPRINT(format, ...) printf("DEBUG: " format, ##__VA_ARGS__)
int main()
{
    DPRINT("hello world");
}
```

Note concatenation operator before `__VA_ARGS__`. I already mentioned that
concatenation operator gets rid of white space and punctuation characters
between two tokens. This is exactly what it does in this case – it removes comma
between format and empty token leaving clean
`printf("DEBUG: " "hello world");`. This is exactly what we needed.
