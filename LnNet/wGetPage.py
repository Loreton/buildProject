#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# 2012-10-10    -   Aggiunto TIMEOUT parameter

import sys, os

def wGetPage(gv, myHost, myURL, user=None, passw=None, JSON=False):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = LN.LnLogger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))
    # username, password = 'asdfds', 'asdfasd'

    try:
        outTempFile = '/tmp/jsonfile'
        os.remove(outTempFile)
    except:
        pass

    htmlPage = None
    WGET_Options = "--output-document={0:s} http://{1:s}{2:s}".format(outTempFile, myHost, myURL)
    if user: WGET_Options = " --http-user={0:s} --http-password={1:s} {2:s}".format(username, password, WGET_Options)

    CMD = "wget " + WGET_Options
    retVal = LN.proc.runCommand_New(gv, CMD, PWAIT=3)

    if "Saving to:" in retVal.err and outTempFile in retVal.err and "saved " in retVal.err:
        retVal.rcode = 0
    else:
        LN.dict.printDictionaryTree(gv, retVal, retCols='TV', lTAB=' '*4, console=True)

    if retVal.rcode == 0:
        try:
            if JSON:
                import json
                f = open(outTempFile, "r")
                htmlPage = json.load(f)
                f.close()
            else:
                htmlPage = LN.file.readAsciiFile(gv, outTempFile, exitOnError=True)

        except (IOError, os.error), why:
            strError = "ERROR reading File [%s]:\n       %s" % (inpFname, str(why))
            logger.error(strError)
            Prj.exit(gv, 2011, strError)


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return htmlPage


if __name__ == "__main__":
    main()