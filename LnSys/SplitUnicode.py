#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-


def splitUnicode(gv, sourceStr, sep):
    logger   = gv.LN.logger
    calledBy = gv.LN.sys.calledBy
    logger.debug('Entered - [called by:%s]' % (calledBy(1))) # Non mettere .info

    logger.debug("Source string: <%s>" % (sourceStr) )

    token = sourceStr.split(sep)

    for i in range(len(token)):
        u = token[i]
        if not isinstance(u, unicode):
            if isinstance(u, str):
                token[i] = unicode( u, "latin-1" )
            else:
                pass   # integer or long datatype
                # u = str(u)   # integer or long datatype
        logger.debug("Token: <%s>" % (token[i]) )

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return token


