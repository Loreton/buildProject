#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-

# *********************************************************************
# * Calcolo del tempo di esecuzione di una funzione
# *     from functools import partial
# *     funcName(param1=p, p2) ==> perform(partial(funcName, param1=p, p2))
# *
# * LnSys.timeFuncElapsed(partial(Action3, "Ciao1", param2="Ciao2"), fPRINT=True )
# * LnSys.timeFuncElapsed(partial(funcName, "Ciao1", param2="Ciao2"), fPRINT=True )
# *********************************************************************
import datetime as DT
import time
from functools import partial
import  functools

# solo per test
def Action3(param1, param2=''):
    print "sono Action3 %s - %s" % (param1, param2)

def timeFuncElapsed(funcToCall, fPRINT=True):

    startTimeSecs   = getNow()
    retValue        = funcToCall()
    endTimeSecs     = getNow()
    # print endTimeSecs-startTimeSecs

    if fPRINT:
        print ("* %s" % ("-"*40) )
        # print '*     Start   time: %20s' % (convert(secs=startTimeSecs) )
        print '*     Start   time: %20s' % (convert(secs=startTimeSecs, out="STR") )
        print '*     End     time: %20s' % (convert(secs=endTimeSecs, out="STR") )
        print '*     Elapsed time: %20s' % (convert(secs=endTimeSecs-startTimeSecs, out="STR", outputFormat="%H:%M:%S" ) )
        print ("* %s" % ("-"*40) )

    return retValue




###################################################################################################
# - M  A I N
###################################################################################################
from TimeConvert import timeConvert as convert
from TimeGetNow  import timeGetNow as getNow
if __name__ == "__main__":
    timeFuncElapsed(partial(Action3, "Ciao1", param2="Ciao2"), fPRINT=True )
    pass
    # xx = callFunctionName('LnSys.callerPrint')
    # xx = callFunctionName('callerPrint')
    # xx = callFunctionName('LnDict.initLog')
