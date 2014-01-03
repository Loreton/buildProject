#!/usr/bin/python -O
# -*- coding: utf-8 -*-
# ......... -*- coding: latin-1 -*-

# import xlrd
import xlwt

def open(gv, filename):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.debug('entry   - [called by:%s]' % (calledBy(1)))

    try:
        logger.info('reading file: %s' % (filename))
        WkBook  = xlwt.Workbook()
        WkSheet = WkBook.add_sheet('MP3_Catalog', cell_overwrite_ok=True)

    except StandardError, why:
        Prj.exit(gv, 9000, "error reading file: %s [%s]" % (filename, why))


        # --------------------------------------------
        # - Creazione del file di Output
        # --------------------------------------------


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return wb
