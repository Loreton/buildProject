#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-
# -O Optimize e non scrive il __debug__
#
# http://code.activestate.com/recipes/66062-determining-current-function-name/
# Version 0.01 08/04/2010:  Starting
# ####################################################################################################################
import sys, os

def LINE( back = 0 ):
    return sys._getframe( back + 1 ).f_lineno

def FILE( back = 0 ):
    return sys._getframe( back + 1 ).f_code.co_filename

def FUNC( back = 0):
    return sys._getframe( back + 1 ).f_code.co_name

def FNAME( back = 0 ):
    frame = sys._getframe( back + 1 )
    return "%s" % ( os.path.basename( frame.f_code.co_filename ))

def FileDIR( back = 0 ):
    frame = sys._getframe( back + 1 )
    return "%s" % ( os.path.basedir( frame.f_code.co_filename ))

def whoAmI( back = 0 ):
    frame = sys._getframe( back + 1 )

    return "[%s:%s] %s()" % ( os.path.basename( frame.f_code.co_filename ),
                           frame.f_lineno, frame.f_code.co_name )

import inspect
def calledBy(deepLevel=0):

    try:
        caller = inspect.stack()[deepLevel + 1]

    except Exception, why:
        # message = "WARNING - [%s] \nNot important if you are aware." % (why)
        # print "\n\nLnSys.calledBy - " + message
        return '%s' % (why)
        return 'Unknown - %s' % (why)

    programFile = caller[1]
    lineNumber  = caller[2]
    funcName    = caller[3]
    lineCode    = caller[4]

    fname       = os.path.basename(programFile).split('.')[0]
    str = "[%s-%s:%d]" % (fname, caller[3], int (caller[2]) )
    str = "[%s.%s:%s]" % (fname, funcName, lineNumber)
    return str