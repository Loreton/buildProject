# #####################################
# # readFile
# #####################################
import os

#############################################################################################
# = 2013-02-12
# - readFileOneLine()
# - Legge un file ascii e lo ritorna come stringa unica eliminando le righe commentate
#############################################################################################
def readAsciiFile(gv, fname, lineCmntStr=None, stripLine=True, exitOnError=False, oneLine=False):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    Row = []

    try:
        f = open(fname,"r")
        for line in f:

            if stripLine: line = line.strip()

            if lineCmntStr and line.strip() != ''  and line.strip()[0] == lineCmntStr:
                continue

            line = line.strip('\n')
            Row.append(line)

        f.close()

    except (IOError, os.error), why:
        if logger: logger.error("ERROR reading File [%s]:\n       %s" % (fname, str(why)))
        if exitOnError: exit(8, "ERROR reading File [%s]:\n       %s" % (fname, str(why)), stackLevel=4 )


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    if oneLine:
        text = '\n'.join(Row)
        return text
    else:
        return Row
