#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import sys;         sys.dont_write_bytecode = True
import platform;    OpSys                = platform.system()
import shutil
import textwrap

import Functions as LN

# Nomi progetti per cui i package possono essere accorpati sotto lo stenno nome
CMK_Common62x   = ['JBoss610_CMK', 'JBoss620_CMK', 'JBoss621_CMK']
Admin_Common62x = ['JBoss610_Admin', 'JBoss620_Admin', 'JBoss621_Admin']
NO_LN_PACKAGE   = ['JBoss610_Admin']



################################################################################
# - getPackageName()
################################################################################
def getPackageName(PRJ_NAME):
        # valori di default
    PRJ_PKGNAME = PRJ_NAME                          # Nome della root directory all'interno del tar e nome del tar.
    LN_PKGNAME  = 'LnFunctions'                        # Nome della directory contenente le funzioni generali

        # ----- Package NAME
    if PRJ_NAME in  CMK_Common62x:        PRJ_PKGNAME = 'JBossCMK'
    if PRJ_NAME in  Admin_Common62x:      PRJ_PKGNAME = 'JBossAdmin'

        # ----- LnPackage NAME

    if   PRJ_NAME in NO_LN_PACKAGE:     LN_PKGNAME = None                     # Nome della directory contenente le funzioni generali
    elif PRJ_NAME == 'JBoss610_Admin':  LN_PKGNAME = "LnFunctions610"                     # Nome della directory contenente le funzioni generali



    return PRJ_PKGNAME, LN_PKGNAME


################################################################################
# - getZipFname()
################################################################################
def getZipFname(PRJ_NAME):
        # valori di default
    ZIP_FNAME = PRJ_NAME

    if   PRJ_NAME in  CMK_Common62x:      ZIP_FNAME = 'JBossCMK'
    elif PRJ_NAME in  Admin_Common62x:    ZIP_FNAME = 'JBossAdmin'


    return ZIP_FNAME



################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":

    ACTION  = ''
    gOPTION = '--GO'
    vOPTION = '--verbose'
    VERBOSE = False

    if len(sys.argv) == 1:
        print "\n"*2
        print '%s [%s] %s [%s]' % (sys.argv[0], vOPTION, "\"Directory del progetto\"", gOPTION)
        print "\n"*2
        sys.exit()

    if sys.argv[1].upper() == vOPTION.upper():
        VERBOSE = True
        if len(sys.argv) > 2:
            PRJ_NAME = sys.argv[2]
        else:
            print "\n"*2
            print '%s [%s] %s [%s]' % (sys.argv[0], vOPTION, "\"Directory del progetto\"", gOPTION)
            print "\n"*2
            sys.exit()
        if len(sys.argv) > 3:
            ACTION   = sys.argv[3].upper()
    else:
        PRJ_NAME = sys.argv[1]
        if len(sys.argv) > 2:
            ACTION  = sys.argv[2].upper()


    (PRJ_PKGNAME, LN_PKGNAME) = getPackageName(PRJ_NAME)


    mySEP = '/'

    thisModuleDIR       = os.path.dirname(os.path.realpath(__file__)).replace("\\", mySEP)
    scriptBase          = thisModuleDIR
    subDirsList         = thisModuleDIR.split(mySEP)
    rootDIR             = mySEP.join(subDirsList[:-1])
    buildDIR            = mySEP.join([rootDIR, '_BUILD_DIR'])
    workingDIR          = mySEP.join([buildDIR, "Working"])                             # Working Directory
    projectSourceDIR    = mySEP.join([rootDIR, PRJ_NAME])                             # Working Directory


    if not os.path.isdir(buildDIR):
        print "directory %s NOT Found." % (buildDIR)
        sys.exit(1)

    if not os.path.isdir(projectSourceDIR):
        print "directory %s NOT Found." % (projectSourceDIR)
        sys.exit(1)



    msg = textwrap.dedent("""\
            # =================================================================
            # - Removing Working Directory
            # =================================================================
        """); print '\n' + msg
    if os.path.isdir(workingDIR):
        if ACTION == '--GO':
            print "removing directory tree [%s]" % (workingDIR)
            LN.delTree(workingDIR, VERBOSE)
        else:
            print "directory tree [%s] would be removed." % (workingDIR)



    msg = textwrap.dedent("""\
            # =================================================================
            # = Effettua la copia dei sorgenti sulla dir di BUILD
            # =================================================================
            """); print '\n' + msg
    sourceDIR       = projectSourceDIR
    destDIR         = mySEP.join([workingDIR, PRJ_PKGNAME])
    print "%s --> %s" % (sourceDIR, destDIR)
    if OpSys.upper() == 'WINDOWS':
        ignoreFunc = shutil.ignore_patterns('*.git*', 'tmp*', '*.json', '*.fmted', 'rpdb2.py', '*.sh' )
    else:
        ignoreFunc = shutil.ignore_patterns('*.git*', 'tmp*', '*.json', '*.fmted', 'rpdb2.py', '*.cmd' )

    if ACTION == '--GO':
        LN.copyTree(sourceDIR, destDIR, ignore=ignoreFunc)


    if LN_PKGNAME:
        msg = textwrap.dedent("""\
                # =================================================================
                # = Effettua una copia di LnPackage sulla dir di BUILD
                # =================================================================
                """);print '\n' + msg
        sourceDIR       = mySEP.join([rootDIR, LN_PKGNAME])
        destDIR         = mySEP.join([workingDIR, PRJ_PKGNAME, "SOURCE", LN_PKGNAME ])
        print "%s --> %s" % (sourceDIR, destDIR)
        if OpSys.upper() == 'WINDOWS':
            ignoreFunc = shutil.ignore_patterns('*.git*', 'tmp*', '*.json', '*.fmted', 'rpdb2.py', '*.sh' )
        else:
            ignoreFunc = shutil.ignore_patterns('*.git*', 'tmp*', '*.json', '*.fmted', 'rpdb2.py', '*.cmd' )

        if ACTION == '--GO':
            LN.copyTree(sourceDIR, destDIR, ignore=ignoreFunc)



    msg = textwrap.dedent("""\
            # =================================================================
            # = Creating zipPackage
            # =================================================================
            """); print '\n' + msg
    sourceDIR   = mySEP.join([workingDIR, PRJ_PKGNAME, "SOURCE"])
    zipName     = "%s/%s/bin/%s.zip" % (workingDIR, PRJ_PKGNAME, getZipFname(PRJ_NAME))
    print "creating zipFile:", zipName
    print "  with directory:", sourceDIR
    excludePattern = ['.git' + os.sep]
    includePattern = ['*.py']
    if ACTION == '--GO':
        myZip = LN.LnZip()
        myZip.open(zipName)
        myZip.addFolderToZip(sourceDIR, include=includePattern, exclude=excludePattern, emptyDir=False, hiddenDir=False)
        myZip.close()



    msg = textwrap.dedent("""\
            # =================================================================
            # = Removing SOURCE direcotry (before creating TAR
            # =================================================================
            """); print '\n' + msg
    appoDir  = mySEP.join([workingDIR, PRJ_PKGNAME, "SOURCE" ])
    if ACTION == '--GO':
        print "removing directory tree [%s]" % (appoDir)
        LN.delTree(appoDir, VERBOSE)
    else:
        print "directory tree [%s] would be removed." % (appoDir)

    msg = textwrap.dedent("""\
            # =================================================================
            # = Creating tar package
            # =================================================================
            """); print '\n' + msg

    tarInputDir =   workingDIR
    tarOutDir   =   buildDIR
    fileName    =   PRJ_NAME
    tarOutFile  =   mySEP.join([tarOutDir, fileName + ".tgz"])

    if os.path.isfile(tarOutFile):
        print "Il file %s esiste gia' ... renaming it" % (tarOutFile)
        now      = LN.timeGetNow()
        newFname = mySEP.join([tarOutDir, "%s_%s.tgz" % (fileName, now)])
        os.rename(tarOutFile, newFname)

    EXcludeFromTAR = ['*.cfgc', '*/Exploded*', '*/.git*', 'LICENSE', 'README.md', '*.psproj', '*/data/*']
    excludePattern = ''
    for pattern in EXcludeFromTAR:
        excludePattern += ' --exclude=%s' % (pattern)

    if VERBOSE:
        TAR_CMD = "tar %s -cvzf %s *" % (excludePattern, tarOutFile)
    else:
        TAR_CMD = "tar %s -czf %s *" % (excludePattern, tarOutFile)

    print "Executing...:", TAR_CMD

    if ACTION == '--GO':
        LN.runCommand(TAR_CMD, wkdir=tarInputDir)

    sys.exit()
    msg = textwrap.dedent("""\
            # =================================================================
            # - Removing Working Directory
            # =================================================================
            """); print '\n' + msg

    if os.path.isdir(workingDIR):
        if ACTION == '--GO':
            print "removing directory tree [%s]" % (workingDIR)
            LN.delTree(workingDIR, VERBOSE)
        else:
            print "directory tree [%s] would be removed." % (workingDIR)


    if ACTION == '--GO':
        print "\n"*3
        print "TGZ file is ready: %s" % (tarOutFile)
        print "\n"*3

