#!/usr/bin/python -O
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
# -O Optimize e non scrive il __debug__

import types

# ======================================================================================
# - Converte i parametri comunque in una LIST
# - Anche se la stringa non la si divide.
# - Il carattere di separazione è ','
# - La stringa all'interno di quote chars è considerata unica.
#
# - I seguenti input tornano tutti 4 campi:
# -     null,null,null,null
# -     ,,,
# -     UserID,,,
# -     UserID        ,           ,       ,
# -     Password      , VARCHAR   , 50    ,
# -     Title1        ,"VARCHAR 01", 50    , "PRIMARY KEY"
# -
# ======================================================================================

def stringToList(gv, inpString, sepChars=','):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))


    quoteChars = "\'\""
    listData = []                       # returned LIST
    posSTART, posEND = 0, 0
    QUOTE_CHAR = False

    if isinstance(inpString, types.ListType):               # Version 0.07 - E' già una LIST, ne facciamo lo STRIP
        # print '............ it is a LIST'
        for i in range(len(inpString)):
            inpString[i] = inpString[i].strip()
        logger.debug('exiting - [called by:%s]' % (calledBy(1)))
        return inpString

    if isinstance(inpString, unicode):
        # print '............ it is a UNICODE'
        inpString = unicode(inpString)

        # -----------------------------------------------
        # - Siamo qui solo se inpString è una Stringa
        # -----------------------------------------------
    # print '............ it is a STRING'
    if inpString.strip() == '': return inpString

        # ---------------------------------------------------
        # - Verifica se nell'ultimo TOKEN c'è un sepChar
        # ---------------------------------------------------
    if sepChars.find(inpString[-1]) >= 0:
        LAST_TOKEN = False
    else:
        LAST_TOKEN = True

        # ---------------------------------------------------
        # - Analisi delle atringa
        # ---------------------------------------------------
    while len(inpString) > 0:
        # print '...', inpString

            # ------------------------------------------------------------
            # - Se la posEND è > della lunghezza della stringa
            # - vuol dire che siamo alla fine della stringa.
            # - Aggiungiamo quanto rimane alla lista ed azzeriamo inpString
            # ------------------------------------------------------------
        if posEND >= len(inpString):
            listData.append(inpString)
            inpString = ''
            continue

            # -------------------------------------------------------------
            # - altrimenti preleviamo il char alla posizione posEND
            # -------------------------------------------------------------
        else:
            char = inpString[posEND]

            # -------------------------------------------------
            # - verifica che il char sia un QUOTE_CHAR
            # - Se lo è: cerca il compagno e se lo trova
            # - re-imposta il posEND a nuova posizione
            # -------------------------------------------------
        if quoteChars.find(char) >= 0:
            xx = inpString.find(char, posEND+1)
            if xx >= 0:
                posEND = xx

            # ----- altrimenti aggiungi la inpString fino al posEND alla lista
        elif sepChars.find(char) >= 0:
            listData.append(inpString[0:posEND])

            # ----- re-imposta inpString a partire da posEND
            inpString = inpString[posEND:].strip()
            if len(inpString) > 0 and sepChars.find(inpString[0]) >= 0:
                inpString = inpString[1:].strip()

            posEND = -1

        posEND += 1

    if not LAST_TOKEN:
        listData.append('')


        # ------------------------------------------------
        # - rimuovi tutti i Quote CHAR se esistono
        # - ma solo se sono all'inizio ed alla fine di ogni valore della lista
        # ------------------------------------------------
    retList = []
    for line in listData:
        line = gv.LN.string.stripQuote(gv, line)
        retList.append(line)


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return retList

