#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import sys
import subprocess
import os


# #####################################################################
# # Return the PID list if processName is provided
# #####################################################################
def getPidCommandLineArgs(gv, PID, exitOnError=False):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy

    if gv.OpSys.upper() == 'WINDOWS':
        CMD = '%s -iql %s' % (gv.PVEXE, PID)
    else:
        CMD = 'ps -fp %s | tail -1' % (PID)

    logger.info('Executing command: %s' % (CMD))
    rcPid = LN.proc.runProcess(gv, CMD, PWAIT=True)
    if rcPid.err:
        logger.error('Error: %s' % (rcPid.err))
        print LN.cERROR + rcPid.err
        if exitOnError:
            LN.sys.exit(gv, 9009, rcPid.err)
    else:
        logger.info('Output: %s' % (rcPid.output))

    return rcPid










##################### W I N D O W S ####################################################
##################### W I N D O W S ####################################################
##################### W I N D O W S ####################################################
##################### W I N D O W S ####################################################

# #####################################################################
# # Return the PID list if processName is provided - USA TASKLIST
# #####################################################################
def getPIDsWinTL(gv, processName, str2Search=None):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(2)))

    if not processName.endswith('*'): processName += '*'

    ps = subprocess.Popen(r'tasklist.exe /NH /FO TABLE /FI "IMAGENAME eq %s"' % (processName), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ps = subprocess.Popen('pv.exe -eqb' % (processName), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    rows = output.split('\n')

    PIDs = []
    for line in rows:
        token = line.strip('\r').split()
        if len(token) > 3:
            PIDs.append(token[1])

    return PIDs

# #####################################################################
# # Return the PID list if processName is provided - USA PV.EXE
# #####################################################################
def getPIDsWin(gv, processName, str2Search=None):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(2)))


    if not processName.endswith('*'): processName += '*'

    ps = subprocess.Popen(gv.PVEXE + ' -eqb %s' % (processName), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    rows = output.split('\n')

    PIDs = []
    for line in rows:
        line = line.strip('\r')
        if line.strip() != '':
            PIDs.append(line.strip())

    return PIDs


'''
def getPidCLineUnix(gv, processID):
    CMD = 'ps -fp %s | tail -1' % (pid)
    pass

def getPidCLineWin(gv, processID):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(2)))

    CMD = '%s -iql %s' % (gv.PVEXE, pid)
    logger.info('Executing command: %s' % (CMD))
    rcPid = LN.proc.runProcess(gv, CMD, PWAIT=True)
    return rcPid
'''






##################### U N I X ####################################################
##################### U N I X ####################################################
##################### U N I X ####################################################
##################### U N I X ####################################################


# #####################################################################
# # Return the PID list if processName is provided
# # if str2Search is provided, will search for it in the parameter value
# #####################################################################
def getPIDsUnix(gv, processName, str2Search=None):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(2)))

    ps = subprocess.Popen("ps ax -o pid -o args ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()

    PIDs = []
    for line in output.split("\n"):
        line = line.strip()                 # IMPORTANTE
        if line == '': continue
        (pid, process) = line.split(' ', 1)
        if process.find(processName) >= 0:
            if str2Search:
                if process.find(str2Search) >= 0:
                    PIDs.append(pid)
            else:
                PIDs.append(pid)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return PIDs


