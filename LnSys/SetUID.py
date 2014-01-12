#!/usr/bin/python -O
# -*- coding: iso-8859-1 -*-
# -*- coding: latin-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys, platform
import subprocess
import getpass
if platform.system().upper() != 'WINDOWS': import pwd

# ###################################################################################################################
# # setUID()
# # Change dello userID all'interno di uno script python
# # Return:
# #     0       se OK
# #     1       se Errore (EXIT if exitOnError==True)
# ###################################################################################################################
def setUID(gv, user, exitOnError=False):
    logger   = gv.LN.logger
    calledBy = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    currUser = getpass.getuser()
    if user == currUser:
        logger.info("L'utente richiesto [%s] risulta essere quello attivo [%s]" % (user, currUser)
    else:
        logger.info("L'utente richiesto [%s] risulta diverso da quello attivo [%s]" % (user, currUser)
        uid = pwd.getpwnam(user)[2]

        try:
            os.setuid(uid)
            logger.info("L'utente richiesto [%s] è il nuovo utente attivo" % (user)

        except (OSError), why:
            logger.error("setUID error: %s" % (why))
            if exitOnError:
                LN.sys.exit(gv, 99, why)
            return 1


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return 0





