#!/usr/bin/python -O
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
# -O Optimize e non scrive il __debug__



# =========================================================================
# - Cerca di simulare il Parse del REXX:
# - leftSep == ''   Vuol dire di partire da posizione 0 della stringa
# =========================================================================
def parseString(gv, line, leftSep, rightSep):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    if leftSep == '':
        pos1 = 0
        pos2 = line.find(rightSep)
    else:
        pos1 = line.find(leftSep)
        if pos1 < 0:
            return '', line
        else:
            pos1 += 1
        pos2 = line[pos1:].find(rightSep) + pos1

    # print pos1, pos2, line[pos1:pos2].strip()

    if pos2 < 0:                # NOT FOUND
        token = line[pos1:].strip()
        rest = ''

    elif pos2 < pos1:
        token = ''
        rest = line

    elif pos2 > pos1:                                         # VALID
        token = line[pos1:pos2].strip()
        rest = line[pos2+1:].strip()

    else:#  pos2 == pos1:           # VALID???
        token = line[pos1:pos1].strip()
        rest = line[pos1:].strip()



    return token, rest