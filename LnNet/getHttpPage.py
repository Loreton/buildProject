#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
#
# 2012-10-10    -   Aggiunto TIMEOUT parameter

import urllib2
import base64

# ####################################################################################################
# NO auth
#   getHttpPage(gv, JBossHost, JBossURI)
# BASIC    (da provare)
#   getHttpPage(gv, 'esil588', '/jbossas', authTYPE='basic', user='asdf', passw='xx')
# DIGEST
#   getHttpPage(gv, JBossHost, JBossURI, authTYPE='digest', REALM='ManagementRealm', user='loreto', passw='asdf', JSON=True)
# ####################################################################################################

def getHttpPage(gv, myURL, myURL_Location, authTYPE=None, user=None, passw=None, REALM=None, JSON=False):
    LN          = gv.LN
    Prj         = gv.Prj
    logger      = LN.LnLogger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    if not myURL.startswith('http://'):
        myURL = 'http://' + myURL
    fullURL = myURL + myURL_Location


    logger.info('url %s - HCJ' % (fullURL))

    timeOUT = 5
    urllib2.socket.setdefaulttimeout(timeOUT)  #Bad page, timeout in 1s.


    htmlPage = None

    if authTYPE:
        if authTYPE.upper() == 'BASIC': # OK
            request = urllib2.Request(fullURL)
            base64string = base64.encodestring('%s:%s' % (user, passw)).replace('\n', '')
            request.add_header("Authorization", "Basic %s" % base64string)

        elif authTYPE.upper() == 'DIGEST':      # OK
            authhandler = urllib2.HTTPDigestAuthHandler()   # per JBoss con utenza locale (Digest)
            authhandler.add_password(
                    realm=REALM,
                    uri=myURL,
                    user=user,
                    passwd=passw
                    )
            opener = urllib2.build_opener(authhandler)
            urllib2.install_opener(opener)
            request = fullURL

        else:
            authhandler = urllib2.build_opener()
            request = fullURL









    try:
        usock    = urllib2.urlopen(request)
        htmlPage = usock.read()
        usock.close()

    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            logger.error('We failed to reach a server: <%s>. Reason: %s' % (fullURL, e.reason))
            # print "URLERROR: " + str(e)

        elif hasattr(e, 'code'):
            logger.error('The server <%s> couldn\'t fulfill the request. Error code: %s' % (fullURL, e.code))
            # print "URLERROR: " +  str(e)

    except (urllib2.HTTPError), why:
        if why.code == 401:     # "authorization failed"
            logger.error('We failed to reach a server: <%s>. Reason: %s' % (fullURL, str(why)))
            # print str(why)
        else:
            raise why
    except:
        pass






    if htmlPage and JSON == True:
        (true,false,null) = (True,False,None)
        htmlPage = eval(htmlPage)

    return htmlPage



if __name__ == "__main__":
    getPage401()