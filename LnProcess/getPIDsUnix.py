#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import sys
import subprocess


# ##############################################################################
# # Return the PID list if processName is provided
# # if str2Search is provided, will search for it in the parameter value
# ##############################################################################
def getPIDsUnix(gv, processName, str2Search=None):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

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


