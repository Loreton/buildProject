#!/usr/bin/python -O
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
# -O Optimize e non scrive il __debug__


# =========================================================================
# - Ritorna:
# - 1    il char del QUOTE
# - 2. 3 la posizione dei QUOTE_CHARs
# - 4    la stringa senza i QUOTE_CHARs
# =========================================================================
def stripQuote(gv, inpString):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    fDEDUG = False
    if fDEDUG: MyLogger.debug("inpString: len=%4d |%s|" % (len(inpString), inpString) )
    quoteChars = "\'\""
    inpString = inpString.strip()
    for char in quoteChars:
        if len(inpString) > 1:
            if fDEDUG: MyLogger.debug("inpString:  char=|%s| strLen=%4d str:|%s|" % (char, len(inpString), inpString) )
            if inpString[0] == char and inpString[-1] == char:
                inpString = inpString[1:-1]

    return inpString