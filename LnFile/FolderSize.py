#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os

# =================================================================
# - get Folder Size
# =================================================================
def getFolderSize(gv, folder):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy

    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    folder_size = 0
    for (path, dirs, files) in os.walk(folder):
        for file in files:
            filename = os.path.join(path, file)
            folder_size += os.path.getsize(filename)

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))

    return folder_size

