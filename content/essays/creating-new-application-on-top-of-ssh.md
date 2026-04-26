---
title: "Creating new application on top of SSH"
date: "2009-03-23T15:03:16"
original_url: "http://www.alexonlinux.com/creating-new-application-on-top-of-ssh"
categories: ["Programming Articles"]
tags: ["code", "encryption", "programming", "scp", "security", "shell", "ssh", "tcp"]
---

# Introduction

As you know, you can use SSH for two things. First, there’s a remote access. You
can get access to a command line on a remote computer. Second use is for
transferring files. OpenSSH suite comes with a handy tool called `scp` which
allows you to copy files to and from a remote computer over SSH. Files being
transferred securely, without exposing their content to someone who may be
sniffing our traffic. And of course there’s a WinSCP program that does the same
on Windows.

For a long period of time I thought that this is it. OpenSSH comes sewed with
two major features: remote access (`ssh`) and file transfer (`scp`). Adding a
custom feature would require deep understanding of SSH and security, I thought.
Apparently I was wrong. It appears that creating a new application that uses SSH
as a communication channel is as easy as a pie. Read on.

# How `scp` works

## You can run commands on a remote computer using `ssh`

One of the neat features of `ssh` is that it allows you to run commands on a
remote computer. To do this, type in `ssh` command with its arguments as if you
were connecting to a remote computer and append to it the command you would like
to run. Like this:

```text
alex ~/works/ssh -> ssh alex@192.168.1.67 df
```

This would run `df` on a remote computer – 192.168.1.67 in our case. Here’s
something important. The output of `df` command will be transferred over SSH to
our computer and we will see it as if we were running the command on our local
computer.

Same thing will occur if we will run command that requires input on a remote
computer. We will type in the arguments here, on our local computer,
and `ssh` will transmit the input over encrypted with SSH channel to the remote
computer and feed it to the commands running on the remote computer, as if the
input was received from a keyboard on a remote computer. Take a look at the
example session that demonstrates this:

```text
alex ~ -> ssh alex@192.168.1.67 'read var; echo ${var} > file.txt'
alex@192.168.1.67's password:
hello world
alex ~ -> ssh alex@192.168.1.67 ls
alex@192.168.1.67's password:
file.txt 
alex ~ -> ssh alex@192.168.1.67 cat file.txt
alex@192.168.1.67's password:
hello world
alex ~ -> ssh alex@192.168.1.67 rm -f file.txt
alex@192.168.1.67's password:
alex ~/works/ssh ->
```

First command that I’ve entered reads a line of text and saves it in shell
variable `var`. Then it writes the content of the variable into file named
file.txt. Second command shows that file.txt was indeed created. Third command
shows the content of the file: “hello world” in our case. Finally, the last
command deletes the file.

Note that all these commands, their input and output being transferred over SSH,
i.e. being encrypted.

## Back to `scp`

Apparently, there’s nothing magical about `scp`. It does not encrypt files before
transferring them. In fact it knows nothing about encryption. This is how it
works.

It uses `ssh` to invoke an instance of itself on a remote computer. To let itself
know that it is a remote instance, it uses two undocumented command line
switches, -f and -t. Then it uses special protocol to communicate with a remote
instance of itself. The communication protocol and the actual data, all being
transferred over SSH. To make it happen, it uses `ssh`‘ input/output streams as a
transport for sending and receiving data to/from remote computer.

Simple isn’t it? In fact, creating an application that runs on top of SSH and
transfers and receives encrypted data, seems to be easier than even creating
TCP/IP client-server with sockets. Lets try creating our own application.

# Creating our own SSH based application

## The idea

Actually, transferring files to a remote computer is a very demonstrative
example. So, I will demonstrate an application that sends a file to a remote
computer and remote computer saves it on its local disk. I’ve written it in
python because it is simpler for me, but you may write it in any programming
language. The principles I’ve been using here, which I will explain later in the
article, are universal and can be used with any programming language.

As with `scp`, I’ve created only one program. It has two modes of operation. When
invoked without command line arguments, it assumes it is a local instance that
should transmit the data. When invoked with command line switch -r, it assumes
it is a remote copy and receives data saving it in file.

Lets see the code.

## The code

```python
#!/usr/bin/python
import os
import sys
import popen2
def BeRemote():
    print "Being remote"
    f = open('/home/alex/works/ssh/data2.dat', 'w+b')
    for s in sys.stdin:
        f.write(s)
    f.close()
def BeLocal():
    print "Being local"
    child = popen2.Popen3('ssh alex@localhost' +
        '/home/alex/works/ssh/ssh_client.py -r')
    f = open('data.dat', 'rb')
    for s in f:
        child.tochild.write(s)
    f.close()
    # Shutting down remote client.
    # By closing its stdin, we're causing it to exit
    # its main loop.
    child.tochild.close()
    child.wait()
if len(sys.argv) > 1 and sys.argv[1] == '-r':
    BeRemote()
else:
    BeLocal()
```

## Discussion

The code starts in line 28 with checking if it has been invoked with command
line switches. If it sees -r command line switch, it runs `BeRemote()` function.
Otherwise it runs `BeLocal()` function.

`BeRemote()` is rather simple function. It creates a file named `data2.dat` in
directory `/home/alex/works/ssh/` (this is where I’ve been developing this project
on my computer). Then it enters a loop where it writes everything it reads from
standard input into the file (lines 10-11). It will continue saving the data as
long as its standard input is open. Once it will be closed, it will close the
file and exit (line 12).

`BeLocal()` is a little more complex. First it spawns `ssh` connecting
to `localhost` with username `alex`. Now I know that it is expected to connect to a
remote computer, but for the sake of demonstration lets pretend
that `localhost` is a remote computer. It tells `ssh` to run program
named `ssh_client.py` with -r command line switch. `ssh_client.py` is the name of
the script, so in essence it runs itself. -r switch tells it to run in remote
mode, that is receiving mode.

It uses popen2 python module to spawn the `ssh` process. This is similar to
using `popen()` function in C. Basically, it runs a process, opens pipe and
redirects process’s input and output through the pipe. Our program sits on the
other end of the pipe and uses it to transmit the data over SSH.

Next, the function opens the file (`data.dat`) we want to transmit and sends it
through the pipe (lines 18-21).

Final step is more interesting. It has to tell `BeRemote()` when it has reached
end of file. This could be done with a special communication protocol between
remote and local instances of the program – this is what `scp` does. I did
something simlier. Instead of notifying remote that it has reached end of file,
I simply close one side of the pipe (line 25). This causes remote side to think
it has reached end of file and exit. At the same time, local side waits until
remote side will exit (line 26) and then exits itself.

## Demonstration

Lets see our little python script in action.

```text
alex ~/works/ssh -> ls -la
total 3836
drwxr-xr-x 2 alex alex    4096 2009-03-22 22:36 ./
drwxr-xr-x 6 alex alex    4096 2009-03-22 00:46 ../
-rw-r--r-- 1 alex alex 4000000 2009-03-22 01:28 data.dat
-rwxr-xr-x 1 alex alex     578 2009-03-22 22:36 ssh_client.py*
alex ~/works/ssh -> ./ssh_client.py
Being local
alex@localhost's password:
alex ~/works/ssh -> ls -la
total 7836
drwxr-xr-x 2 alex alex    4096 2009-03-22 22:36 ./
drwxr-xr-x 6 alex alex    4096 2009-03-22 00:46 ../
-rw-r--r-- 1 alex alex 4000000 2009-03-22 22:36 data2.dat
-rw-r--r-- 1 alex alex 4000000 2009-03-22 01:28 data.dat
-rwxr-xr-x 1 alex alex     578 2009-03-22 22:36 ssh_client.py*
alex ~/works/ssh -> md5sum data.dat
2e02ecd84be565fa22216e8398ff9b63  data.dat
alex ~/works/ssh -> md5sum data2.dat
2e02ecd84be565fa22216e8398ff9b63  data2.dat
alex ~/works/ssh ->
```

First I do `ls -la` to demonstrate that I have only two files in current directory
– the data file `data.dat` and the script. Next I ran `./ssh_client.py`. It tells
us that it is a local side and asks us for a password. Actually, the password
request comes from `ssh`. To avoid being asked for password, you can use identity
files as I explained in my [SSH crash
course]({{< relref "essays/ssh-crash-course.md" >}}).

Then, it transfers the file and exits. After it exits I did `ls -la` once again
and it clearly showed that we now have a new file named `data2.dat`. We can see
that its size is the same as `data.dat` size. Later I confirmed that this is
indeed the same file with md5sum.

# Conclusion

We saw how easy it is to create encrypted communication channel using SSH
and `ssh`. I hope you’ve found this article useful and interesting. In case you
have any questions, don’t hesitate to contact me at alexander.sandler@gmail.com.
