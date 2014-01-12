#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# 2012-10-10    -   Aggiunto TIMEOUT parameter

import sys, os
import httplib
import urllib
import urllib2

###########################################################################
# - get(url, logger=None, type=None)
# - params:
# -     url:     URL ( "http://esil610.ac.bankit.it:8080/json-console/JsonResponder")
# -     logger:  loggerPointer
# -     type:   'JSON' per avere la conversione della pagina JSON in un DICT
###########################################################################
def httpGet(gv, url, timeOUT=5.0, logger=None, type=None):
    LN          = gv.LN
    logger      = LN.LnLogger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    bRetVal = False
    sStatus = False
    htmlPage = None

    logger.info('url %s - HCJ' % (url))

    try:
        urllib2.socket.setdefaulttimeout(timeOUT)  #Bad page, timeout in 1s.
        usock = urllib2.urlopen(url)

    except urllib2.URLError, e:

        if hasattr(e, 'reason'):
            logger.info('We failed to reach a server: <%s>. Reason: %s' % (url, e.reason))
            bRetVal = False

        elif hasattr(e, 'code'):
            logger.info('The server <%s> couldn\'t fulfill the request. Error code: %s' % (url, e.code))
            bRetVal = False

    else:         # everything is fine
        sStatus = 'RUNNING'
        htmlPage = usock.read()     # contiene la pagina HTML
        usock.close()
        bRetVal = True

    logger.info('%s' % (sStatus))

        # ---------------------------------------------------------------------
        # Python can parse json into a dict/array using the eval
        # statement as long as you set true/false/null to the right values.
        # convert to a native python object
        # ---------------------------------------------------------------------
    if bRetVal:
        if type == 'JSON':
            (true,false,null) = (True,False,None)
            htmlPage = eval(htmlPage)
            # print types(htmlPage)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return bRetVal, htmlPage

def main():
    sys.exit()

if __name__ == "__main__":
    main()