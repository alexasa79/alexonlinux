---
title: "SSH crash course"
date: "2009-03-17T19:07:06"
original_url: "http://www.alexonlinux.com/ssh-crash-course"
categories: ["System Administrator Articles"]
tags: ["linux", "open", "protocol", "scp", "security", "session", "ssh", "telnet"]
---

## About this article

I would like to do two things in this article. First I would like to tell you
about SSH. How to make it work. How to use public key cryptography to login to a
remote computer. How to execute remote commands and copy files to/from a remote
machine.

On the other hand, I would like this document to be a sort of reference guide
document. For that reason, I provide a list of links to various places in the
document, that show you how to do actual stuff without too much talking around.

You can read the document from beginning to the end or you can jump to a place
that you need right away.

Here are the jump to links.

# Introduction

Some years ago, when I realized that telnet is out and SSH is in, I was mostly
confused about SSH. I heart that it allows you to login to a remote machine
without username and password. Yet when I heart people talking about all those
cryptography keys I was definite not to get into it. It seemed too complicated
for me. So I used it same way as I used telnet before it – with username and
password.

What I really needed is a document that describes all those nifty things that
you can do with SSH, in simple words. Without getting into too many technical
details, yet explaining enough out of it, to turn SSH into useful and handy tool
instead of a hostile thing that only gurus know how to operate.

Years passed and as I myself learned how to use SSH, including some of its more
advanced features, I decided to write such a document.

Although all information I present in this document is available on the
internet, I think I managed to assemble here things that you need the most.

# Part 1. Basics

## Intro

I believe all Linux distributions today come with command line SSH client,
called `ssh`. We should distinguish between two things here. First, there is SSH
the protocol. But also, there is `ssh`, the program that speaks SSH protocol.
`ssh` is part of larger OpenSSH suite. OpenSSH is what most of the people have.

## Connecting to remote host – simple case

Simplest case is when you want to connect to a remote computer using same
username as you used to login to your current account. For example, lets say you
are logged in on a computer named A and your username is `alex`. You want to
connect to computer B. This is what you type in:

```text
$ ssh B
```

Instead of hostname (B), you can use an IP address of course. Unless configured
otherwise, `ssh` will ask you to provide a password for the user – `alex` in our
case. Once you type in correct password and hit enter, you will find yourself
logged into computer B as user `alex`.

> There might be additional step in between. `ssh` may ask you to confirm
> authenticity of the remote host. Usually it happens first time you connect.
> `ssh` will present you something called RSA/DSA host fingerprint and will ask
> you whether you like it or not – yes or no. For now answer yes, but make sure
> to read about this later in this section of the article.

Let me assume you will not always use same username when connecting from one
host to another (not to mention that it is unlikely that you will use username
`alex`). To tell `ssh` what username to use when connecting to a remote
computer, use `<username>@<hostname>` notation. Like this:

```text
$ ssh alex@B
```

or like this:

```text
$ ssh john@192.168.1.1
```

### RSA/DSA host fingerprint

One of the most important features of SSH protocol is security. This means
obviously encrypting the data that passes between your computer and a remote
computer, but not only. Another thing that embedded into SSH is taking care that
you are connecting to right computer. To explain this, I have to introduce a
villain.

> Villain is a guy who tries to break into our computer or perhaps sniff our
> traffic attempting to steal some valuable information. He can try to replace
> parts of information that fly between two connected computers to tempt us to
> expose some valuable information. He can even try to replace a remote computer
> to make it look like a real thing, while we are feeding it with valuable
> information. In two words, villain is a bad guy and we try to protect
> ourselves with SSH.

As I said, villain can try to replace remote computer. To make sure that it
didn’t happen, we want to know for sure what computer we’re connecting to. For
this reason, during its installation, OpenSSH suite creates a signature of the
computer. This signature called RSA or DSA host fingerprint.

> RSA and DSA are two methods of encrypting data. SSH supports both of them and
> any of them can be used. Differences between two are less important. On my
> Ubuntu system, RSA is the default, but I guess it can be different. Fow now,
> what is important is to see what method we’re using. I’ll tell you a little
> later what for.

When you’re connecting to a remote computer for the first time, its host
fingerprint being saved on your machine. Actually, first `ssh` asks you if the
signature it received from a remote computer is right. You can rely on `ssh` to
do things right, but you can actually check and make sure that the fingerprint
is right. If you have an access to a remote computer some other than via SSH,
you can read its fingerprint and compare it to value `ssh` has given to you.

To read host fingerprint use following command:

```text
$ ssh-keygen -l -f /etc/ssh/ssh_host_rsa_key.pub
2048 96:72:48:4f:69:70:45:b2:39:3d:55:75:78:52:ce:a7 /etc/ssh/ssh_host_rsa_key.pub (RSA)
$ ssh-keygen -l -f /etc/ssh/ssh_host_dsa_key.pub
1024 17:bd:cd:fb:09:82:9b:70:36:3f:b5:a4:4e:f4:84:d9 /etc/ssh/ssh_host_dsa_key.pub (DSA)
```

First command returns RSA fingerprint. Second command returns DSA fingerprint.
You can use these fingerprints to make sure that you’re connecting to a right
computer.

### What happens when host fingerprint changes

First lets try to understand why this may happen. First option is the villain
case that we’ve already mentioned. In this case we should go to police, etc. But
this is not the only case. Host fingerprint can change if, for instance, someone
has reinstalled the operating system on the computer. Another option is when
computer’s IP address has changed, but we still connect to the same IP address
which is by now already taken by other computer. In any of these cases host
fingerprint of the remote computer changes. Lets see what `ssh` will tell us
when this happens.

```text
$ ssh alex@192.168.1.1
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that the RSA host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
96:72:48:4f:69:70:45:b2:39:3d:55:75:78:52:ce:a7.
Please contact your system administrator.
Add correct host key in /home/alex/.ssh/known_hosts to get rid of this message.
Offending key in /home/alex/.ssh/known_hosts:1
RSA host key for localhost has changed and you have requested strict checking.
Host key verification failed.
```

It is big and slightly overwhelming, but at least you won’t miss it:-)

### How to handle expected host fingerprint change

Often you do something to a remote computer that may cause its host fingerprint
to change. For instance, you could have reinstalled operating system on a remote
computer. In this case it is totally normal that `ssh` throws that big and scary
error message on us. Yet it won’t let us to connect to a remote system and we
want to fix this.

`ssh` saves host fingerprints on a local disk, in a file named
`/home/<username>/.ssh/known_hosts`. What we want to do is to delete certain
host from the file and by that cause `ssh` to confirm host fingerprint with us
again, as if we were connecting for the first time.

To do this, we will use following command:

```text
$ ssh-keygen -R 192.168.1.1
/home/alex/.ssh/known_hosts updated.
Original contents retained as /home/alex/.ssh/known_hosts.old
```

Obviously, change 192.168.1.1 to either hostname or IP address or a hostname of
remote computer you’re connecting to.

As you can see, the above command deletes localy saved remote host fingerprint
from `known_hosts` file, but keeps a backup copy of the file (`known_hosts.old`)
in case we need it. In case you want to restore `known_hosts` file, you can
simply copy a backup file overwriting the original one.

Also, note that `known_hosts` file sits in your home directory. Meaning that if
you log into different user account, `ssh` will start saving remote host
fingerprints from scratch.

## Executing command on a remote computer

It is as simple as connecting to a remote computer. All you have to do is to
append a command you want to execute on a remote computer to `ssh` command that
we’ve used to connect to the computer. For example:

```text
$ ssh alex@192.168.1.1 ls
```

This will run `ls` command on computer 192.168.1.1, in `alex`’s home directory.

This way you can run almost any command on a remote computer. But keep in mind
one thing. You may want to put command that you want to run on a remote computer
in single quotes – shell does not expand commands in single quotes. Take a look
at the following example:

```text
$ ssh alex@192.168.1.1 echo "Hello World" > file.txt
```

This command obviously writes something to a file named `file.txt`, but on what
computer? In this particular case, shell will interpret `>` character and will
write output of `ssh` command to a file named `file.txt`. But this is not we
wanted. So to make sure that shell will not interfere us, we will put the
command in single quotes. Like this:

```text
$ ssh alex@192.168.1.1 'echo "Hello World" > file.txt'
```

In case you want to put a single quote in the actual command, this is how you
can do it:

```text
$ ssh alex@192.168.1.1 'echo '"'"'Hello World'"'"' > file.txt'
```

To make it easier for you to understand number of quotes let me split the
command into several pieces to make it more readable.

```text
'echo '
"'"
'Hello World'
"'"
' > file.txt'
```

Note that to put single quotes into final command, I first close single quote
I’ve opened, then put single quote in between double quotes.

## Securely copying files to and from a remote computer

`scp` is part of OpenSSH suite. It is the command used to copy files from/to a
remote computer. In terms of security it works same way as `ssh`. I.e. it is
host fingerprint aware and will ask you to confirm a fingerprint once you access
some host for the first time.

On the other hand it works same way as `cp`. With `scp` like with regular `cp`
you copy a file from one place to another. Also, as with `cp` you can copy
several files into one location.

The syntax is the same as with `cp`. First you specify what to copy, then you
specify where to copy. The difference is however that you can specify a remote
host using special notation that I will show you a little later.

`scp` uses following notation to specify remote files and directories:
`[username@]<hostname>:<directory|file>`. I.e. first you type username followed
by `@`, then you type hostname and finally you enter colon followed by
file/directory name. As with `ssh`, username (`@` included) part is optional and
if omitted `scp` will use username you’ve logged in with. Let’s see few
examples:

```text
$ scp alex@alexandersandler.net:/home/alex/wav.wav .
```

Here I am copying file named `sample.wav` located in home directory of user
`alex` on `alexandersandler.net` host, to my current directory. But wait a
second, wouldn’t it be easier to do it this way:

```text
$ scp alex@alexandersandler.net:~/wav.wav .
```

It appears that `scp` has absolutely no problem to understand `~` instead of
user’s home directory, exactly like in shell does.

### Copying multiple files

```text
$ scp alex@alexandersandler.net:~/works/project/* .
```

This will copy all files from directory `/home/alex/works/project/` on
`alexandersandler.net` to my current directory. Note that `scp` has no problem
with wildcards. Note that as with `cp`, the wildcard is not recursive. I.e. it
will copy all files from `/home/alex/works/project/` directory, but will not
copy its sub-directories.

Here’s another example.

```text
$ scp ~/works/another_project/* alex@alexandersandler.net:~/tmp/
```

In this example, we copy all files from `~/works/another_project/` directory on
our computer to `alexandersandler.net`. Again, the operation is not recursive.
But what if we want it to be recursive? Here comes the first difference between
`cp` and `scp`. With `cp` you use `-R` command line switch. With `scp` you use
`-r` command line switch. Like this:

```text
$ scp -r ~/works/another_project/* alex@alexandersandler.net:~/tmp/
```

Talking about command line switches, here’s another `scp` command line switch
that I use a lot. `-C` tells `scp` to compress the data before sending it.
Depending on content of the files you’re transferring, this can make `scp` much
faster. Here’s an example that demonstrates how to use it.

```text
$ scp -C -r ~/works/last_project/* john@alexandersandler.net:~/works/last_project/
```

Like I already mentioned, `scp` uses same security mechanism as `ssh`. All files
transferred are encrypted and when using `scp` for the first time, like with
`ssh` it will ask you to confirm a host fingerprint. Then it will ask for a
password, exactly as `ssh` does.

# Part 2. Encryption

## Login without entering password?

Oh yes. Actually its quite simple. To make this work, we will have to create and
install so called identity file. You may also heart it being referred as
public/private key or certificate. Don’t these terms to scare you. It is very
simple. Keep reading.

## How modern cryptography works

### What are keys

Computers use pair of keys to encrypt messages they sent between each other.
Each key is a sequence of numbers. It can contain as many as thousands of
numbers, or just a few of them.

These keys are tricky. Once you encrypt something with one key, you can only
decrypt it with its pair key. I.e. if you encrypt a message with key A, you can
only decrypt it with key B. There is no difference between the keys. I.e. if you
encrypt with key A, you can decrypt with key B and if you encrypt with key B,
you can decrypt with key A.

I won’t get into details of how keys get generated and how computers encrypt
messages keys. There are several ways of doing this and it usually involve
complex mathematical transformations. In case you’re still curious, remember
those RSA and DSA things? These are algorythms that computer use to generate
keys and encrypt messages using those keys. You can find more information about
each one of them on wikipedia.

### Public/private key

Remember that we need two keys to encrypt/decrypt messages. In computers,
usually one of them called private key and the other called public key. This is
because computer sends public key to whoever asks for it, making it publicly
available. Private key, on the other hand, kept in secret. But why computers
send public keys away? Doesn’t it negate whole idea of secrecy?

### How actual encryption works

Remember a villain guy I mentioned? In addition to replacing a computer we’re
connecting to, villain can do two additional things to steal information from
us. First villain can try to decrypt messages we send to another computer.
Second, villain may be unable to decrypt the messages, but he may try to
intercept them and replace the data with his own. This can cause remote computer
to expose valuable information.

Lets see how key cryptography prevents these two problems. Lets say we have two
computers – computer A and computer B. Each one of them has a pair of keys – the
public and the private key.

Secure session between them begins with key exchange. Each computer sends its
public key to another computer. Then, to send private information from computer
A to computer B, computer A does this:

1. Encrypts the message with his own private key.
2. Encrypts the result of step 1, with B’s public key.

2nd step makes sure that even if villain intercepts the message, he won’t be
able to decrypt it because he doesn’t have B’s private key – message was
encrypted with B’s public key, so to decrypt it we need B’s private key.

1st step makes sure that villain won’t be able to replace a message with his
own. He can get B’s public key because, well, it is public, but it cannot
encrypt the message with A’s private key because it is private to A. Computer B
on the other hand has A’s public key, so it can decrypt messages encrypted with
A’s private key.

This scheme is indeed amazing and it works for making the Internet secure. But
lets get back to SSH.

## SSH identities

In SSH, a pair of public/private keys called identity. Keys usually kept in two
files. First file contains only the public key. Second file contains both public
and private keys. In case you’re wondering why SSH developers have chosen to
keep both private and public keys together, it is just more convenient this way.
We send public key away so we better have it separate and ready for use. On the
other hand, private key is a secret key. It is useless without public key. Then
why not to put public key into private key file, to allow us to restore public
key from private key file in future? And what if we want to copy private key?
Handling one file is lot easier.

### How to generate identity files

OpenSSH suite comes with a program named `ssh-keygen`. It generates identity
files. This is how you run it.

```text
$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/alex/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/alex/.ssh/id_rsa.
Your public key has been saved in /home/alex/.ssh/id_rsa.pub.
The key fingerprint is:
77:d1:f8:78:31:03:ec:d9:e8:55:58:9a:d7:b2:4d:ef alex@alexandersandler.net
The key's randomart image is:
+--[ RSA 2048]----+
|           ..  o.|
|            .+.oo|
|           .o+O.+|
|            ++oX.|
|        S ..o.+ o|
|         . ... . |
|                E|
|                 |
|                 |
+-----------------+
```

As with `known_hosts` file, identity files kept in `/home/<username>/.ssh`
directory. Names of the files are `id_rsa` and `id_rsa.pub` for private key and
public key files respectively. These files include RSA identity. For DSA, file
names are `id_dsa` and `id_dsa.pub`. If you have slightly older version of
OpenSSH suite, you may have files named `identity` and `identity.pub`. These are
SSH protocol version 1 identity files.

Note that while we’re generating identity files, we are asked for a password.
This allows us to protect the session to a remote computer with both identity
file and a password. We’ll talk about this in a minute. Now, lets see how to use
your identity files.

### How to install identity file

Before I explain how to do install identity files on remote computer, let me say
few words about why to do it. Once you’ve identity file installed, `ssh` will no
longer authenticate you with a password. Instead it will use your identity
files. Now if you’ve supplied a password, when `ssh-keygen` asked you for it,
`ssh` will still ask you for that password.

Using a password when generating identity files basically gives you an option to
have stronger security then regular username/password pair. This way, you’re
protecting yourself with both identity files (you’re the only guy who has them)
and a password.

If you’ve specified blank password, it will let you in, without asking further
questions. I.e. you can use identity files to login to a remote computer,
without supplying a password and if you’re using same username then even without
supplying a username. Just type in `ssh <hostname>` and you’re in.

Note that when you’re installing identity files, you’re basically giving your
public key to a remote host. Yet you keep your private key file secret and don’t
give it to anyone. This is exactly the same process I have mentioned in the *How
actual encryption works* section of this article.

Now to the actual installation. Modern versions of OpenSSH come with nifty
script called `ssh-copy-id`. It will copy identity file (your public key) from
home directory on your current computer (`/home/<user>/.ssh/id_rsa.pub`), to a
remote computer. Let’s see it in action.

```text
$ ssh-copy-id alex@192.168.1.1
```

`ssh-copy-id` will ask you for a password as `ssh` would, but once you’ve
entered the password, you will no longer have to do it again (unless your
identity files protected with password). Note that `ssh-copy-id` has some
requirements. When running it, you should already have identity files under your
user account. Also, your identity files shouldn’t be installed on the host
you’re connecting to, for user you’re connecting with. You can install your
identity files under several different user accounts on remote computer.

There is something that may not be entierly clear to you just yet. I am talking
about the correlation between identity files and user accounts on both local and
remote computer. To understand it, we should learn how to install identity files
manually.

### Installing identity files manually

`ssh-copy-id` may not be installed on your system. Or it may produce an error
message and we wouldn’t know where it came from. To address these issues we have
to understand identity files installation process.

Actually its quiet simple. First of all you have to understand that identity
files located in your user’s home directory. Meaning that even if you’ve
installed `alex`’s identity on some remote computer, you won’t be able to login
to that computer when locally you’re logged in as john. This is because when
`ssh` tries to authenticate you on a remote system, it looks for identity files
(private key) in your home directory.

Second, `ssh` saves installed identity files (public keys) under
`/home/<user>/.ssh/authorized_keys` file. Again this is a home directory of the
user account you’re trying to log into and if you try logging into different
account, `ssh` will ignore identity files you’ve installed originally.

Identity file installation involves one simple step – copying content
`id_rsa.pub` (or `id_dsa.pub`) file on local computer into `authorized_keys`
file on remote computer. Content of identity files is usually single line of
text. You should copy it as such. If you add a line break symbol in the middle,
`ssh` will not recognize this identity. Moreover, it may break other identities,
so be very careful when modifying `authorized_keys` file. Luckily, if you make a
mistake, you can always fix it later.

Lets have a look at a session that demonstrates entire process of generating
identity files and installing them on remote computer, manually. I am logged
into computer named `alexandersandler.net` as `alex` and trying to log into
`192.168.1.1`, again, as `alex`.

```text
$ ssh-keygen
Generating public/private rsa key pair.
Enter file in which to save the key (/home/alex/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/alex/.ssh/id_rsa.
Your public key has been saved in /home/alex/.ssh/id_rsa.pub.
The key fingerprint is:
03:e3:7f:03:fa:e9:c6:01:85:12:f7:a4:38:36:19:cd alex@alexandersandler.net
The key's randomart image is:
+--[ RSA 2048]----+
|      .....      |
|      .+.o       |
|      +.E o      |
|     . * o .     |
|      B S .      |
|     . = * .     |
|      . + *      |
|       . o .     |
|                 |
+-----------------+
$ cat ~/.ssh/id_rsa.pub
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAqgfxOyV0SiQrF+7qq9lOjPvJsacWagHo3LDnv
5n/ZWnZzvTXHk/gZNL2VoUqnaEuf4P/9apepvIVlLrwoUt6x2goGnErvchhn2Tf/MoHNHQ0px
10EYxYfcFfyRs1w/8i/uM1ySnnTv+fbjdKSFMJeqYKhsTeY06p2f7i+QpJVOMQ68ccaY10wj0
fP4wS6AR/6jXfCWeiOtRWZiZ1amf+w1HPIYxN5iLhDpcEK07eC/0GhBnqOcWgi9okHDxEY0nP
bKjsmnA7Lg4yBNCVbDIAx/zdMADTKtskH9gOrX+NJmLQSx4NEq802s6FP1YazaInhDQ9syQ2t
+HihmQPwCKETw== alex@alexandersandler.net
```

This is our public key, or identity. Lets copy the key to clipboard, connect to
remote computer, 192.168.1.1 in our case, and install the identity.

```text
$ ssh alex@192.168.1.1
The authenticity of host '192.168.1.1 (192.168.1.1)' can't be established.
RSA key fingerprint is 96:72:48:4f:69:70:45:b2:39:3d:55:75:78:52:ce:a7.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '192.168.1.1' (RSA) to the list of known hosts.
alex@192.168.1.1's password:
Linux 192.168.1.1 2.6.24.3 #1 SMP Thu Apr 10 11:20:13 EDT 2008 x86_64
The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.
To access official Ubuntu documentation, please visit:
http://help.ubuntu.com/
You have new mail.
Last login: Mon Mar  9 10:16:50 2009 from alexandersandler.net
```

Note that this is the first time I am connecting to this computer, so I was
asked to confirm host fingerprint and asked for a password. Well, the truth is
that this is not the first time I am connecting to this computer. I just made
things look like this is the first time;-)

```text
alex@localhost:~$ echo 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAqgfxOyV0SiQrF
+7qq9lOjPvJsacWagHo3LDnv5n/ZWnZzvTXHk/gZNL2VoUqnaEuf4P/9apepvIVlLrwoUt6x2
goGnErvchhn2Tf/MoHNHQ0px10EYxYfcFfyRs1w/8i/uM1ySnnTv+fbjdKSFMJeqYKhsTeY06
p2f7i+QpJVOMQ68ccaY10wj0fP4wS6AR/6jXfCWeiOtRWZiZ1amf+w1HPIYxN5iLhDpcEK07e
C/0GhBnqOcWgi9okHDxEY0nPbKjsmnA7Lg4yBNCVbDIAx/zdMADTKtskH9gOrX+NJmLQSx4NE
q802s6FP1YazaInhDQ9syQ2t+HihmQPwCKETw== alex@alexandersandler.net'
>> ~/.ssh/authorized_keys
alex@localhost:~$ exit
```

Now we have key installed and it is time to see it in action. Lets try
connecting to the machine again.

```text
$ ssh alex@192.168.1.1
Linux 192.168.1.1 2.6.24.3 #1 SMP Thu Apr 10 11:20:13 EDT 2008 x86_64
The programs included with the Ubuntu system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.
Ubuntu comes with ABSOLUTELY NO WARRANTY, to the extent permitted by
applicable law.
To access official Ubuntu documentation, please visit:
http://help.ubuntu.com/
You have new mail.
Last login: Mon Mar  9 10:16:50 2009 from alexandersandler.net
alex@localhost:~$
```

Note that `ssh` didn’t ask us to provide password. It works!

# Part 3. Advanced SSH

## X forwarding

### Introduction

You may already know this or may not, but X Windows server (the one that you use
to have graphical user interface in Linux) allows you to present a UI for a
program on a remote computer. Actually, this is the reason why it is called
X**server**. X Windows server is a server because it gives programs a way to
present their user interfaces. X Server serves programs. Actual programs on the
other hand are X Windows clients. They use X Windows server to present
themselves on screen.

You may be wondering what it is useful for and I won’t blame you. The truth is
that it may become exceptionally handy in certain situations. Imagine yourself
connecting to a certain computer using telnet or SSH. As you know, both telnet
and SSH allow you to run textual shell. Sometimes it suffices, sometimes it
doesn’t. What if text only shell is not enough?

This is when the server function of the X Windows server becomes handy. If you
have a X Windows server on a computer that you directly work with, you can tell
programs on your remote computer to use X Windows server on your local computer
and present themselves on your local computer. I.e. you type in `xterm` inside
of your telnet or SSH session, while connected to a remote computer, and `xterm`
window appears right in front of you, on your local computer, despite the actual
program runs on a remote computer miles away. Every command you type in the
`xterm` being executed on a remote computer, but you work with it as if it was
running on your computer.

### Remote X Windows server configuration

You don’t want to allow just any program to present itself on your computer. If
access to your X Windows server was completely open, someone could try to catch
a moment when you run firefox and run firefox of his own, on his own computer,
but on your screen. This could make you think that you’re working with program
that runs locally, while it actually runs on a remote computer. When something
like this happens, every piece of information you type into your browser is
available to the villain. Including your browsing history and even your
passwords.

Obviously access to X Windows server has to be closed by default and it is.
Formerly, two programs controlled who can use your X Windows server: `xauth` and
`xhost`. There are however, two problems with these two. First of all using them
is inconvenient. To present remote application on your local X Windows server
you had to run two commands with quiet complex syntax every session. You could
make the configuration persistent, but then you had to do it yourself. It was
automatically done for you.

Another problem is lack of security. X Windows server uses protocol named XDMCP.
It is insecure. As a result someone who has access to your traffic could watch
you browsing the internet.

### How SSH fixes the situation

If you run `ssh` with `-Y` command line switch, `ssh` will automatically
configure X Windows forwarding to your local X Windows server. This means that
when you run `ssh` with `-Y` switch, every command or program that has UI, will
present itself on your X Windows server computer, rather than on remote
computer. No need to run `xhost` and `xauth`. `ssh` does this for you.

#### What if -Y doesn’t work

Both SSH client and SSH server has an option to enable/disable -Y command line
switch. Moreover, by default OpenSSH ships with -Y disabled, meaning that you
won’t be Hable to use this command line switch out of the box. Luckily, most of
Linux distributors enable this option in OpenSSH configuration files. However,
there is a slight chance that your Linux distribution has strict security
settings and keeps X forwarding disabled.

If this is the case, we will have to enable X forwarding. To see how, read next
section of this article.

## Configuration

In this section, I would like to cover few of the most useful OpenSSH
configuration options.

### Allowing login as root

Perhaps one of the first things that I needed with SSH is to allow me to login
as root. Before you allow this, bare in mind that this is a bad practice.
Working as root is generally a bad idea even if you are developing drivers for
Linux – something that very root access.

To allow root access, we have to tell SSH server to accept such connections. To
do this, we have to modify SSH server’s configuration file and tell `sshd`
(that’s the name of SSH server program) to reread it’s configuration. SSH server
configuration file is `/etc/ssh/sshd_config`. Note that to modify the file you
will need root access.

Option that controls root access called `PermitRootLogin`. To allow root login,
simply append:

```text
PermitRootLogin yes
```

to the end of the file.

Once done we have to tell `sshd` to reload configuration. Strictly speaking this
is distribution dependant, but the command you have to run most likely looks
like this:

```text
/etc/init.d/sshd reload
```

or

```text
/etc/init.d/ssh reload
```

First variance works on OpenSuSE. Second works on Ubuntu.

### X forwarding

We’ve seen how to enable X Windows forwarding with -Y command line switch. But
how about doing this automatically? This is doable. Another thing that you may
want to do is to disable X forwarding. Again, this is doable.

To enable X forwarding automatically, you have to modify `ssh`’ configuration
file `/etc/ssh/ssh_config` and append `ForwardX11Trusted` directive. Like this:

```text
ForwardX11Trusted yes
```

No need to reload anything. Once you save the file, `ssh` will automatically
imply `-Y` on every new connection.

On the other hand, to prohibit clients from using -Y, we should remove
X11Forwarding directive from /etc/ssh/sshd_config. OpenSSH disables this option
by default, but many Linux distributors enable it. So, if X forwarding works for
you, this means that there’s “X11Forwarding yes” line somewhere in
/etc/ssh/sshd_config.

### Other options

There are very nice manual pages for both `/etc/ssh/ssh_config` and
`/etc/ssh/sshd_config` files named `ssh_config` and `sshd_config` respectively.
Both manual pages include documentation for all `ssh` and `sshd` options that
are available.

# Conclusion

I hope you’ve found this article useful. In case you have further questions,
don’t hesitate to send them to me. My email is alexander.sandler@gmail.com.
