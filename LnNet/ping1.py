#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# 2012-10-10    -   Aggiunto TIMEOUT parameter

import subprocess
import shlex

def ping(host):
    print "Pinging...", host
    command_line = "ping -c 1 " + host
    args = shlex.split(command_line)

    try:
        subprocess.check_call(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        print "Website is there."
        return 0

    except subprocess.CalledProcessError:
        print "Couldn't get a ping."
        return 1


if __name__ == "__main__":
    rCode = ping('www.google.com1')
    print rCode
    rCode = ping('www.google.com')
    print rCode
