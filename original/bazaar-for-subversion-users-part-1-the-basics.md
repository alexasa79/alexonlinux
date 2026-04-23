---
title: "Bazaar for subversion users, part 1 – the basics"
type: "post"
created_at: "2009-06-23T17:06:01"
original_url: "http://www.alexonlinux.com/bazaar-for-subversion-users-part-1-the-basics"
categories: ["Programming Articles", "Reviews"]
tags: ["bazaar", "branch", "open source", "repository", "subversion", "VCS"]
---

# Table of contents

[Introduction to the series](#introduction_to_the_series)
[Introduction to the article](#introduction_to_the_article)
[Way of working with Bazaar](#way_of_working_with_bazaar)
[Demo setup description](#demo_setup_description)
[Directory and user configuration](#directory_and_user_configuration)
[The basics](#the_basics)
[Creating a project](#creating_a_project)
[Checking-out the project](#checking-out_the_project)
[Adding files to the project](#adding_files_to_the_project)
[Committing files](#committing_files)
[Few words about revision numbers in Bazaar](#few_words_about_revision_numbers_in_bazaar)
[Local commits or offline commits](#local_commits_or_offline_commits)
[Committing local commits to remote branch](#committing_local_commits_to_remote_branch)
[Multi-user environment](#multi-user_environment)
[Making modifications to files and viewing differences](#making_modifications_to_files_and_viewing_differences)
[Committing non-up-to-date file](#committing_non-up-to-date_file)
[Merging with the latest version of the file](#merging_with_the_latest_version_of_the_file)

# Introduction to the series [BACK TO TOC](#table_of_contents)

This series of articles continues a subject that I started [in one of my previous posts](distributed-vs-centralized-version-control-systems). Due to reasons I’ll describe in a second, Subversion doesn’t work for me anymore. I have a bunch of one developer projects that I would like to manage. My version control server (Subversion server at the moment) is on the Internet, works over HTTP. Because of that, it is slow. So slow, that it made me crying for a new version control.

Working with Subversion is still fun. If you’re working in an environment where all project participants are close to each other, then it is still my VCS of choice. This is because Subversion is a mature VCS with great community supporting it – this translates into excellent clients for various OSs, great support, etc.

Yet today more and more projects operate in a distributed manner. This is especially true for open source projects, where project participants often live in various countries. This is also true for people like me – those who prefer to keep their repository online from high availability considerations.

This series of articles is a summary of things that I had to learn to know Bazaar and to convert some of my projects from Subversion.

## Introduction to the article [BACK TO TOC](#table_of_contents)

This is the first out of several articles that I plan to conduct on the subject. In this article we will see the basics. Material I present here is introductory. It should be enough to get you started and as you will advance more articles will arrive.

# Way of working with Bazaar [BACK TO TOC](#table_of_contents)

There are to ways of working with Bazaar.

- Purely distributed
- Semi-centralized

First means that there’s no central repository. Every user works in his own repository and repositories can be easily merged. Moreover, the entire concept of branch and repository has been put together. Meaning that there are no repositories per se anymore. Each branch is a repository and a repository is a branch.

Semi-centralized approach means that repositories kept on remote computer and we checkout the repository – just like in Subversion.

The major difference between the two is that in the first case we checkout a repository that sits on our computer, usually in the same directory as the repository (more on this later in the series). In the later case, we have to checkout the remote repository.

This article intended for Subversion users and because of that I will concentrate on a second approach. Despite that, once you’ll understand the concepts behind all this, you will be able to work both ways.

# Demo setup description [BACK TO TOC](#table_of_contents)

For the sake of the demonstration, I prepared two Ubuntu Jaunty (that is Ubuntu 9.04) computers. First named*hubuntu*. This is our server computer – this is where I’ll keep the main repository. Second computer called*shmubuntu*. This is the client computer.

## Directory and user configuration [BACK TO TOC](#table_of_contents)

Repository files on*hubuntu*, the server computer should have dedicated place and an owner user. For that reason I created a user named*bzr*. Then I created directory*/srv/bzr*and*chown*‘d the directory to the user. Finally, I created two more directories:*/srv/bzr/trunk*and*/srv/bzr/branches*.*trunk*directory is for the main repository.*branches*directory is for branches. This is exactly like it is in Subversion.

Then, I installed Bazaar on both computers. In case you’re wondering, on Ubuntu, you can do it with:

```text
alex@hubuntu:~$ sudo aptitude install bzr
```

Next, I created two users*user1*and*user2*on*shmubuntu*. These are the users that will do the job.

Finally, I installed*user1*‘s and*user2*‘s identity on*bzr@hubuntu*. I did it because*bzr*on*hubuntu*owns the repository. We want*user1*and*user2*to be able to modify the repository files. To do that we should either add*user1*and*user2*on*hubuntu*and configure permissions or to make sure that*user1*and*user2*work on*hubuntu*as*bzr*, the user that owns the repository. The later seems to be much easier to do.

# The basics [BACK TO TOC](#table_of_contents)

## Creating a project [BACK TO TOC](#table_of_contents)

It all starts with creating a project. Lets say our*user1*logged into*shmubuntu*wants to create a new project and place the repository for the project on*hubuntu*. Here is what*user1*should do.

```text
user1@shmubuntu:~$ bzr init sftp://bzr@hubuntu/srv/bzr/trunk/project1
```

There are couple of interesting things about this command. First of all,*init*creates a new repository. What you should specify is a directory where you want it. By the way, directory should not exist. If it exists, Bazaar will complain about it. Otherwise, it will create the directory automatically for you.

If we want to work in a truly distributed manner, we create the repository in a local directory. But since we work in a centralized manner, we create the repository on a remote computer.

When creating local repository, the directory name should be plain Unix path. For remote it should be standard URI. The protocol in the URI can be either*sftp*for*scp*like protocol, or*ftp*. Other commands also accept*http*as a protocol, but in Bazaar it is read-only protocol. Since we actually want to write something to the repository,*http*won’t work for us.

Finally, note that we’ve created a repository named*project1*under*trunk*directory. If you go to that directory on the server, the only thing you’ll find there is a directory named*.bzr*. This is where Bazaar keeps its meta-data. Unlike Subversion that keeps*.svn*in every directory under the project, Bazaar has its*.bzr*only under root directory of the project. This way it stands less in your way when, for instance, packaging the project.

## Checking-out the project [BACK TO TOC](#table_of_contents)

Check-out is plain and simple.

```text
user1@shmubuntu:~$ cd works/
user1@shmubuntu:~/works$ ls
user1@shmubuntu:~/works$ bzr co sftp://bzr@hubuntu/srv/bzr/trunk/project1
user1@shmubuntu:~/works$ ls
project1/
user1@shmubuntu:~/works$
```

As you can see, its just like in Subversion. There are couple of things to notice here:

1. Note that I checked-out the project as user*bzr*on server’s side. This is because this is the user that has write permissions on repository files and we will need write it when we will commit.
2. Bazaar creates the project directory for us, just like it did when we created the project.

Note that*co*is an alias to*checkout*. So, the command could be*bzr checkout*.

## Adding files to the project [BACK TO TOC](#table_of_contents)

This one is also exactly like in Subversion. For the sake of the demonstration I created a small C project, with one source file and a small library in a separate directory. All compiled with single Makefile.

```text
user1@shmubuntu:~/works$ cd project1/
user1@shmubuntu:~/works/project1$ ls
Makefile  main.c  some/
user1@shmubuntu:~/works/project1$ bzr add
adding Makefile
adding main.c
adding some
adding some/some.c
adding some/some.h
user1@shmubuntu:~/works/project1$
```

Like in Subversion, this doesn’t mean the files are in repository. To actually add the files into repository we’ll have to commit them.

## Committing files [BACK TO TOC](#table_of_contents)

This is also, exactly like in Subversion.

```text
user1@shmubuntu:~/works/project1$ bzr ci -m 'initial commit - added project files'
Committing to: sftp://bzr@hubuntu/srv/bzr/trunk/project1/
added Makefile
added main.c
added some
added some/some.c
added some/some.h
Committed revision 1.
user1@shmubuntu:~/works/project1$
```

*ci*is an alias to*commit*. -m command line switch tells Bazaar to append a message to the commit. Without -m, Bazaar will open default editor asking you to write a message in the editor.

**

### Few words about revision numbers in Bazaar [BACK TO TOC](#table_of_contents)

In Bazaar each repository has a current revision number. Each time you commit, the revision number moves forward by one. You can identify state of your revision by its revision number. This means that like in Subversion, you can checkout certain version of the project using revision number. Branch revision numbers are different. We’ll talk about this later in the series.

## Local commits or offline commits [BACK TO TOC](#table_of_contents)

We’ve already seen how to commit directly into repository, but how this solves the performance issue with the centralized VCS ? After all, if all Bazaar is able to do is to commit into a repository on remote host, how is it faster then Subversion for that matter?

The point is that Bazaar allows you do so called local commits. We’ll talk about this in greater detail in the next part of this series of articles. In the meantime, I would like to introduce you to the topic.

As unusual as it might be, there is almost no difference between your local, checked-out, copy of the project and the remote repository. I.e. what you have on your hard drive after checking out the project, is the entire repository. Actually, you can let other people to check-out your copy of the project.

As a matter of fact, the term repository does not exist in Bazaar. Instead of repositories there are*branches*. Checked-out branch or a*checkout*is just a branch of a special kind. What’s important to understand now is that you can actually commit into Bazaar’s*checkout*, without committing to original branch that we’ve checked out.

To do a local commit, append –local command line switch to the commit command. Like this:

```text
user1@shmubuntu:~/works/project1$ bzr ci --local -m 'did another change'
Committing to: /home/user1/works/project1/
modified main.c
Committed revision 6.
user1@shmubuntu:~/works/project1$
```

This command will not transmit a thing over the net. Instead it will save all the changes locally.

### Committing local commits to remote branch [BACK TO TOC](#table_of_contents)

At some point in time, we will probably want to*commit*our local commits into the main branch. Unfortunately, Bazaar won’t let us do it straightforwardly. Instead it will ask us to*update*first. This is a little annoying as there’s no obvious reason for this – actually there’s an [open bug on this in Bazaar’s launchpad page](https://bugs.launchpad.net/bzr/+bug/139549). Anyway, here is what we have to do:

```text
user1@shmubuntu:~/works/project1$ bzr update
 M  main.c
All changes applied successfully.
 M  main.c
All changes applied successfully.
Updated to revision 6.
Your local commits will now show as pending merges with 'bzr status', and can be committed with 'bzr commit'.
user1@shmubuntu:~/works/project1$
```

And then:

```text
user1@shmubuntu:~/works/project1$ bzr ci -m "June 30'th 2009 daily commit"
Committing to: sftp://bzr@hubuntu/srv/bzr/trunk/project1/                                                                                   
modified main.c
Committed revision 7.                                                                                                                       
user1@shmubuntu:~/works/project1$
```

Note the comment I’ve left on the*commit*. This is actually a cool idea – that is to do all commits locally and do daily*commit*to main repository using cron task. This way we can do commits fast, without waiting for slow internet.

# Multi-user environment [BACK TO TOC](#table_of_contents)

## Making modifications to files and viewing differences [BACK TO TOC](#table_of_contents)

### Committing non-up-to-date file [BACK TO TOC](#table_of_contents)

Now it is time to engage*user2*. Lets say that*user2*has changed one of the project files and committed it – file named*main.c*in our case.*user1*has changed that file too and now wants to commit his change. So, first we have:

```text
user2@shmubuntu:~/works/project1$ bzr ci -m 'added include to string.h'
Committing to: sftp://bzr@hubuntu/srv/bzr/trunk/project1/
modified main.c
Committed revision 3.
user2@shmubuntu:~/works/project1$
```

And then we have:

```text
user1@shmubuntu:~/works/project1$ bzr ci -m 'a couple of minor changes'
bzr: ERROR: Bound branch BzrBranch6('file:///home/user1/works/project1/') is out of date with master branch BzrBranch6('sftp://bzr@hubuntu/srv/bzr/trunk/project1/').
To commit to master branch, run update and then commit.
You can also pass --local to commit to continue working disconnected.
user1@shmubuntu:~/works/project1$
```

Here, Bazaar behaves exactly like Subversion. As you remember, Subversion won’t let your commit to overwrite a file that has been changed in repository. I.e. if repository contains newer version of the file, Subversion will ask you to update first. This is exactly what Bazaar has asked us to do.

### Merging with the latest version of the file [BACK TO TOC](#table_of_contents)

Since our*user1*ran into a conflict, he has to update his local repository first. We already saw this command in action:

```text
user1@shmubuntu:~/works/project1$ bzr update
M  main.c
All changes applied successfully.
Updated to revision 3.
user1@shmubuntu:~/works/project1$
```

Note that update will overwrite user1’s changes. On the contrary, Bazaar will try to merge the changes. If it succeeds, like it did in our example, then you’ll have to commit the file. Like this:

```text
user1@shmubuntu:~/works/project1$ bzr ci -m 'a couple of minor changes'
Committing to: sftp://bzr@hubuntu/srv/bzr/trunk/project1/
modified main.c
Committed revision 4.
user1@shmubuntu:~/works/project1$
```

Here, Bazaar again behaves exactly like Subversion. It does update the file as long as this update doesn’t break anything. But what if there’s a conflict? This, and many other things you will find in the second part of this article series, which comes in a couple of days. Stay tuned.
