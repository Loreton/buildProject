import types, os, inspect, sys

EXIT_KEYB   = -30
PAUSE_KEYB   = -31
EXIT_STACK  = -32

# =======================================================================
# - 13 Maggio 2010  : Aggiunto il parametro stackLevel
# =======================================================================
def exit(gv, rcode, text, stackLevel=2):
    Prj         = gv.Prj
    LN         = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    if text == None:
        textList = ['No error message passed']
    elif isinstance(text, types.ListType):
        textList = text
        pass
    else:
        textList = text.split('\n')

        # -------------------------------
        # - Display dello STACK
        # -------------------------------
    logger.console(LN.cGREEN + "[EXIT called by (STACK):")
    for i in range(1, 10):
        caller = calledBy(i)
        if caller != 'list index out of range':
            logger.console(LN.cGREEN + "    %s" % (caller))

        # -------------------------------
        # - Display dell'Errore
        # -------------------------------
    if rcode == 0:
        TEXT_COLOR = LN.cGREEN
    else:
        TEXT_COLOR = LN.cERROR


    logger.console(TEXT_COLOR + "[RCODE: %d]" % (rcode))
    logger.console(TEXT_COLOR + "[TEXT Message:]" )
    for line in textList:
        logger.console(LN.cWARNING + ' '*10 + "%s" % (line))


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    sys.exit(rcode)


def callerPrint(gv, deepLevel=1, rcode=0, BlankLINES=5, Indent="=     "):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entered - [called by:%s]' % (calledBy(1)))

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

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))