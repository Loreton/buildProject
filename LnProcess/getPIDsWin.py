#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import sys
import subprocess
import os



# #####################################################################
# # Return the PID list if processName is provided - USA PV.EXE
# #####################################################################
def getPIDsWin(gv, procName, str2Search=None):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    processNAME = procName

    if not procName.endswith('*'): processNAME = procName + '*'

    ps = subprocess.Popen(gv.PVEXE + ' -ql %s' % (processNAME), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()


    PIDs = []


    for line in output.split("\n"):
        line = line.strip()                 # IMPORTANTE
        if line == '': continue
        line = line.replace('\t', ' ')    # replace del tab
        (procName, pid, procArgs) = line.split(' ', 2)
        if str2Search:
            if procArgs.find(str2Search) >= 0:
                PIDs.append(pid)
        else:
            PIDs.append(pid)


    return PIDs

