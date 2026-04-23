---
title: "g15dods"
type: "post"
created_at: "2007-12-23T01:40:51"
original_url: "http://www.alexonlinux.com/g15dods"
categories: ["Resources"]
tags: ["day of defeat", "day of defeat source", "dod", "dods", "g15", "lcd screen", "logitech", "source"]
---

# Intro

Ok. This is a G15 Applet for DOD:S page – the g15dod page.

- G15 is a Logitech’s keyboard with additional LCD screen. Screen can be used for wide range of purposes, among them, viewing ingame information and stats.
- DOD:S is a Day Of Defeat Source game.

Here you’ll find info about g15dods, installation instructions, revision history, etc…

# Download

### Current Version

Current version is 0.2.6. You can download it [http://www.alexonlinux.com/wp-content/uploads/2008/01/g15dod-setup-026.exe](http://www.alexonlinux.com/wp-content/uploads/2008/01/g15dod-setup-026.exe)[here](http://www.alexonlinux.com/wp-content/uploads/2008/01/g15dod-setup-026.exe).

### Previous Versions

You can download version 0.2.5 from [here](http://www.alexonlinux.com/wp-content/uploads/2008/01/g15dod-setup-025.exe) and version 0.2 from [here](http://www.alexonlinux.com/wp-content/uploads/2008/01/g15dod-setup-02.exe).

# What’s new

### What’s new in this version

1. Several people complained about different issues related to inability to detect Steam installation directory and/or username. In this version, I rewrote the whole installation directory/username detection mechanism. It should be much better now.Special thanks to**Mike Olsen**from [echovoice](http://www.g15forums.com/forum/showthread.php?t=1811) for helping me with this!!!
2. This version automatically detects when you switch between steam accounts.

### What’s in version 0.2.5

1. You no longer have to specify DOD:S installation directory. Application detects it automatically.

### What’s in version 0.2

Couple of things.

1. You can now see network traffic info and CPU/MEM usage info. You can switch between these two using buttons (see buttons section below).
2. You can now reset totals and todays stats using keyboard buttons (again, see Buttons section below).
3. Fixed couple of bugs, such as, you no longer can run several instances of the application at the same time:-)
4. Added a lot of message boxes in case there is an error.

# Preview

![g15dods screen shot](http://www.alexonlinux.com/wp-content/uploads/2008/01/g15dod.jpg)

# Installation

Just run the setup and it will tell you what to do.

Make sure to add “-condebug” parameter to Day Of Defeat: Source launch options (open Steam, goto My Games, right click on Day Of Defeat: Source, enter properties, press “Set launch options” button and write -condebug). This option causes DOD:S to write console log to file. Later, g15dods uses the information written to this file to generate stats.

# Uninstalling

Go to your All Programs menu, then to g15dods and press uninstall. Then, you will know what to do:-)

# Documentation

### Usage

As you can see, applet shows two panes on the screen. Right pane shows game stats. Left pane shows some info that might be useful during the game – current time (!!!) and network stats.

The game stats are:

1. Your total number of kills and deaths.
2. Number of kills and deaths since you started the app (basically, since you started the computer).
3. Number of kills and number of seconds elapsed since from the last you were killed.

When not playing, game stats are hidden.

### Configuration dialog

Configuration dialog allows you to reset the stats and to change the DOD:S installation directory. Open configuration dialog, run Logitech LCD manager, choose “G15 DOD:S Applet” from the list and press configure button.

In configuration dialog, no matter what changes you made, always press the OK button to apply. Otherwise, the application will ignore your changes.

As you can guess, setting the “Reset Totals” and “Reset Todays” check boxes, will reset your stats (either totals, todays or both) – but only after pressing the OK button:-D

### Buttons

Starting version 0.2 of the application, you can do few nice things with keyboard buttons under the screen.

First (leftmost) button can be used to switch between Network traffic information and CPU/MEM usage information.

Holding down third and fourth buttons for two seconds (and more) will reset total kills and deaths stats and todays kills and deaths respectively.

# Known issues

1. It may complain about some missing DLLs. In case it does, let me know and I’ll help you to solve this problem.
2. Sometimes, it shows negative netwok traffic values.
3. You name it8-)
