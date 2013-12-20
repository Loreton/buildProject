#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import shutil

# =================================================================
# - Copy directory
# =================================================================
def createDir(gv, path, exitOnError=False):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy

    logger.info('entered - [called by:%s]' % (calledBy(1)))

    logger.info( "Creating directory: [%s]" % (path) )

    if os.path.isdir(path):
        logger.error( "Source directory already exists [%s]" % (path) )
        return False

    try:
        os.makedirs(path)           # La dir non deve esistere
        logger.info( "Created  directory: [%s]" % (path) )

    except (IOError, os.error, WindowsError), why:
        msg = "Can't COPY Subtree [%s] to [%s]: %s" % (srcPATH, dstPATH, str(why))
        logger.warning(msg)
        if exitOnError:
            Ln.sys.exit(9001, msg)
        return False

    logger.info('exiting - [called by:%s]' % (calledBy(1)))
    return  True

