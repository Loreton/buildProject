#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Funzioni per operare sul python dictionary
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import types



# #########################################################################################
# = Ritorna il puntamento ad un determinato punto del Dictionary
# = Se non esiste lo crea
# = keyList può essere [] oppure "key1;key2;   key3 ; key4]
# = Ritorna None: La keyList == [] oppure il dict non contiene KEYs
# #########################################################################################
def getDictPtr(gv, origDict, keyList="", fCREATE=False, fieldSep=';'):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.LnLogger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))


    if not type(origDict) == types.DictionaryType: return None

        # - Convertiamo il tipo di path passatoci ----
    if type(keyList) == types.StringType:
        KEYList = []
        for KEY in keyList.split(fieldSep):
            KEY = KEY.strip()
            if KEY != '':
                KEYList.append(KEY)

    elif type(keyList) == types.ListType:
        KEYList = keyList

    else:
        KEYList = []


        # - Cerchiamo il path ----
    retPtrDict = origDict

    for KEY in KEYList:
        if retPtrDict == None: continue                 # Cattura pointers NULL
        if  KEY in retPtrDict.keys():
            retPtrDict = retPtrDict[KEY]                       # puntiamolo

        else:
            if fCREATE:
                # retPtrDict[KEY] = {'%s CREATED NEW' % (KEY): True}
                retPtrDict[KEY] = {}
                retPtrDict = retPtrDict[KEY]
            else:
                retPtrDict = None
                break

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return retPtrDict


# #########################################################################################
# = Ritorna il valore di un campo di un dictionary
# #########################################################################################
def getDictValue(gv, origDict, fldName, keyList=""):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.LnLogger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))


    wkDict = getDictPtr(gv, origDict, keyList=keyList, fCREATE=False)
    if not wkDict:
        return None

    retVal = wkDict.get(fldName)

    logger.info('%s = %s' % (fldName, retVal))

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return retVal







if __name__ == "__main__":
    pippo =''
    myDict = {}
    myDict['key1'] = 'KEY1'
    myDict['Loreto1'] = {}
    myDict['Loreto1']['Loreto2'] = {"CIAO": 53}
    newDict = getDictPrt(myDict, keyList=['Loreto', 'Loreto2'], fCREATE=False)
    #newDict = getDictPrt(myDict, fCREATE=True)
    print newDict