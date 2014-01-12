#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################

import os, sys
import imp


# #########################################################################################
# - loadDictFile(cfgFileName, moduleName=None, fDEBUG=False)
# - Load di un modulo di configurazione (sintassi python-dictionary)
# - e lo ritorna in formato dictionary
# - [moduleName] non deve contenere il '.'
# #########################################################################################
# import LnFunctions as LN

def loadDictFile(gv, cfgFileName, moduleName=None, fDEBUG=False):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    paths = []
    if os.path.isabs(cfgFileName):      # Se è un path assoluto
        paths.append(cfgFileName)
    else:                               # cerchiamolo da qualche parte
        currPythonPATH = os.getenv('PYTHONPATH')
        if currPythonPATH: paths.extend(currPythonPATH.split(os.pathsep))
        paths.extend(sys.path)        # Aggiungiamo le sys.path

    logger.debug("searching file: [%s]" % (cfgFileName))

    FILE_FOUND  = False
    dictID      = None
    module      = None

    if not moduleName:
        FileName = os.path.basename(cfgFileName)
        moduleName = "MODULE_%s" % (FileName)
        moduleName = moduleName.replace('.', '_')

    logger.debug("moduleName: [%s]" % (moduleName))

    for path in paths:
        fullPath = os.path.join(path, cfgFileName)
        logger.debug("searching on PATH:%s" % (path))

        if os.path.isfile(fullPath):
            FILE_FOUND = True
            (scriptDir, FileName) = os.path.split(os.path.abspath(fullPath))

            logger.info("Reading file: %s as ModuleName:%s" % (cfgFileName, moduleName))

            try:
                module = imp.load_source(moduleName, fullPath)
                dictID = vars(module)

            except Exception, why:
                message = "Error loading file:%s - [%s]" % (fullPath, why)
                logger.error(message)
                print (message)
                sys.exit()

            break

        else:
            logger.error("File NOT found: %s" % (cfgFileName))

        # ritorniamo il dictionary, il path del file ed il path completo
    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return module, dictID, path, fullPath


