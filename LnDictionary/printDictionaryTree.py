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
# -     MaxDeepLevel:   Indica il numero MAX di profondit� (iterazioni) da raggiungere
# -     values:         Indica se ritornare anche il valore delle keys
# -     lTAB:           Prefix a sinistra della riga
# -     retCols:         'LTV'
# -                        L  se vogliamo LevelCol
# -                        T  se vogliamo Type
# -                        V  se vogliamo Value
# -
# #########################################################################################
def printDictionaryTree(gv, dictID, header=None, MaxDeepLevel=999, level=0, retCols='LTV', lTAB='', console=False):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    lista = getDictionaryTree(dictID, MaxDeepLevel=MaxDeepLevel, level=level, retCols=retCols)

    if header:
        logger.info("*"*60)
        logger.info("*     %s" % (header) )
        logger.info("*"*60)
    for line in lista:
        logger.info("%s%s" % (lTAB, line) )

    if console:
        if header:
            print
            print lTAB + "*"*60
            print lTAB + "*     %s" % (header)
            print lTAB + "*"*60
        for line in lista:
            print "%s%s" % (lTAB, line)



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

# #########################################################################################
# - getDictionaryTree()
# -
# - PARAMS:
# -     level:          serve per tenere traccia delle iterazioni ed abche per l'indentazione
# -     MaxDeepLevel:   Indica il numero MAX di profondit� (iterazioni) da raggiungere
# -     values:         Indica se ritornare anche il valore delle keys
# -
# - RETURN: LIST of the keys with level indication:
# -            LVL TYPE       KeyName
# -            [0] dict       JbossColl
# -            [1] list           PATHS
# -            [1] str            Source System
# -            [1] str            Target System
# -            [0] int        LOG_CONSOLE
# -            [0] int        LOG_FILE
# -            [0] dict       Portit_DiscoL
# -            [1] dict           Flusso_DiscoL_With_BACKUP
# -            [2] list               PATHS
# -            [2] str                Source System
# -            [2] str                Target System
# -            [0] str        Type_of_Command
# -            [0] str        esil601
# -     Es.:
# -       [0] str          user.timezone                    : GMT+1
# -       [0] bool         javax.xml.jaxp-provider          : True
# -       [0] int          BdI.txn-status-manager.port      : 4713
# -
# - E' possibile utilizzarlo anche per leggere un modulo caricato con il comando:
# -         configFileID = loadConfigModule(Fname)
# -         CfgDict = vars(configFileID)        # con il comando vars trasformo il modulo in dictionary
# -
# -         lista = getDictionaryTree_Prev(vars(configFileID))
# -         lista = getDictionaryTree_Prev(CfgDict)
# #########################################################################################
# - L'idea � quella di stampare prima tutti i valori e poi andare all'interno dei dict
def getDictionaryTree(dictID, MaxDeepLevel=999, level=0, retCols='LTV'):
    lista = []
    if type(dictID) == types.InstanceType:  # devo scoprire come farne il print
        dictID = vars(dictID)

    if MaxDeepLevel < 0: return lista

    values = (True if 'V' in retCols else False)

    dictTYPES = [types.InstanceType, types.DictType]
    if not type(dictID) in dictTYPES:
        return lista

    # print '............................', type(dictID)
    for key, val in sorted(dictID.items()):
        valueTypeStr = str(type(val)).split("'")[1]
        valueType    = type(val)

        if key.startswith('__') and key.endswith('__'): continue    # elimina tutti i built-in (presente in un modulo)

        if valueType == types.ModuleType:
            continue                                # elimina eventuali import (presente in un modulo)

        newLine = "%s %s" % (' '*level*4, key)        # base della Linea
        if 'T' in retCols: newLine = "%-8s    %s" % (valueTypeStr, newLine)        # aggiungiamo il TYPE
        if 'L' in retCols: newLine = "[%2d] %s"   % (level, newLine)        # aggiungiamo il LEVEL

        if valueType in dictTYPES:
            continue

        if values:
            if valueType in [types.StringType, types.UnicodeType]:
                if val.strip() == '':
                    val = '"' + val + '"'
                newLine = "%-50s: %s" % (newLine.rstrip(), val.strip())
                lista.append(newLine)

            elif valueType == types.ListType:
                if len(val) == 0:
                    newLine = "%-50s: []" % (newLine.rstrip())
                    lista.append(newLine)
                elif len(val) == 1:
                    newLine = "%-50s: [%s]" % (newLine.rstrip(), val[0])
                    lista.append(newLine)
                else:
                    newLine = "%-50s: [" % (newLine.rstrip())   # Apertura LIST
                    lista.append(newLine)
                    counter = 0
                    for line in val:
                        if type(line) in dictTYPES:             # Dictionary interno ad una LIST
                            counter += 1
                            level += 1
                            lista.append('')
                            lista.append('[%2d] dict-%02d' % (level, counter))
                            newLista = getDictionaryTree(line, MaxDeepLevel=MaxDeepLevel-1, level=level+1, retCols=retCols)
                            lista.extend(newLista)
                            level -= 1
                            continue
                        newLine = "%-54s %s" % (' ', line)
                        lista.append(newLine)

                    lista.append('%-50s: ]' %(' ') )            # Cjhiusura LIST

            elif valueType == types.BooleanType or\
                 valueType == types.NoneType or\
                 valueType == types.IntType or\
                 valueType == types.FloatType or\
                 valueTypeStr == "datetime.date":
                newLine = "%-50s: %s" % (newLine.rstrip(), val)
                lista.append(newLine)

            else:
                lista.append(newLine)

        else:
            lista.append(newLine)

    lista.append('')    # separator

        # Analisi di tutte le chiavi che sono a livello ddel dictionary.

    for key, val in sorted(dictID.items()):
        valueTypeStr = str(type(val)).split("'")[1]
        valueType    = type(val)

        if key.startswith('__') and key.endswith('__'): continue    # elimina tutti i built-in (presente in un modulo)

        if valueType == types.ModuleType: continue                                # elimina eventuali import (presente in un modulo)

        newLine = "%s %s" % (' '*level*4, key)        # base della Linea
        if 'T' in retCols: newLine = "%-8s    %s" % (valueTypeStr, newLine)        # aggiungiamo il TYPE
        if 'L' in retCols: newLine = "[%2d] %s"   % (level, newLine)        # aggiungiamo il LEVEL


        if valueType in dictTYPES:
            lista.append(newLine)
            if valueType == types.InstanceType:
                newLista = getDictionaryTree(vars(val), MaxDeepLevel=MaxDeepLevel-1, level=level+1, retCols=retCols)
            else:
                newLista = getDictionaryTree(val, MaxDeepLevel=MaxDeepLevel-1, level=level+1, retCols=retCols)
            lista.extend(newLista)
            lista.append('')

    return lista




def printObject(object):
    for i in [v for v in dir(object) if not callable(getattr(object,v))]:
        print '\n%s:' % i
        exec('print object.%s\n\n') % i