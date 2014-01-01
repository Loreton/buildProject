#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-
# -O Optimize e non scrive il __debug__
#
# Version 0.01 08/04/2010:  Starting
# ####################################################################################################################
import os, sys
from   types import *                     # per StringType, etc


# ###########################################################################
# * Gestione input da Keyboard.
# * 29-08-2010 - Rimosso LnSys dalla chiamata alla LnSys.exit()
# * 12-02-2012 - Cambiato keys in keyLIST
# * 12-03-2013 - Cambiato keyLIST in validKeys
# * 01-01-2014 - modificato il validKeysLIST.
# ###########################################################################
def getKeyboardInput(gv, msg, validKeys='ENTER', exitKey='X', deepLevel=3, fDEBUG=False, keySep=","):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    exitKeyUPP = exitKey.upper()

    if keySep in validKeys:
        validKeyLIST = validKeys.split(keySep)
    else:
        validKeyLIST = list(validKeys)

    if keySep in exitKeyUPP:
        exitKeyLIST = exitKeyUPP.split(keySep)
    else:
        exitKeyLIST = list(exitKeyUPP)

    # print exitKeyLIST
    # print validKeyLIST
    print
    if fDEBUG:
        callerFunc1 = "%s" % (calledBy(deepLevel-1))
        callerFunc2 = "%s" % (calledBy(deepLevel))
        msg = "[%s - %s]\n         <%s [%s]> - (%s to exit) ==> " % (callerFunc2, callerFunc1, msg, validKeys, exitKey)
    else:
        msg = "%s [%s] - (%s to exit) ==> " % (msg, validKeys, exitKey)

    try:
        while True:
            choice      = raw_input(msg).strip()
            choiceUPP   = choice.upper()
            if fDEBUG: print "choice: [%s]" % (choice)

            if choice == '':
                if "ENTER" in validKeyLIST:
                    return ''
                else:
                    print '\n... please enter something\n'

            elif choiceUPP in exitKeyLIST:
                print "Exiting on user requests"
                sys.exit(1)

            elif choice in validKeyLIST:
                break

            else:
                print '\n... try again\n'

    except StandardError, why:
        exit(8, "Error running program [%s]\n\n ....%s\n"  % (sys.argv[0], why) )

    logger.info('exiting - [called by:%s]' % (calledBy(1)))
    return choice


