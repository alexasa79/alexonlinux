---
title: "sed – the missing manual"
date: "2008-07-16T08:28:54"
original_url: "http://www.alexonlinux.com/sed-the-missing-manual"
categories: ["Programming Articles", "System Administrator Articles"]
tags: ["modify", "regular expression", "replace", "script", "sed", "shell"]
---

# Introduction

`sed` is an exceptionally powerful and often overlooked tool. Its most common
use is in scripts, where we want to replace part of the string matching certain
pattern. While this is the most common use, it’s far from being its only use.

In this manual I’ll try to describe `sed`’s most useful features.

# Why `sed` Rules?

As with most of the Unix command line utilities, `sed` reads data from the
standard input and writes the result into the standard output. One thing that I
like about `sed` is that it doesn’t have many command line switches. Actually, I
often use only one of them. We’ll talk about it a little later in this manual.

`sed` is special. Special because it turns some common and quiet complex tasks
into simple. For instance, what if you want to delete last line in a file? I can
think of at least four ways to achieve this, but `sed` is the only way to do
this with one command. And how about deleting lines 5 through 10? You can write
bash script that does the job of course. Yet same effect can be achieved with
single `sed` command.

And of course its most common use. That is to find and replace a pattern with
some other pattern. It is absolutely irreplaceable. The later used so widely, so
I guess I have no choice but to start with it.

# `sed` Simple Case – Search And Replace

Let’s say we have a file with numbers. Each number occupies a single line in the
file. I’ll use this file as a sample input file in this article. Obviously,
you’ll have your own input information and you will do your own stuff with it,
but for the sake of the demonstration, let’s think our input file contains plain
numbers. By the way, you can produce the file with

```text
$ seq 20 > file
```

command. This will print numbers from 1 to 20, one in a line.

`sed` accepts commands as command line last argument. It is common practice to
place `sed`’s commands into single quotes, to tell the shell it should not try
to interpret and manipulate `sed`’s command.

`sed` commands designated with single characters, followed by optional argument.
Let’s see a sample `sed` command. Since we’re talking about search and replace,
this is the command we’ll see.

```text
$ cat file | sed 's/<search pattern>/<replace pattern>/[optional switches]'
```

The search and replace command is in single quotes. Both patterns are regular
expressions, meaning that `.` will be interpreted as any character, etc. You may
omit optional switches at the end. Let’s see some examples of `sed`’s search and
replace in action.

```text
$ cat file | sed 's/1/x/'
```

This is perhaps the simplest case of search and replace. This particular command
replaces all instances of 1 digit with x character. You’re right. Not very
handy. Let’s try something more complicated and perhaps meaningful.

```text
$ cat file | sed 's/1/x/'
```

This command replaces every instance of 1 character with x, affecting all
numbers between 10 and 19 and 1. Well, this is not exactly true. This command
changes 11 into x1, instead of changing it into xx. This is wrong, isn’t it?

The truth is that unless explicitly told to replace all occurrences of the
search pattern with replace pattern, `sed` will replace only first occurance.
I.e. 11 will turn into x1 instead of xx. This is where optional switches become
handy. You can use `g` switch to tell `sed` to replace all occurrences of the
search pattern in each line. This is how:

```text
$ cat file | sed 's/1/x/g'
```

Unlike previous command, this one will cause 11 to be replaced with xx.

Now let’s see few search and replace commands that envolve regular expressions.
`sed` supports common regular expression syntax out of the box.

## Search and replace with regular expressions

There are plenty of resources describing regular expressions on the web and I
assume that you possess some degree of knowledge in regular expression syntax.
Yet, [here](http://www.regular-expressions.info/) is a wonderful resource on
regular expressions that I myself often use.

```text
$ cat file | sed 's/^1./-/'
```

This command replaces every two digit number starting with 1, with dash
character. I.e. it will replace numbers 10-19 with ‘-‘. The ‘^’ character that
you see at the front of the search pattern indicates that following characters
should be first characters in the line of text.

Here’s another, more complex example.

```text
$ cat file | sed 's/^\(.\)$/1\1/'
```

This example is more interesting because it demonstrates one of the more
powerful feature of regular expressions and that is grouping. The sample `sed`
command above places 1 before all one character long numbers. I.e numbers 1-9
will turn to 11-19.

# `sed`’s Other Half

`sed` accepts several different commands. We’ve seen only one of them, but the
rest are no less useful than search and replace.

In general, sed commands consist of two parts. First part specifies what line of
input to manipulate. Second part of the command specifies the actual
manipulation. The command may be search and replace that we’ve already seen. Or
it may be simply delete one of the input lines or print it twice. Oh and you can
run several `sed` commands one after another for each input line.

It is true that search and replace is perhaps the most common `sed` command, but
other commands combined with addressing features of `sed`, are no less useful.

# Generic `sed` Command

Generic `sed` command looks like this:

```text
sed '[address] <command>[;[address] <command>]
```

Note that I used square brackets for address. That is because address is
optional (common designation of optional argument) – when we did search and
replace we didn’t specify any address.

You can specify several `sed` commands one after another, delimited with
semicolon. `sed` will apply commands on every line of input, command by command,
line by line.

The additional two `sed` commands that I would like to explain here are `d` and
`p` – the delete and print commands. The truth is that I rarely use any other
`sed` command. Combined with `sed`’s powerful addressing, these two and perhaps
search and replace are the commands that you will use the most.

## `sed` Addresses

The idea behind addressing in `sed` is to let you specify what lines of input
you want to alter. This is a unique feature because no other command line
utility allows you to modify very specific line of text in the input with such
ease. Throughout this section of this article, I’ll use the `d` command to
demonstrate use of addresses. This command deletes the line. So if we tell `sed`
to modify only the 10th line and then do `d` command it will delete the line
from the output.

### Simple addressing, by line number

You can specify a number of line that we want to alter. As you remember, each
`sed` command consists of address followed by a command, delimited by a space
character. Let’s see few examples.

```text
$ cat file | sed '10 d'
```

This command will delete 10th line in the input file, meaning that we will see
all numbers but number 10.

In case you want to specify last line of the input file, you can use $ sign as
address specification. Following example will print numbers 1 through 19.

```text
$ cat file | sed '$ d'
```

### Complex addressing

You can specify a range of lines. To do this, you specify first line of the
range and the last one with comma in between.

```text
$ cat file | sed '1,9 d'
```

Will print lines 10 through 20. Next example on the other hand, will print lines
1 to 9.

```text
$ cat file | sed '10,$ d'
```

Now here’s something neat. You can also tell `sed` that address lines appear
starting line X every Y lines. To do this, you specify `X~Y` as an address.
Here’s an example.

```text
$ cat file | sed '1~2 d'
```

This will print the even numbers out of 1-20 range. On the contrary, following
command will print only the odd numbers.

```text
$ cat file | sed '0~2 d'
```

Finally, we can specify addresses using regular expressions. You can do this by
specifying regular expression in between two slash characters.

```text
$ cat file | sed '/^1./ d'
```

This command will delete all two character lines starting with 1. I.e. it will
print numbers 1-9 and 20. Here’s another regular expression example.

```text
$ cat file | sed '// d'
```

# Putting it all together

Last command that I would like to demonstrate you is `p` command. As you could
have guessed, it prints input line as is. There’s one caveat in using it. `sed`
will print the input line (or what may have left of it) anyway, so when telling
it to print the line it will do it twice. It is easy to overcome this problem is
using `-n` command line switch – remember I mentioned a command line switch that
I use from time to time, this is it:D

Let’s see few examples of the ‘p’ command in action.

```text
$ cat file | sed 'p'
```

As expected, this command will simply print every line of text twice. Let’s see
something more complex.

```text
$ cat file | sed -n '1,5 p'
```

In this command I used the addressing feature of `sed`. It will print all
numbers from 1 to 5. Finally, let’s try to put it all together.

```text
$ cat file | sed -n '/^.$/ d; /^2./ d; /^1./ s/1/2/; p'
```

What you see here is three `sed` commands in a row. First one deletes all lines
of text one character long. This will delete all numbers from 1 to 9. Next, it
deletes all two digit numbers that start with 2. This will delete number 20.
Finally, it searches for all two digit numbers starting from 1 and replaces 1
with 2. Eventually, we use `p` command to print the result. Last `p` command
needed only because we used `-n` command line switch. Eventually it will print
numbers 20 to 29.

Here’s another a slightly complex example, that does however exactly the same –
prints numbers 20 through 29.

```text
$ cat file | sed '1,9 d; $ d; s/1/2/g;'
```

This concludes this introductionary article on `sed`. Hope you found it
interesting. If you have further questions, drop me an
[email](mailto:alexander.sandler@gmail.com) or leave a comment here.
