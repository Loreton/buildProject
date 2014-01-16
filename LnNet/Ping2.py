#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys, commands
import re
import os
import time
import socket

# *******************************************************************************
# return True/False and Error/Status Message
# host='10.1.13.1'
# *******************************************************************************
def Ping(host):
    # LnLogger.console("[PING] - Pinging host: %s" % (host))
    LnLogger.console("Pinging %s" % (host), 'HCJ')
    report = ("No response","Partial Response","Alive")
    bRetVal = True
    sRetVal = None
    # ------------------------------------------------------------------------------
    # 2 packets transmitted, 0 received, +1 errors, 100% packet loss, time 0ms
    # 2 packets transmitted, 1 received, 50% packet loss, time 220ms
    # 2 packets transmitted, 0 received, 100% packet loss, time 1000ms
    # or
    # ping: unknown host 111.111.111.111
    # ------------------------------------------------------------------------------
    nPackets = 2
    if gOpSysName == 'nt':
        print "Windows Ping .................. not yet implemented"
        sys.exit(-100)

    cmd = 'ping -q -c%d %s | grep received' % (nPackets, host)
    (iCode, sCode) = commands.getstatusoutput(cmd)
    line = sCode.replace(',', ' ')
    token = tokenizeStrip(sCode, ' ')
    if token[3].isdigit():
        rcvdPckts = int(token[3])
    else:
        rcvdPckts = -1

    if rcvdPckts == nPackets:
        bRetVal = True
        sRetVal = report[rcvdPckts]
    elif rcvdPckts >= 0 and rcvdPckts < nPackets:
        bRetVal = False
        sRetVal = report[rcvdPckts]
    else:
        bRetVal = False
        sRetVal = sCode
        LnLogger.debug("Pinging host %s - %s" % (host, sCode))

    # LnLogger.console("[PING] - Ping Status: %s" % (sRetVal))
    LnLogger.console("%s" % (sRetVal), '')
    return bRetVal, sRetVal

