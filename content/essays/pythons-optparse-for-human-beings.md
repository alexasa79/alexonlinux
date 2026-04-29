---
title: "Python’s optparse for human beings"
date: "2009-04-29T10:23:17"
original_url: "http://www.alexonlinux.com/pythons-optparse-for-human-beings"
categories: ["Opinion", "Programming Articles"]
tags: ["command", "line", "modules", "options", "optparse", "programming", "python"]
---

# Introduction

This article extends `optparse`’s documentation. `optparse` is a Python module
that allows your program to easily parse command line options it receives. In
addition, it takes care of some of the very common tasks, such as handling `-h`
command line option.

`optparse` is one of those modules that are an absolutely must have for almost
every project. However, because we start new project so seldom, it is difficult
to remember all those recipes that we come up with, every time we add a new
command line option. This article is an attempt to bring together such recipes.

[optparse’s official
documentation](http://docs.python.org/library/optparse.html) lacks some very
important information. On the contrary to official documentation, in this
document I am trying to give you more hands-on kind of documentation. This
article is a cookbook of things that you do with `optparse` most often.

# What do we do with command line options

Every time we use `optparse`, we use it to do a number of things. Obviously we
want our program to support command line options. What varies is the type of
options we want to support. Some options doesn’t have additional arguments
(boolean options). Others are mandatory. Some require one or more arguments.
Finally, we may want options to depend on each other – i.e. we may want one
option to depend on presence of another.

These are most common things that we would like to implement, but there are
more. Lets try to build a list of all such functionalities that we may want to
implement.

- Support for a standalone command line options (boolean options). Support for
  mandatory (required) options. Support for options with one or more arguments.
  Default values for options. Dependency between options. Grouping of options in
  help screen. Customizing help screen.

However, before we dig into implementation details of each and every one of
these bullets, lets see the basics of using `optparse`.

# `optparse` Basics

No matter what you do with `optparse`, it all starts with importing `optparse`
and instantiating `OptionParser` class.

```python
import optparse
parser = optparse.OptionParser()
```

## Adding options

To add an option, we should use `OptionParser`’s method called `add_option()`.
It accepts a large number of parameters. For now, we will see only the most
basic. We will see more advanced parameters later in this article. Note that we
should call `add_option()` for every option that we would like our program to
support.

Obviously the most important parameter tells what command line option we would
like to support. Lets say that for sake of this article we would like our little
Python script to support -n command line option. Also, we would like -n to have
longer sibling –new. –new and -n would have the same meaning, but one is shorter
and the other longer and more verbose.

This is how we add these options.

```python
parser.add_option('-n', '--new')
```

Note that by all means this is not enough to be able to parse even simplest case
of command line options. This is only the basics.

## Specifying help string for an option

One more thing that is very common when using `optparse` is to give a short help
string that would tell user what this particular command line option does.
`optparse` will print this string if user runs your program with `-h`.

To specify such help string pass parameter named `help` to `add_option()`. Like
this:

```python
parser.add_option('-n', '--new', help='creates a new object')
```

## Telling `optparse` to parse arguments

Once we’ve added all the options we want our program to support, we should tell
`optparse` that it is time to do actual parsing. This is how we do it.

```python
(opts, args) = parser.parse_args()
```

`parse_args()` method returns a tuple of objects. First object, `opts`, contains
all values we’ve received via command line. We will learn how to use this later
in the article.

`args` is a list of words that contain everything that left after options that
parser recognizes. This is useful if you want your program to support indefinite
number of arguments – like in `cp` or `mv` Unix commands, where you specify
options first and then a long list of files to copy/move, followed by a
destination directory.

## Putting it together

This is how our script looks like so far.

```python
#!/usr/bin/python
import optparse
parser = optparse.OptionParser()
parser.add_option('-n', '--new', help='creates a new object')
(opts, args) = parser.parse_args()
```

Running it with -h command line option, would produce following result.

```text
alex ~/works/args -> ./args.py -h
Usage: args.py [options]
Options:
  -h, --help         show this help message and exit
  -n NEW, --new=NEW  creates a new object
alex ~/works/args ->
```

`args.py` is the name I had given to the script. Take this little nice help
screen. Note that we didn’t do a thing to make it appear. This is where power of
`optparse` begins.

# `optparse` Cookbook

What we saw until now were common things that you do with `optparse` to operate
it. No matter what options you would like your program to support and what are
relationships between the options, you have to instantiate `OptionParser` and
have to call `parse_args()` method.

However, few methods that we’ve seen so far, are useless by themselves. We use
them to do more specific things, which we will study in this section of the
article.

## Support for a standalone command line options

I call such options boolean options because eventually we want some boolean
variable to indicate if `optparse` saw the option or not.

For the sake of the demonstration, lets say we want our script to support -b
option. When this option is specified, we want some variable to be True. This is
how we do it.

```python
parser.add_option('-b', help='boolean option', dest='bool', \
    default=False, action='store_true')
(opts, args) = parser.parse_args()
```

Note three new named parameters that we’re passing to `add_option()`. `dest`
specifies the name of the variable that will hold True or False value once
`optparse` runs into `-b`. `default` specifies default value of the variable, in
case `optparse` doesn’t find `-b`. Finally `action` tells `optparse` what to do
when it runs into `-b`. `store_true` action tells `optparse` to place True value
into `bool` once it detects `-b`.

Additional action that we may want to use called `store_false`. It tells
`optparse` to set a value of `bool` to False. Note that when we use
`store_false`, we better change `default` value to something other than False –
otherwise you won’t be able to see the difference between when `-b` is there and
it is not.

Once `parse_args()` finishes, you can access the variable via `opts.bool`. You
can drop the default value of the variable. In this case, if you don’t specify
`-b` command line option, value of `opts.bool` will be `None`.

## Support for mandatory (required) options.

`optparse` itself doesn’t support mandatory options. As `optparse`’s
documentation states, mandatory options are a bad practice and should be
avoided. However, I think that at the end, it is your choice to make and modules
such as `optparse` should give you the tools to do things that you want to do.
This said, this is what I usually do to have a mandatory option.

For a single variable, just don’t set default value for it and check if
`opts.<variable name>` is `None`, after `opt_parse()`. Like this:

```python
parser.add_option('-m', help='mandatory option', dest='man',
    action='store_true')
(opts, args) = parser.parse_args()
if opts.man is None:
    print "A mandatory option is missing\n"
    parser.print_help()
    exit(-1)
```

Obviously, when a mandatory option is missing, we want to do something about it.
This can be anything of course, but most likely you want to tell about the
mistake and print a help message. This is exactly what happens in lines 7-9.

But what if you have multiple mandatory options? Well, we can do exactly the
same, but for several options. Lets have a look.

```python
parser.add_option('-m', help='mandatory option', dest='man',
    action='store_true')
parser.add_option('-p', help='mandatory option', dest='pan',
    action='store_true')
(opts, args) = parser.parse_args()
# Making sure all mandatory options appeared.
mandatories = ['man', 'pan']
for m in mandatories:
    if not opts.__dict__[m]:
        print "mandatory option is missing\n"
        parser.print_help()
        exit(-1)
```

Here, we have two mandatory options: -m and -p. In lines 9-14, I build a list of
all mandatory options (represented by their destination property name), run
through the list and see if any of them is None. If so, it prints an error
message, help message and returns.

## Support for options with one or more arguments

With `optparse` we can parse options with an argument and even several
arguments. This is how we do it.

```python
parser.add_option('-s', help='arguments', dest='opt_args', \
    action='store')
```

This example is somewhat different from what we’ve seen before. Here, use an
action named `store`. This action tells `optparse` to store option’s argument in
specified destination member of `opts`.

How about having an option with two or three arguments. It is doable as well.

```python
parser.add_option('-M', help='multiple arguments', dest='multi', \
    action='store', nargs=2)
```

As you can see, you can tell `optparse` how many arguments you want some option
to support. To do this, we pass `nargs` parameter to `add_option()`. Its default
value is 1. This is why we could omit it when we registered option with a single
argument. However, if we need two or more options, `nargs` is a must.

In this case `parse_args()` will place all arguments in a tuple. I.e. after we
run `parse_args()`, `opt.multi` will be a tuple containing all arguments that
user has passed to our program.

## Option destination types

By default, all members of `opts` object will be strings. I.e. when you specify
a destination for your argument, its type is string, by default. However, it
doesn’t have to be this way. You can change the type of the destination variable
for the argument by passing `add_option()` a parameter named `type`. Note that
default `type` is string. Despite you can always convert string into anything
you want, you can ask `optparse` to do it for you. This is how.

```python
parser.add_option('-s', help='arguments', dest='opt_args', \
    action='store', type='int', default=10)
parser.add_option('-M', help='multiple arguments', dest='multi', \
    action='store', nargs=2, type='string')
```

Here we’ve specified int type for -s and string type for -M. Note default value
of -s. It should be of the same type as option itself.

Also note `-M`. Although `optparse` turns two arguments into a tuple, it does
not support different types for several arguments. So, when an option has
multiple arguments, their type should be the same.

## Dependencies between options

As with mandatory options, `optparse` does not give you much help setting
dependencies between various options. If you still want to have some
relationship between options, you have to implement it manually, after
`parse_args()` is over.

Luckily this is not very difficult thing to do. Remember how we’ve implemented
mandatory options? We can do the same here.

```python
parser.add_option('-A', help='option A', dest='a',
    action='store_true')
parser.add_option('-B', help='option B', dest='b',
    action='store_true')
(opts, args) = parser.parse_args()
if opts.b and not opts.a:
    print "Option B requires option A\n"
    parser.print_help()
    exit(-1)
```

Here, option B requires option A. If B is there, but A is missing, script will
produce an error message, print help screen and exit.

## Help screen customizations

### Grouping options

`optparse` has a neat feature allowing you to group options. You can create as
many groups as you want. Each group will have a short description that would
appear on help screen. Also, you can use option groups to group options inside
of your program, making it easier to understand and more readable. This is how
you do it.

First, we create an option parser as we usually do.

```python
parser = optparse.OptionParser()
```

Next we create a new options group.

```python
group1 = optparse.OptionGroup(parser, 'Options group 1')
group2 = optparse.OptionGroup(parser, 'Options group 2')
```

Note that to create an option group, we have to specify parser that we will use
and a short description of the options in this option group. The description
will later appear in the help screen.

Now we should add the actual options. This time however, we add them to groups
instead of adding them to parser.

```python
group1.add_option('-t', help='group 1 option', dest='t', \
    action='store')
group2.add_option('-d', help='group 2 option', dest='d', \
    action='store')
```

`add_option()` method of class `OptionGroup` is exactly the same as
`add_option()` method of class `OptionParser`.

Finally, we add groups to parsers and call `parse_options()`.

```python
parser.add_option_group(group1)
parser.add_option_group(group2)
(args, opts) = parser.parse_args()
```

Now, lets have a look at the help screen.

```text
alex ~/works/args -> ./args.py -h
Usage: args.py [options]
Options:
  -h, --help  show this help message and exit
  Option group 1:
    -t T      group 1 option
  Option group 2:
    -d D      group 2 option
alex ~/works/args ->
```

See how -t and -d standout, each in its own group.

### Changing programs usage string

You can specify your own usage string. This is the first line of help screen.
You do this by passing `usage` parameter to `OptionParser` constructor.

```python
parser = optparse.OptionParser(usage='Usage: %prog <options>')
```

If we run this code, this is how our help screen would look like.

```text
alex ~/works/args --> ./args.py -h
Usage: args.py <options>
.
.
.
```

As you can see, you can use `%prog` mnemonics inside of usage string. It will be
substituted with the name of the program.

### Telling option’s default value

Another thing that you can do is specify default value of the option in its help
screen. To do that you can use `%default` mnemonics inside of help string of an
option. Like this:

```python
parser.add_option('-w', default='hello', dest='t', \
    action='store', help='this one has a default value [%default]')
```

This will make help line in help screen for this option to look like this:

-w T this one has a default value [hello]

### Better argument description

```python
parser.add_option('-s', help='single argument', dest='single', \
    action='store')
parser.add_option('-M', help='multiple arguments', dest='multi', \
    action='store', nargs=2)
```

Lets have a look at how the help screen would look like for two options above.

```text
  -s SINGLE          single argument
  -M MULTI           multiple arguments
```

Not a pretty sight. See how `optparse` described parameters that each option
receives. In fact, `optparse` take this description from name of the destination
argument. To generate such description, it converts its name into a string and
changes it to upper case.

This may somewhat work for an option that receives one argument. But it
certainly will not work for an option that receives mutliple arguments, such as
`-M`. Luckily, there’s a solution for this problem. `add_option()` receives a
parameter named `metavar`. It tells `optparse` how to describe option argument
in help screen. So, instead of calling `add_option()` the way we did it for `-s`
and `-M`, we should call it this way:

```python
parser.add_option('-s', help='single argument', dest='single', \
    action='store', metavar='<ARG>')
parser.add_option('-M', help='multiple arguments', dest='multi', \
    action='store', metavar='<ARG1> <ARG2>', nargs=2)
```

This makes the help message for these two options look like this:

```text
  -s <ARG>           single argument
  -M <ARG1> <ARG2>   multiple arguments
```

Now this is much better.

### Adding program description

You can have a description of what your program does. When having it, it will
appear in help screen between usage line and options description. To do that,
pass `description` argument to `OptionParser` constructor, when creating
`OptionParser` object. Like this:

```python
desc="""This is a description of %prog. optparse uses Python's
textwrap module to format the text, so
don't
bother
adding
new
line
characters, as optparse will prettify your description in
its own way."""
parser = optparse.OptionParser(description=desc)
parser.add_option('-s', help='single argument', dest='single', \
    action='store')
(args, opts) = parser.parse_args()
```

Running this little program with -h, will produce following help screen.

```text
alex ~/works/args --> ./args.py -h
Usage: args.py [options]
This is a description of args.py. optparse uses Python's  textwrap
module to format the text, so  don't  bother  adding  new  line
characters, as optparse will prettify your description in its own
way.
Options:
  -h, --help  show this help message and exit
  -s SINGLE   single argument
alex ~/works/args -->
```

Note how `optparse` reformatted the description string. It uses Python’s
textwrap module to format your description, producing nice, 80 character long
lines of text.

Also note that as with `usage` parameter, you can use `%prog` mnemonics here. It
will be substituted with name of your program.

### Adding epilog

Epilog will appear after options description. To specify epilog, pass `epilog`
parameter to `OptionParser`’s constructor. Note that as with description string,
`optparse` will prettify the text you use with textwrap.

## Program version string

Like help screen, `optparse` can also generate version string, responding to
`--version` option. Unlike with help screen where `optparse` did most of the
job, here `optparse` merely prints what you’ve specified as version string.

To specify version string, pass `version` parameter to `OptionParser`’s
constructor. You can use `%prog` mnemonics inside of version string. Here’s an
example.

```python
parser = optparse.OptionParser(version='%prog version 1.0')
(args, opts) = parser.parse_args()
```

Running this script with –version option, produces following result.

```text
alex ~/works/args --> ./args.py --version
args.py version 1.0
alex ~/works/args -->
```

`optparse` produce version string only if you run it with `--version` option. If
you want to your program to print its version with `-v` option, you will have to
add `-v` option manually and then call `print_version()` method of
`OptionParser`, to produce the version string.

# Conclusion

There is a bunch of other things that you can do with `optparse`. You can have
your own actions, your own formatter – an object that formats the help screen.
You can use callbacks that get called when `optparse` runs into certain option.
However, I think I’ve covered 99.9% of what you may need. In case I missed
something, send me an email to
[alexander.sandler@gmail.com](mailto:alexander.sandler@gmail.com).
