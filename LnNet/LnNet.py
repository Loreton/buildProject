#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys, commands
import re
import os
import time
import socket

import LnLogger
# from LnLogger import linePADLen
from   GlobalVariables import *           # Variabili Globali del progetto
from  LnMixed import tokenizeStrip         


# *******************************************************************************
# return Physical Status
# *******************************************************************************
def interfaceStatus(interfaceName):
    # LnLogger.console("[%s] - Checking interface" % (interfaceName))
    LnLogger.console("Interface %s" % (interfaceName), 'HCJ')
    if  interfaceName == None:
        LnLogger.error("Request for STRANGE (None) interface has been issued!!!!")
        return None

    (iCode, sCode) = commands.getstatusoutput('ifconfig -a')
    sCode = sCode.splitlines()
    status = None
    ifName = ''

    if (iCode == 0):
        for line in sCode:
            data = line.strip()

                # intercettiamo la riga con il nome scheda
                # eth0      Link encap:Ethernet  HWaddr 00:06:5B:FD:C6:CD
            if (data.find('Link encap:') > 0):
                appoStr = data.split(' ', 1)
                if appoStr[0] == interfaceName.lower():
                    ifName = appoStr[0]

                # Status dell0interfaccia
            elif (data.find('MTU:')>0 and ifName != ''):
                appoStr = data.split(' ')
                if appoStr[0] == 'UP':
                    status = 'UP'
                else:
                    status = 'DOWN'
                break

    # LnLogger.console("[%s] - Status   interface: %s" % (interfaceName, status))
    LnLogger.console("%s" % (status), '')
    return status

# *******************************************************************************
# *******************************************************************************
def GetConfig(interfaceName):
    LnLogger.console("reading network configuration using ifconfig command")
    command = 'ifconfig %s' %(interfaceName)
    (iCode, sCode) = commands.getstatusoutput(command)
    sCode = sCode.splitlines()
    sCode.append('dummy line')             # per sicurezza
    currCard = None

    if (iCode == 0):
        for line in sCode:
            data = line.strip()
            # print data

                # intercettiamo la riga con il nome scheda      <eth0      Link encap:Ethernet  HWaddr 00:06:5B:FD:C6:CD>
            if data.find('encap:') > 0 :
                appoStr = data.split(' ', 1)
                currCard = appoStr[0]
                # print currCard

                # intercettiamo l'indirizzo IP                  <inet addr:10.1.13.34  Bcast:10.1.13.255  Mask:255.255.255.0>
            elif (data.startswith('inet addr:') and currCard != ''):
                appoStr = data.replace(':', ' ')
                appoStr = appoStr.split(' ', 3)
                currCard += ' ' + appoStr[2]
                # print currCard

            elif (data.find('MTU:')>0 and currCard != ''):
                appoStr = data.split(' ')
                if appoStr[0] == 'UP':
                    currCard += ' UP'
                else:
                    currCard += ' Down'

            else:
                if (len(data) < 1) and (currCard != ''):           # end of interface or output
                    LnLogger.info(currCard)
                    currCard = ''
                    print 'dummy'


        return currCard


# def resolveDNS(host):
# ----------------------------------------------------
# - return:
# -      False, 'unknown', 'unknown'
# -      True, IPAddr, hostName
# ----------------------------------------------------
def DNSresolve(host):
    IPAddr = None
    hostName = None
    bRetVal = True
    LnLogger.info("trying to resolve host [%s] " % (host) )

    if validateIPAddr(host) == True:
        try:
            hostName = socket.gethostbyaddr(host)[0]
        except socket.herror, e:
            LnLogger.warning("1.ERROR resolving Address : %s --> [%d] - %s" % (host, e[0], e[1]))
            bRetVal = False
        except socket.gaierror, e:
            LnLogger.warning("2.ERROR resolving Address : %s --> [%d] - %s" % (host, e[0], e[1]))
            bRetVal = False

        # if bRetVal == True:
            # try:
                # IPAddr = socket.gethostbyname(hostName)
            # except socket.gaierror, e:
                # LnLogger.warning("3.ERROR resolving host name: %s --> [%d] - %s" % (hostName, e[0], e[1]))
                # bRetVal = False
    else:
        try:
            IPAddr   = socket.gethostbyname(host)
        except socket.gaierror, e:
            LnLogger.warning("4.ERROR resolving host name: %s --> [%d] - %s" % (host, e[0], e[1]))
            bRetVal = False

        if bRetVal == True:
            try:
                hostName = socket.gethostbyaddr(IPAddr)[0]
            except socket.herror, e:
                LnLogger.warning("5.ERROR resolving Address: %s --> [%d] - %s" % (IPAddr, e[0], e[1]))
                bRetVal = False



    if  bRetVal == True:
        LnLogger.info("host [%s] has been resolved in %s - %s" % (host, hostName, IPAddr) )

    return bRetVal, IPAddr, hostName




# *******************************************************************************
# *******************************************************************************
def validateIPAddr(address):

    if not (re.search('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(|\/\d{1,2})$', address)):
        return False

      # remove IPMask
    if (address.count('/') == 1):
        (ip, mask) = address.split('/')
        if not (0 <= int(mask) <= 32):
            return False
    else:
        ip = address

    for octet in ip.split('.'):
        if not (0 <= int(octet) <= 255):
            return False

    return True



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


# *******************************************************************************
# return False if interface is DOWN
# return True  if interface is UP
# *******************************************************************************
def stopInterface(interface, IPAddr, TIMEOUT=5):
    LnLogger.console("[%s] - Stopping interface" % (interface))
    bRetVal = False
    sRetVal = None

    # ----- check if exists ----------
    status = interfaceStatus(interface)
    # cmd = 'ifconfig -a | grep %s' % (interface)
    # (iCode, sCode) = commands.getstatusoutput(cmd)
    # LnLogger.debug("[%s] - iCode:%d sCode:%s" % (cmd, iCode, sCode))
    if  (status != 'UP'):
        sRetVal = 'Interface %s is down' % (interface)
        LnLogger.info('Interface %s is down' % (interface))
        return True, sRetVal

    # ----- executing STOP command ----------
    cmd = 'ifconfig %s down' % (interface)
    (iCode, sCode) = commands.getstatusoutput(cmd)
    LnLogger.debug("command:[%s] - iCode:%d sCode:%s" % (cmd, iCode, sCode))
    
    # ----- WAIT for STOP execution ----------
    while(TIMEOUT>0):
        LnLogger.debug("Waiting for a while.... Stopping interface [%s: %s]" % (interface, IPAddr))
        time.sleep(1)
        (bCode, sCode) = Ping(IPAddr)
        if sCode.lower() == 'no response':  # non deve rispondere al Ping
            break
        TIMEOUT -= 1

    if TIMEOUT > 0:
        sRetVal = 'Interface %s is down' % (interface)
        LnLogger.info(sRetVal)
        bRetVal = True
    else:
        sRetVal = 'Cannot stop Interface %s' % (interface)
        LnLogger.info(sRetVal)
        bRetVal = False

    LnLogger.console("[%s] - Status  interface: %s" % (interface, sRetVal))
    return bRetVal, sRetVal

# *******************************************************************************
# (interface, IPAddr, mask) = ('eth0:4', '10.1.13.234', '24')
# *******************************************************************************
def startInterface(interface, IPAddr, mask, TIMEOUT=5):
    LnLogger.console("[%s] - Starting interface" % (interface))
    bRetVal = False
    sRetVal = None
    
    # ----- check if Interface is already ACTIVE ----------
    (bCode, sCode) = Ping(IPAddr)
    if bCode == True:
        LnLogger.info("IPAddress [%s] is already alive." % (IPAddr))
        return  True, sRetVal

    # ----- executing START command (ignore rCode because testing it with Ping) ----------
    cmd = 'ifconfig %s %s/%s up' % (interface, IPAddr, mask)
    (iCode, sCode) = commands.getstatusoutput(cmd)
    if iCode != 0:
        sretVal = "ERROR [%s] - iCode:%d sCode:%s" % (cmd, iCode, sCode)
        LnLogger.error(sRetVal)
        return False, sRetVal

    # ----- WAIT for START execution ----------
    while(TIMEOUT>0):
        time.sleep(1)
        LnLogger.debug("Waiting for a while.... Starting interface [%s]" % (IPAddr))
        (bCode, sCode) = Ping(IPAddr)
        if bCode == True:
            break
        TIMEOUT -= 1

    if TIMEOUT > 0:
        sRetVal = 'Interface %s is UP' % (interface)
        LnLogger.info(sRetVal)
        bRetVal = True
    else:
        sRetVal = 'Cannot start Interface %s' % (interface)
        LnLogger.info(sRetVal)
        bRetVal = False

    LnLogger.console("[%s] - Status  interface: %s" % (interface, sRetVal))
    return bRetVal, sRetVal



