#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import platform


OpSys = platform.system()
if OpSys == 'Windows':    import win32file



# ============================================
# = Given a directory, return the free space
# = (mega Bytes) on that drive.
# ============================================
def driveSpace(gv, dir, unit=''):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy

    logger.debug('entered - [called by:%s]' % (calledBy(1)))

    retValue = 0

    if OpSys == 'Windows':
        drive = os.path.splitdrive(dir)[0] + os.sep
        if not os.path.isdir(drive):
            logger.error( "Drive [%s] doesn't exists" % (drive) )
            logger.console( "Drive [%s] doesn't exists" % (drive) )
            return 0
        Bytes = getWindowsDriveFreeSpace(drive)

    else:
        Bytes = getLinuxDriveFreeSpace()

    KBytes = Bytes/1024.0
    MBytes = KBytes/1024.0
    GBytes = MBytes/1024.0
    if   unit == 'KB': retValue = KBytes
    elif unit == 'MB': retValue = MBytes
    elif unit == 'GB': retValue = GBytes
    else:              retValue = Bytes


    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return retValue

# ============================================
# = Given a directory, return the free space
# = (mega Bytes) on that drive.
# ============================================
def getWindowsDriveFreeSpace(drive):

    fs = win32file.GetDiskFreeSpace(drive)
    Bytes  = (fs[0]*fs[1]*fs[2])
    return Bytes


