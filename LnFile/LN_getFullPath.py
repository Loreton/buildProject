import os, sys
import types
# =========================================================================
# = Ricerca del path completo di un file nel path indicato.
# = Comunque viene ricercato anche nelle sys.path[]
# = search_path:
# =       un nome di variabile
# =       un insieme di percorsi separati da os.pathsep
# =========================================================================
def getFullPath(gv, filename, pathEnv='PATH', exitOnError=False):
    i = 0
    LN          = gv.LN
    logger      = LN.logger
    calledBy    = LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))
    # i+=1; print '................', str(i)*20

    if not os.path.isfile(filename):
        retPath = None
            # ------------------------------------------------------------------------------
            # - Verifica che il search_path non sia a sua volta una variabile d'ambiente
            # - Non ricordo dove viene usato.
            # ------------------------------------------------------------------------------
        variableValue = os.getenv(pathEnv)             # check it in Env Variables
        pythonPaths = os.getenv('PYTHONPATH')        # get PYTHONPATH env

        if variableValue:
            myPaths = variableValue
        else:
            myPaths = pathEnv

        paths = (myPaths + os.pathsep + pythonPaths).split(os.pathsep)

        # paths = myPaths.split(os.pathsep)
        paths.extend(sys.path)      # Aggiungiamo le sys.path come default


        for path in paths:
            # i+=1; print '................', str(i)*20, path, filename

            # fullName = os.path.join(path, filename) # mi da problemi con il DEBUGGER pyscripter
            fullName = path + os.path.sep + filename
            if os.path.isfile(fullName):
                retPath = os.path.abspath(fullName)
                break
    else:
        retPath = filename

    if retPath:
        # i+=1; print '................', str(i)*20
        logger.debug("PATH found for %s: %s" % (filename, retPath))
    else:
        msg =  "PATH NOT found for: %s" % (filename)
        logger.error(msg)
        if exitOnError:
            LN.sys.exit(gv, 9008, msg)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    # i+=1; print '................', str(i)*20
    return retPath
