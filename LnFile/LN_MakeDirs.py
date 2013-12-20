#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os


def makeDirs(gv, path, exitOnError=False):
    LN = gv.LN
    Prj = gv.Prj
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    bError = True

    if path == '':
        logger.error("How can I create a directory with NO-NAME??? [%s]" % (path))
        return bError

    if path.lower().startswith('/cygdrive/'):
        path = path[10:]
        path = path[:1] + ':' + path[1:]

    if not os.path.isdir(path):
        logger.debug("creating directory [%s] " % (path))

        try:
            os.makedirs(path)
            bError = False

        except (IOError, os.error), why:
            msg = "ERROR creating directory [%s]:\n       %s" % (`path`, str(why))
            logger.error(msg)
            bError = True
            if exitOnError:
                Prj.exit(gv, 1001, msg)

    else:
        logger.debug("directory [%s] already exists" % (path))
        bError = False

    return bError
