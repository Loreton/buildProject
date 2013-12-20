#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# ##############################################################################################
# - dirList()
# - CALL:
# -     files = dirList('d:\TMP', pattern='*sterni*.txt|*2011-07-27*.txt', getFullPath=True )
# - return: LIST of FileNames
# -                                        by: Loreto Notarantonio (2010-02-16)
# ##############################################################################################
import os, fnmatch

# ============================================================
# Return a list of file names found in directory 'dirName'
#    pattern: "*.x; *x*.y*" ....
#   deepFileIndicator   - è un nome di file che, se trovato, vuol dire che abbiamo raggiunto il livello massimo
#   deepLevelNO         - Numero di livello (subtree) da analizzare
#
# Example usage: fileList = dirList('H:\TEMP', '*.txt', 'F')
#       Only files with 'txt' extensions will be added to the list.
# Example usage: fileList = dirList('H:\TEMP', '*.txt;*.tx*', 'FS')
#       Only files with 'txt' extensions will be added to the list. Search in all Subdirs.
# Example usage: fileList = dirList('H:\TEMP', '*txt*', 'D')
#       Only Directories with 'txt' extensions will be added to the list.
#
# ============================================================
def dirList(gv, dirName, pattern='*', what='FDS', getFullPath=True, deepFileIndicator='1234ABCD.ZXC', deepLevelNO=99, static_MaxRCODE=[0]):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))

    fileList    = []
    fDEBUG      = False
    MaxRCODE    = 0

    FILES       = True if 'F' in what else False
    SUBDIRS     = True if 'S' in what else False
    DIRS        = True if 'D' in what else False


    deepLevelNO -= 1
    logger.debug("entering into dir: %s searching for %s" % (dirName, pattern) )


        # limit the Subdirs at current level (The next iteration do not enter into SubDirs)    - da aggiustare
    if os.path.isfile(os.path.join(dirName, deepFileIndicator) ):
        what = what.replace('S', '')    # Eliminiamo il il SUBDIRs
    if deepLevelNO < 0:
        return fileList


    # -----------------------------------------------
    # - file      = name of file without FullPath
    # - dirfile   = name of file with    FullPath
    # -----------------------------------------------
    try:
        for file in os.listdir(dirName):
            for fSpec in pattern.split(';'):        # Splitting the pattern
                fSpec = fSpec.strip()
                dirfile = os.path.join(dirName, file)
                if fnmatch.fnmatch(file, fSpec):    # cerca il MATCH nel nome del file
                    if FILES  and os.path.isfile(dirfile):
                        if getFullPath: fileList.append( dirfile)
                        else:           fileList.append( file)
                    elif DIRS and os.path.isdir(dirfile):
                        if getFullPath: fileList.append( dirfile)
                        else:           fileList.append( file)

                if SUBDIRS and os.path.isdir(dirfile):
                    if fDEBUG == True: logger.console("going into dir: %s\\%s" % (dirfile, fSpec) )
                    (rCode, newList) = dirList(gv, dirfile, pattern=fSpec, what=what, getFullPath=getFullPath, deepFileIndicator=deepFileIndicator, deepLevelNO=deepLevelNO)
                    MaxRCODE = max(MaxRCODE, rCode)
                    fileList.extend(newList)

    except StandardError, why:
        if dirName.find('System Volume Information') >= 0:
            pass
        else:
            logger.error("Listing directory:\n [%s%s%s]\n\n %s" % (dirName, os.sep, pattern, str(why)))
            MaxRCODE = max(MaxRCODE, 10)


    logger.info("exiting  from dir: %s" % (dirName) )
    return MaxRCODE, fileList


















def dirList_OK(gv, dirName, pattern='*', getFullPath=False):
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))
    pColor      = gv.LN.sys.colors()

    fileList = []

    pattern = pattern.split('|')

    try:
        listaFiles = os.listdir(dirName)
    except StandardError, why:
        if dirName.find('System Volume Information') >= 0:      # Per windows
            pass
        else:
            errMsg = "ERROR Listing directory:\n [%s%s%s]\n\n %s" % (dirName, os.sep, pattern, str(why))
            logger.error (errMsg)
            print (errMsg)
            return []


    fileList    = []
    logger.info('[%4d] total files' % (len(listaFiles)))
    for file in listaFiles:
        for fSpec in pattern:
            if fnmatch.fnmatch(file, fSpec):                      # cerca il MATCH nel nome del file
                fullFname = os.path.join(dirName, file)
                if os.path.isfile(fullFname):
                    if getFullPath: fileList.append( fullFname)
                    else:           fileList.append( file)

    logger.info('[%4d] matching pattern' % (len(fileList)))

    logger.info('exiting - [called by:%s]' % (calledBy(1)))
    return fileList

