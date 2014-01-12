#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os

#############################################################################################
# - getJsonData
#############################################################################################
def getJsonData(gv, inpFname):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = LN.LnLogger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    JsonDict = None

    if not os.path.isfile(inpFname):
        msg = "ERROR --- JSON file [%s] is missing... or NOT found." % (inpFname)
        Prj.exit(gv, 2010, msg)

    data = ''

        # Lettura dei dati da file
    try:
        import json

    except ImportError:
        import simplejson as json

    try:
        f = open(inpFname, "r")
        JsonDict = json.load(f)
        f.close()

    except (IOError, os.error), why:
        strError = "ERROR reading File [%s]:\n       %s" % (inpFname, str(why))
        logger.error(strError)
        Prj.exit(gv, 2011, strError)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return JsonDict


