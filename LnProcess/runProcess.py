#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import sys
import subprocess
import datetime, os, time, signal

class LnStructure(): pass


# ###################################################################################################################
# # http://docs.python.org/2/library/subprocess.html
# # The shell argument (which defaults to False) specifies whether to use the shell as the program to execute.
# #    If shell is True, it is recommended to pass args as a string rather than as a sequence.
# #    Per tale ragione convertiamo in stringa eventuali args[]
# # * stdOUT:   Indica il nome del file che vogliamo usare come redirect per stdout
# # *           Nel caso volessimo dividere OUT ed ERR bisogna implementare un nuovo parametro stdERR
# ###################################################################################################################
def runProcess(gv, command, argsList=[], PWAIT=True, timeOut=None, stdOUTfile=False):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    retVal = LnStructure()
    retVal.err = None

    CMD = command + ' ' + ' '.join(argsList)

    if stdOUTfile:
        logger.info("RunAS with redirection to: %s" %(stdOUTfile))
        f = open(stdOUTfile, 'a')
        stdIN   =   subprocess.PIPE
        stdOUT  =   f
        stdERR  =   f
    else:
        logger.info("RunAS with NO redirect")
        stdIN   =   subprocess.PIPE
        stdOUT  =   subprocess.PIPE
        stdERR  =   subprocess.PIPE

    ps = subprocess.Popen(CMD, shell=True, stdin=stdIN, stdout=stdOUT, stderr=stdERR)

    if PWAIT and timeOut:
        timeOut_mS = timeOut*1000000
        start = datetime.datetime.now()
        mySIGKILL = 9
        myWNOHANG = 1
        while ps.poll() is None:
            time.sleep(0.1)
            now = datetime.datetime.now()
            elapsed_Sec = (now - start).seconds
            if elapsed_Sec > timeOut:
                # print LN.cERROR + 'killing....', ps.pid
                os.kill(ps.pid, mySIGKILL)
                retVal.output = ''
                retVal.err    = 'Timeout occurs WAITing process to be completed'
                break

        if not retVal.err:
            retVal.output = ps.stdout.read()
            retVal.err    = ps.stderr.read()

    elif PWAIT:
        ps.wait()
        retVal.output = ps.stdout.read()
        retVal.err    = ps.stderr.read()

    else:
        retVal.output = ps
        retVal.err = ''
    
    logger.debug("retVal1.output       = %s" % (retVal.output))
    logger.debug("retVal1.errMsg       = %s" % (retVal.err))

        # Soluzione Empirica -  da verificare attentamente
    if not ps.returncode == 0:
        if retVal.err == '':
            #failingWords = ['failed', 'error', 'not found', 'rolled back']
            #for word in failingWords:
                #if word in retVal.output or word.upper() in retVal.output :
                    #print '>>>>' + word.upper() + '<<<<'
            retVal.err      = retVal.output
            retVal.output   = ''
                    #break

    logger.debug("retVal2.output       = %s" % (retVal.output))
    logger.debug("retVal2.errMsg       = %s" % (retVal.err))

    logger.info('exiting - [called by:%s]' % (calledBy(1)))
    return  retVal



'''
# ###################################################################################################################
# # http://docs.python.org/2/library/subprocess.html
# # The shell argument (which defaults to False) specifies whether to use the shell as the program to execute.
# #    If shell is True, it is recommended to pass args as a string rather than as a sequence.
# #    Per tale ragione convertiamo in stringa eventuali args[]
# # * stdOUT:   Indica il nome del file che vogliamo usare come redirect per stdout
# # *           Nel caso volessimo dividere OUT ed ERR bisogna implementare un nuovo parametro stdERR
# ###################################################################################################################
def runProcess_Prev(gv, command, argsList=[], PWAIT=True, stdOUTfile=False):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    retVal = LnStructure()

    CMD = command + ' ' + ' '.join(argsList)

    if stdOUTfile:
        logger.info("RunAS with redirection to: %s" %(stdOUTfile))
        f = open(stdOUTfile, 'a')
        stdIN   =   subprocess.PIPE
        stdOUT  =   f
        stdERR  =   f
    else:
        logger.info("RunAS with NO redirect")
        stdIN   =   subprocess.PIPE
        stdOUT  =   subprocess.PIPE
        stdERR  =   subprocess.PIPE

    ps = subprocess.Popen(CMD, shell=True, stdin=stdIN, stdout=stdOUT, stderr=stdERR)

    if PWAIT:
        ps.wait()
        retVal.output = ps.stdout.read()
        retVal.err    = ps.stderr.read()

    else:
        retVal.output = ps
        retVal.err = ''

    logger.debug("retVal1.output       = %s" % (retVal.output))
    logger.debug("retVal1.errMsg       = %s" % (retVal.err))

        # Soluzione Empirica -  da verificare attentamente
    if retVal.err == '':
        failingWords = [' failed ', ' error ', ' not found ', ' rolled back ']
        for word in failingWords:
            if word in retVal.output or word.upper() in retVal.output :
                retVal.err      = retVal.output
                retVal.output   = ''
                break

    logger.debug("retVal2.output       = %s" % (retVal.output))
    logger.debug("retVal2.errMsg       = %s" % (retVal.err))

    logger.info('exiting - [called by:%s]' % (calledBy(1)))
    return  retVal

'''
