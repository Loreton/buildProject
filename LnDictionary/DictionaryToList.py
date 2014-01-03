#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Funzioni per operare sul python dictionary
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types
# #########################################################################################
# # Ritorna una lista di liste del dictionary di input
# # 2014-01-03  - Al momento supporta solo MP3Catalog dictionary
# #########################################################################################
def dictionaryToList(gv, dictID, MaxDeepLevel=99, dictLIST='Normal', Attrib=False):
    LN      = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

        # --------------------------------------------------------
        # - Ritorna una lista formattata di tutto il Dictionary
        # [ 0] dict         Bambini
        # [ 1] dict             Canzoni sotto l'albero
        # [ 2] dict                 Varie
        # [ 3] list                     Alla scoperta di Babbo NATALE: [
        # [ 3] int                                               2
        # [ 3] unicode                                           x
        # [ 3] unicode                                           .
        # [ 3] unicode                                           .
        # [ 3] int                                               3010560
        # [ 3] str                                             : ]
        # [ 3] list                     Ci vuole un fiore   : [
        # [ 3] int                                               2
        # [ 3] unicode                                           x
        # [ 3] unicode                                           .
        # [ 3] unicode                                           .
        # [ 3] unicode                                           B
        # [ 3] unicode                                           S
        # [ 3] unicode                                           .
        # [ 3] unicode                                           .
        # [ 3] str                                             : ]
        # --------------------------------------------------------
    lista = LN.dict.getDictionaryTree(gv, dictID, MaxDeepLevel=MaxDeepLevel, retCols='LTV')


        # ----------------------------------------------------------------
        # - Elaborazione delle righe tornate
        # - Viene creata una lista contenente le righe.
        # - Ogni riga a sua volta sarà una lista.
        # ----------------------------------------------------------------

        # Creiamo una lista per i livelli
    Level = []
    for i in range(MaxDeepLevel+1):
        Level.append('')

    dictLIST             = []
    fSET_END_SECTION    = False
    INSIDE_LIST         = False
    for line in lista:
        if line == '': continue
        (level, rest)  = LN.string.parseString(gv, line, '[', ']')
        level = int(level)                                      # convert unicode to integer
        objType, rest = rest.split(' ', 1)

        line = line.strip()
        rest = rest.strip()

        if INSIDE_LIST == True:
            if rest.endswith(': ]'):
                newLine = Level[:level]
                newLine.extend(currList)
                dictLIST.append(newLine)
                currList = []
                INSIDE_LIST = False
                continue
            else:
                currList.append(rest)
                continue


        if objType == 'dict':
            Level[level] = rest

        elif objType == 'list':
            Level[level] = rest.split(': [')[0]
            INSIDE_LIST = True
            currList = []
        else:
            print "objType = ", objType
            # ####################
            choice=LN.sys.getKeyboardInput(gv, "******* objType NON previsto *******", validKeys="ENTER", exitKey='X,Q', keySep=',', deepLevel=3, fDEBUG=False)
            # ####################



    # for line in dictLIST:
    #     print len(line), line
    #     print

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return dictLIST

