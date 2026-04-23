---
title: "Distributed vs. centralized version control systems"
type: "post"
created_at: "2009-06-16T21:26:33"
original_url: "http://www.alexonlinux.com/distributed-vs-centralized-version-control-systems"
categories: ["Blog", "Opinion"]
tags: ["bazaar", "kernel", "subversion", "version control system"]
---

When*git*appeared for the first time, I was convinced that I don’t need it. It seemed that*git*is good for large and distributed projects, like kernel. While my own needs where much more modest – manage a project with couple of dozen files and perhaps a couple of contributors at most.

Couple of years passed and I am now looking into [Bazaar](http://bazaar-vcs.org/). This is a relatively new distributed version control system. I think I’ll write more about Bazaar, but in the meantime, I’d like to share some thoughts that crossed my mind while I was playing with it.

There’s one thing that distributed version control does much better then centralized version control. Let me explain.

We do commits for two reasons.

1. We want our work backed-up. We commit to repository because we know that repositories being backed up.
2. We want to be able to track our work, i.e. keep a record of changes that we apply to the project.

In centralized version control system, these two are integrated in one system. I.e. if you want to track your changes, you commit. If you want to backup your code, again, you commit.

Don’t know how about you, but for me, this is totally broken. I work on a small projects, usually from home. I prefer not to host Subversion server on one of my home computers, but rather have a small VPS system for this purpose. It has mirrored disks, so the data is safe, more or less.

The problem is that this setup is horribly slow. It uses web front-end, so it creates a new secure connection to the server for every file I commit. This is so frustrating. I bet Subversion has faster front-ends, but I doubt they will be fast enough.

On the other hand, with distributed version control, the two above items are separated. When you commit for code tracking purposes, you commit to your local repository. When you want to backup your code, you commit to centralized, backed-up repository. In the first case, you can commit as often as you want – do local commits, in Bazaar terms. In the later case, you can commit to the repository, lets say, nightly.

So, despite distributed version control systems naturally fit large projects, my mini-projects can enjoy them as well. Hence I am definitely going to try Bazaar with one of my mini-projects and report the results. Stay tuned.
