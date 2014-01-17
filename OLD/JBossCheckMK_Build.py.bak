#!/usr/bin/python
# -*- coding: iso-8859-1 -*-


import subprocess
import sys, os
import shutil
import textwrap
import time


# ###################################################################################################################
# ###################################################################################################################
def copyTree(sourceDIR, destDIR):
    print "\n"
    print textwrap.dedent("""\
        Copy directory tree [%s]
                            [%s]
        """ % (sourceDIR, destDIR))

    if ACTION == '--GO':
        try:
            shutil.copytree(sourceDIR, destDIR)                 # La destDIR non deve esistere
        except (IOError, os.error), why:
            print textwrap.dedent("""\
                ERRORR copying directory tree [%s]
                                              [%s]
                Reason: %s
                """ % (sourceDIR, destDIR, str(why)))
            sys.exit(3)
    else:
        print "-----  was a DRY-RUN"



# ###################################################################################################################
# ###################################################################################################################
def chDir(dir):
    savedDir = os.getcwd()
    try:
        print "Moving to directory: %s" % (dir)
        os.chdir(zipDir)

    except (IOError, os.error), why:
        print ("ERROR changing directory [%s]:\n       %s" % (zipDir, str(why)) )
        sys.exit(4)

    return savedDir


# ###################################################################################################################
# ###################################################################################################################
def timeGetNow(GMT=False):
    if GMT:
        Tuple   = time.gmtime()
    else:
        Tuple   = time.localtime()

    # string  = time.strftime("%Y/%m/%d %H:%M:%S", Tuple)
    string  = time.strftime("%Y_%m_%d-%H_%M_%S", Tuple)
    return  string

    # secs    = time.mktime(Tuple)
    # return  secs




# ###################################################################################################################
# # TESTED 2013-02-11
# # http://docs.python.org/2/library/subprocess.html
# # The shell argument (which defaults to False) specifies whether to use the shell as the program to execute.
# #    If shell is True, it is recommended to pass args as a string rather than as a sequence.
# # Example:
# #       runProcess('ls', argsList=['-la'])
# ###################################################################################################################
def runCommand(command, wkdir, argsList=[], exit=False):

    CMD = command + ' ' + ' '.join(argsList)
    print ":::::::::::::::::::", os.path.normpath(wkdir)
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, cwd=wkdir)

    for line in iter(proc.stdout.readline, b''):
        print line,

    for line in iter(proc.stderr.readline, b''):
        print line,

    proc.communicate()





################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    if len(sys.argv) > 1:
        ACTION = sys.argv[1].upper()
    else:
        ACTION = ''
    mySEP = '/'

    thisModuleDIR   = os.path.dirname(os.path.realpath(__file__)).replace("\\", mySEP)
    scriptBase      = thisModuleDIR
    subDirsList     = thisModuleDIR.split(mySEP)
    PyProjectDIR     = mySEP.join(subDirsList[:-1])
    buildDIR        = mySEP.join([PyProjectDIR, 'build'])
    workingDIR      = mySEP.join([buildDIR, "Working"])                             # Working Directory
    PRJ_NAME        = "JBossCheck_MK"                          # Nome del Progetto e della dir con i sorgenti
    PRJ_PKGNAME     = "JBossCheck_MK"                          # Nome della root directory all'interno del tar e nome del tar.


    if not os.path.isdir(buildDIR):
        print "directory %s NOT Found." % (buildDIR)
        sys.exit(1)

    print textwrap.dedent("""\

            # =================================================================
            # - Removing Working Directory
            # =================================================================
        """)

    if os.path.isdir(workingDIR):
        if ACTION == '--GO':
            print "removing directory tree [%s]" % (workingDIR)
            shutil.rmtree(workingDIR, ignore_errors=True)
        else:
            print "directory tree [%s] would be removed." % (workingDIR)



    print textwrap.dedent("""\

            # =================================================================
            # = Effettua la copia dei sorgenti sulla dir di BUILD
            # =================================================================
        """)
    sourceDIR       = mySEP.join([PyProjectDIR, PRJ_NAME])
    destDIR         = mySEP.join([workingDIR, PRJ_PKGNAME])

    # print sourceDIR
    # print destDIR
    # sys.exit()
    copyTree(sourceDIR, destDIR)


    print textwrap.dedent("""\

            # =================================================
            # = Effettua una copia di LnPackage sulla dir di BUILD
            # =================================================
        """)
    LN_PKGNAME      = "LnFunctions"                                                # Nome del modulo che deve essere trasformato in pacchetto
    LnPackageDIR    = mySEP.join([PyProjectDIR, LN_PKGNAME])
    destDIR         = mySEP.join([workingDIR, PRJ_PKGNAME, "SOURCE",LN_PKGNAME ])
    copyTree(LnPackageDIR, destDIR)


    print textwrap.dedent("""\

            # =================================================
            # = Creating zipPackage
            # =================================================
        """)
    WIN = True
    if WIN == True:
        ZIPCMD  =   "PKZIP25.EXE"
        ZIPOPTS =   "-add=all  -dir=current -excl=*.pyc -incl=*.py -level=6 -zip=new -attr=all"
    else:
        ZIPCMD    =   "zip"
        ZIPOPTS   =   "-f  -x*.pyc -i*.py -1 -o -r"

    zipDir      = "%s/%s/SOURCE" % (workingDIR, PRJ_PKGNAME)
    zipName     = workingDIR + "/%s/bin/%s.zip" % (PRJ_PKGNAME, PRJ_PKGNAME)

    ZIP_CMD     = '%s %s "%s" "%s/*.*"' % (ZIPCMD, ZIPOPTS, zipName, zipDir)

    print "Executing...:", ZIP_CMD
    if ACTION == '--GO':
        runCommand(ZIP_CMD, wkdir=zipDir)



    print textwrap.dedent("""\

            # =================================================
            # = Removing SOURCE direcotry (before creating TAR
            # =================================================
        """)
    if ACTION == '--GO':
        appoDir  = mySEP.join([workingDIR, PRJ_PKGNAME, "SOURCE" ])
        print "removing directory tree [%s]" % (appoDir)
        shutil.rmtree(appoDir, ignore_errors=True)
    else:
        print "directory tree [%s] would be removed." % (workingDIR)


    print textwrap.dedent("""\

            # =================================================
            # = Creating tar package
            # =================================================
        """)
    tarInputDir =   workingDIR
    tarOutDir   =   buildDIR
    fileName    =   PRJ_NAME
    tarOutFile  =   mySEP.join([tarOutDir, fileName + ".tgz"])

    if os.path.isfile(tarOutFile):
        print "Il file %s esiste gia' ... renaming it" % (tarOutFile)
        now      = timeGetNow()
        newFname = mySEP.join([tarOutDir, "%s_%s.tgz" % (fileName, now)])
        os.rename(tarOutFile, newFname)

    TAR_CMD = "tar --exclude=*.cfgc --exclude=*/Exploded* -cvzf ../%s.tgz *" % (fileName)
    print "Executing...:", TAR_CMD
    if ACTION == '--GO':
        runCommand(TAR_CMD, wkdir=tarInputDir)

