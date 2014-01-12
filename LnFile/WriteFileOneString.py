# #####################################
# # readFile
# #####################################
import os

# =========================================================================
# = 2013-02-12
# - writeFileOneString()
# = Write Data (String or LIST) to file
# =========================================================================
def writeFileOneString(gv, outFname, strData, exitOnError=False):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    retVal = 0
    try:
        FILE = open(outFname, "wb")
        FILE.write(strData)
        FILE.close()
        logger.info("file %s has been created" % (outFname))

    except (IOError, os.error), why:
        retVal = 1
        strError = "ERROR writing File [%s]:\n       %s" % (fName, str(why))
        logger.error(strError)
        if exitOnError:
            exit(8, strError, stackLevel=4)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return retVal
