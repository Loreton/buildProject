# #####################################
# # readIniFile
# #####################################
# import LnPackage as Ln

#############################################################################################
# = 2013-02-12
# - readBinaryFile()
# - Legge un file e lo ritorna come stringa unica
#############################################################################################
def readBinaryFile(gv, fname, exitOnError=False):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    text = ''
    try:
        f = open(fname,"r")
        text = f.read()
        f.close()

    except (IOError, os.error), why:
        if logger: logger.error("ERROR reading File [%s]:\n       %s" % (fname, str(why)))
        if exitOnError: exit(8, "ERROR reading File [%s]:\n       %s" % (fname, str(why)), stackLevel=4 )

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return text
