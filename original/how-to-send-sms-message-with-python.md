---
title: "How to send SMS message with Python"
type: "post"
created_at: "2009-04-02T13:51:08"
original_url: "http://www.alexonlinux.com/how-to-send-sms-message-with-python"
categories: ["Programming Articles", "Short articles"]
tags: ["message", "python", "sms", "web interface"]
---

I can’t beleive all the things that you can do with Python. Obviously, whatever you can do with Python, you can do with a whole bunch of programming languages out there. What I am really impressed with, is the ease.

Few weeks ago I was looking for a way to programatically send myself SMS on certain occasions. I was (and still) developing a system that would check for certain conditions on a server and alert me when something is wrong.

Eventually, I came up with a Python script,**40 lines**long:-) Note that you have to pay for the messages, but thats just few pennies. I bet there’s a way to plug into ICQ’s protocol and send SMS for free, but I don’t think you can do this with only 40 lines of code.

Here is the idea. There are firms on the internet, that provide service called SMS gateway. These firms has special devices plugged into GSM network on one end and has some programmable interface on the other end.

Here’s what you do. You open an account with such a firm. Then you either pay for one message or buy some credits and then spend them by sending messages.

SMS gateway I used called [world-text](http://www.world-text.com). Please, by all means I have nothing to do with these guys. I found them on the internet, just as you would.

There are couple of nice things about this particular company, although I bet if you spend some time researching you will find a better and probably cheaper one.

I don’t think there’s a standard for SMS gateways. Each company does something of its own. World-text provide web based gateway and this is what makes it so easy to use with Python.

Python code that I’ve written, simply sends properly formatted HTTP request to their web interface. Here’s the code.

```text
#!/usr/bin/python

import sys
import time
import glob
import httplib
import urllib

recepients = []

recepients.append("-------------")

world_text_username = "your@email.com"
world_text_password = "your password"

def usage():
    print "alertme.py <message to send>"
    sys.exit(0)

def send_sms(msg):
    global recepients, world_text_username, world_text_password

    print "Asked to send sms: %s" % msg

    for r in recepients:
        params = ""
        params = params + "username=" + world_text_username
        params = params + "&password=" + world_text_password
        params = params + "&" + urllib.urlencode({'message': msg})
        params = params + "&sourceaddr=SMSAlert"
        params = params + "&mobile=" + r
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn = httplib.HTTPConnection("sms.world-text.com:1081")
        conn.request("POST", "/sendsms", params, headers)
        conn.close();

if len(sys.argv) != 2:
    usage()

send_sms(sys.argv[1])
```

To use the script, just append your phone number, including country and regional code to the recepients list – make sure to delete the “———-” from it. Next change*world_text_username*and*world_text_password*to something meaningful and you are ready to bombard yourself with SMS messages:-)

In case you have further questions, email me at [alex@alexonlinux.com](mailto:alex@alexonlinux.com).

Have fun!:D
