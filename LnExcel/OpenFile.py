#!/usr/bin/python -O
# -*- coding: utf-8 -*-
# ......... -*- coding: latin-1 -*-

import xlrd

def open(gv, filename):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entry   - [called by:%s]' % (calledBy(1)))

    try:
        logger.info('reading file: %s' % (filename))
        wb      = xlrd.open_workbook(filename)

    except StandardError, why:
        Prj.exit(gv, 9000, "error reading file: %s [%s]" % (filename, why))


    logger.info('exiting - [called by:%s]' % (calledBy(1)))
    return wb
