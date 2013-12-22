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

##########################################################################
# - initLog() per gli altri moduli - Si basano sulla variabile 'LoggerID'
# -           oppure deve essere chiamata la initLog(LogID)
##########################################################################
#    import logging
#    logger = None
#    LoggerID = os.getenv('LoggerID')
#    def initLog(logID):
#       global loggerName, logger
#       loggerName  = logID + '.' + __name__
#       logger      = logging.getLogger(loggerName)
#       logger.info("I'm active on this log.")
#
#    if (logger == None)  and (LoggerID != None and LoggerID != ''):   initLog(LoggerID)
#
#----------------------------------------------------------------------
#
#   def add1(x, y):
#       """"""
#       funcName = sys._getframe().f_code.co_name
#       logger = logging.getLogger(loggerName + "." + funcName)
#       logger.info("added %s and %s to get %s" % (x, y, x+y))
#       return x+y
#
#    import LnOtherModulo as otherMod; otherMod.init(loggerName)


#############################################################################################
# - initLog()
# - LoggerName è l'ID del LOG. Da esso ricaviamo anche il filename
# - Se si vogliono due LOG devo replicare il file.
#############################################################################################
def init(loggerID, logDir, logFname, maxBytes=1000000, nFiles=2):
    # print "%s %s %s %d %d" % (loggerID, logDir, logFname, maxBytes, nFiles)
    # sys.exit()

    global gRootLogger, gRotateHandler, gConsoleHandler, gLogFilePath, gLogDir
    LOG_FILENAME = os.path.join(logDir, logFname)
    if not os.path.isdir(logDir):
        print "LogDir: %s non esiste. Crearla (o cambiarla) per proseguire."
        sys.exit

    gLogDir = logDir
        # carica il file di logConfig
    # logging.config.fileConfig(logConfigFileName)

        # creiamo il nostro pointer
    rootLogger = logging.getLogger(loggerID)

    # Set up a specific logger with our desired output level
    rootLogger.setLevel(logging.DEBUG)


        # Add the log message handler to the rootLogger
    ROTATE_FORMAT         = '%(asctime)s %(msecs)d %(levelname)-8s [%(module)s:%(lineno)d] %(message)s'
    ROTATE_FORMAT         = '%(asctime)s %(levelname)-8s [%(module)-25s:%(lineno)d] %(message)s'
    ROTATE_FORMAT         = '%(asctime)s %(levelname)-8s [%(name)-35s:%(lineno)d] %(message)s'
    ROTATE_FORMAT         = '%(levelname)-8s [%(name)-50s:%(lineno)d] %(message)s'
    ROTATE_FORMAT         = '%(levelname)-8s [%(module)-50s:%(lineno)d] %(message)s'
    ROTATE_DATE_FORMAT    = '%d-%m-%Y %H:%M:%S'
    rotateHandler         = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=maxBytes, backupCount=nFiles)
    rotateFormatter       = logging.Formatter(fmt=ROTATE_FORMAT, datefmt=ROTATE_DATE_FORMAT)
    rotateHandler.setFormatter(rotateFormatter)


        # Add the log message handler to the console
    CONSOLE_FORMAT          = '[%(name)-35s:%(lineno)d] %(levelname)-8s %(message)s'
    CONSOLE_FORMAT          = '[%(module)-35s:%(lineno)d] %(levelname)-8s %(message)s'
    CONSOLE_DATE_FORMAT     = '%H:%M:%S'
    consoleHandler          = logging.StreamHandler()
    consoleFormatter        = logging.Formatter(fmt=CONSOLE_FORMAT, datefmt=CONSOLE_DATE_FORMAT)
    consoleHandler.setFormatter(consoleFormatter)

    rootLogger.addHandler(consoleHandler)
    rootLogger.addHandler(rotateHandler)

    gRootLogger     = rootLogger
    gRotateHandler  = rotateHandler
    gConsoleHandler = consoleHandler

    gLogFilePath = LOG_FILENAME

    return rootLogger


def getFilePath():
    return gLogFilePath

def getLogDir():
    return gLogDir


import platform

def changeLevel(handler, level, type):
    handler.disabled = True

    if level == None:
        handler.setLevel(logging.CRITICAL)
        # NON ho capito perché mi dà errore su Windows.
        if platform.system().upper() != 'WINDOWS': gRootLogger.removeHandler(handler)

    else:
        handler.setLevel(level)
        handler.disabled = False
        gRootLogger.addHandler(handler)
        gRootLogger.warning("------------------------------------------------------------")
        gRootLogger.warning("- [%s:%s] activated - called by: %s" % (type, LOG_LEVELS[level], calledBy(2)))
        gRootLogger.warning("------------------------------------------------------------")


# comodo per usarlo con le mie funzioni di info,error,...
def setShortLine():
    ROTATE_FORMAT     = '%(levelname)-8s %(message)s'
    rotateFormatter   = logging.Formatter(fmt=ROTATE_FORMAT)
    gRotateHandler.setFormatter(rotateFormatter)

    CONSOLE_FORMAT    = '%(levelname)-8s %(message)s'
    consoleFormatter  = logging.Formatter(fmt=CONSOLE_FORMAT)
    gConsoleHandler.setFormatter(consoleFormatter)

def setFileLevel(level=None):
    changeLevel(gRotateHandler, level, "FILE")

def setConsoleLevel(level=None):
    changeLevel(gConsoleHandler, level, "CONSOLE")



def info(text):
    msg = "%-35s - %s" % (calledBy(1), text)
    if gRootLogger:
        gRootLogger.info(msg)
    else:
        if gConsoleANYWAY: print "INFO    - ", msg


def warning(text):
    msg = "%-35s - %s" % (calledBy(1), text)
    if gRootLogger:
        gRootLogger.warning(msg)
    else:
        if gConsoleANYWAY: print "WARNING - ", msg

def error(text):
    msg = "%-35s - %s" % (calledBy(1), text)
    if gRootLogger:
        gRootLogger.error(msg)
    else:
        if gConsoleANYWAY: print "ERROR   - ", msg


def debug(text):
    # if gRootLogger:  gRootLogger.debug("%-30s - %s" % (calledBy(1), text) )
    msg = "%-35s - %s" % (calledBy(1), text)
    if gRootLogger:
        gRootLogger.debug(msg)
    else:
        if gConsoleANYWAY: print "DEBUG   - ", msg


def setConsoleAnyway(status):
    gConsoleANYWAY = status






import inspect
def calledBy(deepLevel=0):
    try:
        caller = inspect.stack()[deepLevel +1]

    except Exception, why:
        message = "WARNING - [%s] \nNot important if you are aware." % (why)
        print "\n\nLnSys.calledBy - " + message
        return 'Unknown - %s' % (why)

    programFile = caller[1]
    lineNumber  = caller[2]
    funcName    = caller[3]
    lineCode    = caller[4]

    fname       = os.path.basename(programFile).split('.')[0]
    # str = "[%s-%s:%d]" % (fname, caller[3], int (caller[2]) )
    str = "[%s.%s:%s]" % (fname, funcName, lineNumber)
    # str = "[%s:%s]" % (fname, lineNumber)
    return str



if __name__ == "__main__":
    main()