---
title: "Recursively deleting symbolic link and what it points to"
type: "post"
created_at: "2010-02-01T10:52:59"
original_url: "http://www.alexonlinux.com/recursively-deleting-symbolic-link-and-what-it-points-to"
categories: ["Articles", "Code library", "Programming Articles", "Short articles"]
tags: []
---

Recently I looked for a solution to this little problem. how do you, programmatically, delete a symbolic link and a file that it points to?

One problem that you should take care of when tackling this problem, is that symbolic link can point to a symbolic link. Then symbolic link should also point to symbolic link. And once again, and again and again…

So what can we do about it? First, lets start with*lstat*() system all. It will tell us is the file we’re interested in, is actually a symbolic link. To be more precise,*st_mode*field in*struct stat*will have flag S_IFLNK if specified file is a symbolic link. Note that it should be*lstat*() and not*stat*() – the later will return information about file the link points to and not about the link.

Next step is to call*readlink*(). This system call returns name of the file pointed to by specified symbolic link.

Finally, you should repeat the process recursively, for the pointed to file. Here is the code that does it:

```text
int recursive_deleter(const char* filename)
{
  struct stat st;
  char buffer[1024];

  if (lstat(filename, &st)) {
    perror("stat");
    return -1;
  }     

  if (st.st_mode & S_IFLNK == S_IFLNK) {
    memset(buffer, 0, sizeof(buffer));
    if (readlink(filename, buffer, sizeof(buffer)) < 0) {
      perror("readlink");
      return -1;
    }           

    printf("File %s is a symbolic link to %s\n", filename, buffer);

    if (recursive_deleter(buffer))
      return 0;
  }     

  printf("Deleting %s\n", filename);

  if (unlink(filename)) {
    perror("unlink");
    return -1;
  }     

  return 0;
}
```

Have fun!
