---
title: "printf() vs stream IO in C++"
date: "2012-08-14T21:10:51"
original_url: "http://www.alexonlinux.com/printf-vs-stream-io-in-c"
categories: ["Blog", "Programming Articles", "Short articles"]
tags: ["c programming language", "C++", "CPU", "linux", "output stream", "performance", "printf", "programming", "standard library", "stream"]
---

Before joining Dell I was mostly working in kernel writing in C programming language. At Dell I still work on mostly low level stuff, but this time it is user-mode, so I am not tied up to C anymore. We’re writing in C++ and I am learning C++. One of the less appealing things for me in C++ was streaming support and the way its input/output implemented. In particular I got used to printf() functions family and leaving those in favor of streams and cout was tough. What really strikes me is the fact that no C++ book explains this stuff. All C++ books just tell you – so, my dear, this is how this stuff is done in C++. It took me some time to realize how C++ style input/output is much more convenient and powerful than printf() family of functions. Here’s why.

### The C++ way

So, In C++ you normally work with stream of some sort. Stream is an abstraction that may hide anything in the world. It can be string stream that writes things to string or debug output stream that sends debug printouts to some remote debug log server. Once you have a stream, you redefine operator << for various classes to write into stream instead of doing bit-shift. For input streams you define operator >> that reads data from string or from socket and initializes object of some class with values it read. All those operator << and >> seems kind of weird. And in fact, this can be any of the operators. For some reason, standard library uses bit-shift operators and this turned into a standard. Boost, popular C++ extensions library uses operator% to implement similar functionality, although in slightly different way.

### Convenience

At first, defining operator << for every class I write seemed like a tedious task. But you just do it once and then you can use it forever. Moreover, you can use classes that already have it to implement more stuff. So you just do it once really.

### It makes much more sense in object oriented language

Since we’re talking object oriented here, C++ way to output stuff actually makes much more sense. The way object represented as a string is a property is the object itself.

### Performance

Here is the interesting part. In printf(), the standard C library has to parse format string every time you print something. So, at runtime, every time you print something, standard C library parses your format string to figure out what and how many parameters you passed to printf(). This is important for high performance systems. Intensively printing, just anything, whether this is a debug log or part of some communication protocol rises CPU consumption of your program to the roof.

> I worked for one company where they came up with a really neat trick to overcome the problem of high CPU consumption. They had to implement debug logging in C for their high performance product. So, instead of formatting the string every time there is a printout, they saved format string and then every printout they just saved the arguments in their binary form. To read the debug log, they had to read format strings that were periodically saved in the debug log file. Then they read binary arguments for the debug printout and finally formatted the message. So instead of formatting the printouts at runtime, they formatted the printouts when debug log is read.

Another problem occurs when you by mistake pass wrong data type to printf() function and compiler misses it. Another problem is when you pass a string that is not properly null terminated. Etc. Etc. C++ way solves all these problems. First, data type resolving happens during compilation. It is up to compiler to detect what type of data you’re trying to print and to call right operator<<. This improves CPU consumption situation. For the same reason, it is much harder to print something that is of unexpected type. Compiler is usually pretty good at resolving data types.

### Wrapping it up

So, it seems that C++ way of producing output both better conforms object oriented way of programming and yields higher quality results. The only problem is that it requires you to get used to, but then, you do it just once.
