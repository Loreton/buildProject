#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import logging
import logging.config
import os, sys

gRootLogger     = None
gRotateHandler  = None
gConsoleHandler = None
gLogFilePath    = None
gLogDir         = None
gConsoleANYWAY  = True

LOG_LEVELS = {
    logging.DEBUG       : 'DEBUG',
    logging.INFO        : 'INFO',
    logging.CRITICAL    : 'CRITICAL',
    logging.WARNING     : 'WARNING',
    logging.ERROR       : 'ERROR',
}

logger = None

## ################################################################
# - initLog()
# - Prevede che la variabile Project sia stata impostata prima del lancio
# - La variabile LnProject ?ndispensabile in quanto tutti i moduli la cercano
# ################################################################
def initUserLog(logID):

    if not logID:
        print 'initUserLog.............................', logID
        print
        print "initUserLog - Please set <%s> environment variable before start this program." % (logID)
        print
        sys.exit(88)

    try:
        # creazione del LOG
        (userLoggerCLASS, userLogger) = LnLOG.initLog(logID, init=True)

    except AttributeError, why:
        print ("\n\n--- ERROR opening Logger for %-20s\n  - [%s]\n  - [%s]" % (logID, why, LnLOG.calledBy(-2)))
        sys.exit(-2)

    userLoggerCLASS.enableConsoleLogger(logging.INFO)
    userLoggerCLASS.enableRotateLogger(logging.DEBUG)
    userLogger.info("Logger for %-20s has been initialized. - called by %s" % (logID, LnLOG.calledBy(3)))
    return userLogger, userLoggerCLASS

if __name__ == "__main__":
    main()