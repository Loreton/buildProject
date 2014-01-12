#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import shutil
import glob

# =================================================================
# - Copy multiple files to single file
#
# copyFile(gv, srcPATH="D:/temp/LnFile", srcFile='*',             dstPATH="D:/tmp/LnFileDest", dstFile='pippo.cfg', exitOnError=False)
# copyFile(gv, srcPATH="D:/temp/LnFile", srcFile='_*',            dstPATH="D:/tmp/LnFileDest", dstFile='pippo.cfg', exitOnError=False)
# copyFile(gv, srcPATH='D:/temp/LnFile', srcFile="LN_CopyDir.py", dstPATH="D:/tmp/LnFileDest", dstFile='pippo.cfg', exitOnError=False)
# =================================================================
def copyFile(gv, srcPATH=None, dstPATH=None, srcFile=None,  dstFile=None, createDir=False, exitOnError=False):
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    logger.debug( "srcPATH....: %s" % (srcPATH) )
    logger.debug( "srcFile....: %s" % (srcFile) )
    logger.debug( "dstPATH....: %s" % (dstPATH) )
    logger.debug( "dstFile....: %s" % (dstFile) )

    errMsg = None
    if not srcPATH:
        errMsg = "Missing source directory parameter"

    elif not os.path.isdir(srcPATH):
        errMsg = "Source directory doesn't exists [%s]" % (srcPATH)

    elif not srcFile:
        errMsg = "Missing source file parameter"

    if errMsg:
        logger.error(errMsg)
        if exitOnError:
            LN.sys.exit(gv, 9003, errMsg)
        print LN.cERROR + errMsg
        return False

    if '*' in srcFile: dstFile = None

    try:
        if not os.path.isdir(dstPATH):
            if createDir:
                logger.info('creating directory:%s' % (dstPATH))
                os.makedirs(dstPATH)               # non posso farlo per il subTree
            else:
                msg = "Directory [%s] doesn't exists. Use createDir=True if you want it to be created." % (dstPATH)
                logger.warning(msg)
                if exitOnError:
                    LN.sys.exit(gv, 9002, msg)
                return False

        if dstFile: dstPATH = "%s/%s" % (dstPATH, dstFile)
        for filename in glob.glob("%s/%s" % (srcPATH, srcFile)):
            msg = 'copying %s -> %s' % (filename, dstPATH)
            logger.debug(msg)
            # print LN.cYELLOW + msg
            shutil.copy2(filename, dstPATH)

    except (IOError, os.error), why:
        msg = "Can't COPY [%s/%s] to [%s]: %s" % (srcPATH, srcFile, dstPATH, str(why))
        logger.warning(msg)
        if exitOnError:
            LN.sys.exit(gv, 9002, msg)
        return False

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))
    return True



################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":

    copyFile(gv, srcPATH="D:/temp/LnFile", srcFile='*',             dstPATH="D:/tmp/LnFileDest", dstFile='pippo.cfg', exitOnError=False)
    copyFile(gv, srcPATH="D:/temp/LnFile", srcFile='_*',            dstPATH="D:/tmp/LnFileDest", dstFile='pippo.cfg', exitOnError=False)
    copyFile(gv, srcPATH='D:/temp/LnFile', srcFile="LN_CopyDir.py", dstPATH="D:/tmp/LnFileDest", dstFile='pippo.cfg', exitOnError=False)

