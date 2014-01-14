#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Funzioni per operare sul python dictionary
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import types

# #########################################################################################
# - printDictionaryTree() ordered
# - CALL: printDictionaryTree(CfgDict, MaxDeepLevel=3, values=True, lTAB=' '*12)
# - PARAMS:
# -     level:          serve per tenere traccia delle iterazioni ed anche per l'indentazione
# -     MaxDeepLevel:   Indica il numero MAX di profondità (iterazioni) da raggiungere
# -     values:         Indica se ritornare anche il valore delle keys
# -     lTAB:           Prefix a sinistra della riga
# -     retCols:         'LTV'
# -                        L  se vogliamo LevelCol
# -                        T  se vogliamo Type
# -                        V  se vogliamo Value
# -
# #########################################################################################
def printDictionaryTree(gv, dictID, header=None, MaxDeepLevel=999, level=0, retCols='LTV', lTAB='', console=False):
    LN      = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    lista = LN.dict.getDictionaryTree(gv, dictID, MaxDeepLevel=MaxDeepLevel, level=level, retCols=retCols)

    if header:
        logger.info("*"*60)
        logger.info("*     %s" % (header) )
        logger.info("*"*60)
    for line in lista:
        logger.info("%s%s" % (lTAB, line) )

    if console:
        COLOR = LN.cBWH
        COLOR = LN.cWHITE + LN.HI.BRIGHT
        COLOR = LN.cMAGENTA
        COLOR = LN.cCYAN

        if header:
            print
            print lTAB + COLOR + "*"*60
            print lTAB + COLOR + "*     %s" % (header)
            print lTAB + COLOR + "*"*60
        for line in lista:
            print COLOR + "%s%s" % (lTAB, line)



    # if header:
    #     logger.info("*"*60)
    #     logger.info("*     %s" % (header) )
    #     logger.info("*"*60)

    #     if console:
    #         print
    #         print lTAB + "*"*60
    #         print lTAB + "*     %s" % (header)
    #         print lTAB + "*"*60
    #         print

    # for line in lista:
    #     outLine ="%s%s" % (lTAB, line)
    #     if header:  logger.info(outLine)
    #     if console: print outLine


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))



def printObject(object):
    for i in [v for v in dir(object) if not callable(getattr(object,v))]:
        print '\n%s:' % i
        exec('print object.%s\n\n') % i