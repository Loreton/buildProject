# ##############################################################################################
# - writeFile()
# -*- coding: iso-8859-1 -*-
# -                                        by: Loreto Notarantonio (2010-02-16)
# ##############################################################################################
import os
import types
import unicodedata
# =========================================================================
# = 2013-02-12
# = Write Data (String or LIST) to file
# =========================================================================
def writeFile(gv, outFname, data, append=True, commentStr=False, lineSep='\n'):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))
    pColor      = gv.LN.sys.colors()

    if commentStr == True:
        if logger:
            logger.debug("-"*60)
            logger.debug("Writing file %s" % (outFname) )
            logger.debug("-"*60)

    try:
        if append:
            FILE = open(outFname, "a")
        else:
            FILE = open(outFname, "wb")

        if isinstance(data, types.ListType):
            for line in data:
                if commentStr == True: logger.debug(line)
                FILE.write(line + lineSep)

        elif isinstance(data, types.StringType):
            FILE.write(data)

        else:
            logger.error( "TYPE=[%s] NON contemplato... Provvedere ad inserirlo" % (type(val)) )

        FILE.close()

    except (IOError, os.error), why:
        strError = "ERROR reading File [%s]:\n       %s" % (outFname, str(why))
        logger.error(strError)
        exit(8, strError, stackLevel=4 )

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))

    return

# =========================================================================
# = 2013-02-12
# = Write Data (String or LIST of LIST) to file - Da problemi con caratteri speciali
# =========================================================================
def writeFile_ListOfList(gv, outFname, data, append=True, commentStr=False, lineSep='\n'):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    try:
        if append:
            FILE = open(outFname, "a")
        else:
            FILE = open(outFname, "wb")

        if isinstance(data, types.ListType):
            for line in data:

                if isinstance(line, types.ListType):
                    print '.........', line
                    for item in line:
                        print '.........', item
                        # xx = unicodedata.normalize('NFKD', str(item)).encode('ascii', 'ignore')
                        FILE.write(item + ';')
                    FILE.write(lineSep)

                else:
                    FILE.write(line + lineSep)

        elif isinstance(data, types.StringType):
            FILE.write(data)

        else:
            logger.error( "TYPE=[%s] NON contemplato... Provvedere ad inserirlo" % (type(val)) )

        FILE.close()

    except (IOError, os.error), why:
        strError = "ERROR reading File [%s]:\n       %s" % (outFname, str(why))
        logger.error(strError)
        exit(8, strError, stackLevel=4 )

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))

    return




