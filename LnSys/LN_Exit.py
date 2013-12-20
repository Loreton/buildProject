import types, os, inspect, sys

EXIT_KEYB   = -30
PAUSE_KEYB   = -31
EXIT_STACK  = -32

# =======================================================================
# - 13 Maggio 2010  : Aggiunto il parametro stackLevel
# =======================================================================
def exit(gv, rcode, text, stackLevel=2):
    Prj         = gv.Prj
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    if isinstance(text, types.ListType):
        textList = text
        pass
    else:
        textList = text.split('\n')


        # -------------------------------
        # - Display dell'Errore
        # -------------------------------
    logger.info("Rcode: %d" % (rcode))
    for line in textList:
        logger.info("      Msg=%s" % (line))


    if rcode == EXIT_STACK:
        print '\n'*3
        print '*'*60
        traceback.print_stack()
        print '*'*60

    else:
        logger.info("\n"*4)
        logger.info("*" + "== EXIT =="*8)
        logger.info("*")

        callerPrint(gv, stackLevel, rcode, BlankLINES=0, Indent="=     * ")
        if rcode == 0:
            logger.info("* %s!" % (textList))
        else:
            logger.error("*     * ERROR: Rcode...: %d" % (rcode))
            # print '.............',textList
            for line in textList:
                logger.error("=     * ERROR: Message.: %s!" % (line))

        logger.info("*")
        logger.info("#"*40)


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
    sys.exit(rcode)


def callerPrint(gv, deepLevel=1, rcode=0, BlankLINES=5, Indent="=     "):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    caller = inspect.stack()[deepLevel]
    programFile = caller[1]
    lineNumber  = caller[2]
    funcName    = caller[3]
    if caller[4]:
        lineCode = caller[4][0]
    else:
        lineCode = 'UNKNOWN source line code'

    lun = len(lineCode) + 25
    lun = len(lineCode) + 5

    riga = []
    riga.append("\n"*BlankLINES)
    riga.append("%s" % (Indent) + "-"*lun)
    riga.append("%s" % (Indent) + "         C A L L E R")
    riga.append("%s" % (Indent))

    fname = os.path.basename(programFile).split('.')[0]
    riga.append("%s %-10s: %s.%s:[%s]" % (Indent, "called by:",        fname, funcName, lineNumber))
    riga.append("%s %-10s: %s" % (Indent, "Line code",           lineCode.strip()))
    riga.append("%s" % (Indent) + "-"*lun)
    riga.append("")

    for line in riga:
        if rcode == 0:
            logger.info(line)
        else:
            logger.error(line)

    logger.info('exiting - [called by:%s]' % (calledBy(1)))