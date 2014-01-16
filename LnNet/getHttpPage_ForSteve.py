#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# 2012-10-10    -   Aggiunto TIMEOUT parameter

import urllib2
import base64


def getHttpPageTEST(myURL):
    htmlPage = None


    print ('url %s - HCJ' % (myURL))

    timeOUT = 5
    urllib2.socket.setdefaulttimeout(timeOUT)  # timeout in secondi.


    # -----------------------
    # - Connessione
    # -----------------------


    try:
        usock    = urllib2.urlopen(myURL)
        htmlPage = usock.read()
        usock.close()

    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print ('We failed to reach a server: <%s>. Reason: %s' % (myURL, e.reason))

        elif hasattr(e, 'code'):
            print('The server <%s> couldn\'t fulfill the request. Error code: %s' % (myURL, e.code))

    except (urllib2.HTTPError), why:
        if why.code == 401:     # "authorization failed"
            print('We failed to reach a server: <%s>. Reason: %s' % (myURL, str(why)))
        else:
            raise why
    except:
        pass


    return htmlPage


if __name__ == "__main__":
    page = getHttpPageTEST('http://esil588')
    print page