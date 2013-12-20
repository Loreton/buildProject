#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import subprocess

class LnStructure(): pass

# ###################################################################################################################
# # TESTED 2013-02-11
# # http://docs.python.org/2/library/subprocess.html
# # The shell argument (which defaults to False) specifies whether to use the shell as the program to execute.
# #    If shell is True, it is recommended to pass args as a string rather than as a sequence.
# # Example:
# #       runProcess('ls', argsList=['-la'])
# ###################################################################################################################
def runCommand(gv, command, argsList=[], exit=False):
    logger   = gv.LN.logger
    calledBy = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    CMD = command + ' ' + ' '.join(argsList)

        # -----------------------------------------------------------------
        # - subprocess.check_call       permette di catturare l'errore
        # - subprocess.call        NON  permette di catturare l'errore
        # -----------------------------------------------------------------
    logger.info('executing command: [%s]' % (CMD))
    try:
        rCode = subprocess.check_call(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logger.info('rCode is OK')

    except Exception as e:
        logger.info('rCode ERROR')
        rCode = 1
        errMSG = str(e)
        logger.error(errMSG)
        if exit:
            print errMSG
            sys.exit(rCode)

    logger.info('exiting - [called by:%s]' % (calledBy(1)))
    return rCode





def runCommand_New(gv, command, wkdir='.', argsList=[], PWAIT=0, stdOUTfile=False, exit=False):
    retVal = LnStructure()
    retVal.err = None
    retVal.rcode = 0

    logger   = gv.LN.logger
    calledBy = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    CMD = command + ' ' + ' '.join(argsList)
    logger.info('executing command: [%s]' % (CMD))

    stdIN, stdOUT, stdERR   =   (subprocess.PIPE, subprocess.PIPE, subprocess.PIPE)


    if stdOUTfile:
        logger.info("Run with redirection to: %s" %(stdOUTfile))
        f = open(stdOUTfile, 'a')
        stdIN, stdOUT, stdERR   =   (subprocess.PIPE, f, f)

    procID = subprocess.Popen(CMD, shell=True, stdin=stdIN, stdout=stdOUT, stderr=stdERR, bufsize=1, cwd=wkdir)

        # ---------------------------------------------------
        # - Al momento 2013-09-13 è assicurato solo "else:"
        # ---------------------------------------------------
    if PWAIT == 99:     # live ma va verificato.
        arrayOut = []
        arrayErr = []

        for line in iter(procID.stdout.readline, b''):
            print line,
            arrayOut.append(line.strip('\n'))

        for line in iter(procID.stderr.readline, b''):
            print line,
            arrayErr.append(line.strip('\n'))

        procID.communicate()
        retVal.output   = arrayOut
        retVal.err      = arrayErr

    elif PWAIT > 0:
        timeOut = PWAIT
        retVal = WaitProcess(procID, timeOut)

    elif PWAIT < 0:     # attesa infinita
        print "WARNIG - Attesa processo senza TimeOUT"
        procID.wait()
        retVal.output = procID.stdout.read()
        retVal.err    = procID.stderr.read()

    else:
        retVal.output   = procID.stdout.read().split('\n')
        retVal.err      = procID.stderr.read().split('\n')

    if retVal.err:
        retVal.rcode = 1

    # print
    # for line in retVal.err:     print line
    # print
    # for line in retVal.output:  print line
    # sys.exit()
    return retVal

# =========================================================
# - Attende la fine del processo oppure va in TimeOUT
# - called by: runCommand_New
# =========================================================
import datetime, time
import os
def WaitProcess(procID, timeOut):
    retVal = LnStructure()
    retVal.err = None

    timeOut_mS = timeOut*1000000
    start = datetime.datetime.now()
    mySIGKILL = 9
    myWNOHANG = 1
    while procID.poll() is None:
        time.sleep(0.1)
        now = datetime.datetime.now()
        elapsed_Sec = (now - start).seconds
        if elapsed_Sec > timeOut:
            os.kill(procID.pid, mySIGKILL)
            retVal.output = ''
            retVal.err    = 'Timeout occurs WAITing process to be completed'
            break

    if not retVal.err:
        retVal.output = procID.stdout.read()
        retVal.err    = procID.stderr.read()

    return retVal

# Fa il print live delle righe
def runCommand_3(gv, command, wkdir='.', argsList=[], exit=False):
    logger   = gv.LN.logger
    calledBy = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    CMD = command + ' ' + ' '.join(argsList)

    logger.info('executing command: [%s]' % (CMD))

    proc = None
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, cwd='.')

    for line in iter(proc.stdout.readline, b''):
        print line,

    for line in iter(proc.stderr.readline, b''):
        print line,

    proc.communicate()


    return
