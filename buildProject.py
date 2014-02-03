#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
import os
import sys;         sys.dont_write_bytecode = True
import platform;    OpSys                = platform.system()
import subprocess
import shutil
import textwrap
import time, zipfile

import Functions as LnFuncs


# ####################################################################################################################
def copyTree(src, dst, symlinks=False, ignore=None):
# ###################################################################################################################
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    # if not os.path.isdir(dst): os.makedirs(dst)
    os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                shutil.copytree(srcname, dstname, symlinks, ignore)
            else:
                shutil.copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error as err:
            errors.extend(err.args[0])
    try:
        shutil.copystat(src, dst)

    except WindowsError, why:
        print "ERROR: %s" % (why)
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))
    if errors:
        raise shutil.Error(errors)

# ###################################################################################################################
def chDir(dir):
# ###################################################################################################################
    savedDir = os.getcwd()
    try:
        print "Moving to directory: %s" % (dir)
        os.chdir(zipDir)

    except (IOError, os.error), why:
        print ("ERROR changing directory [%s]:\n       %s" % (zipDir, str(why)) )
        sys.exit(4)

    return savedDir


# ###################################################################################################################
def timeGetNow(GMT=False):
# ###################################################################################################################
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
def runCommand(command, wkdir, argsList=[], exit=False):
# ###################################################################################################################

    CMD = command + ' ' + ' '.join(argsList)
    print "::", os.path.normpath(wkdir)
    proc = subprocess.Popen(CMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, cwd=wkdir)

    for line in iter(proc.stdout.readline, b''):
        print line,

    for line in iter(proc.stderr.readline, b''):
        print line,

    proc.communicate()



import stat, shutil
################################################################################
def LnRmTree(topDir):
################################################################################
    shutil.rmtree(topDir)
    return
    for root, dirs, files in os.walk(topDir, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            print "removing File:", filename
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            dirname = os.path.join(root, name)
            os.rmdir(dirname)
            print "removing dir:", dirname
    os.rmdir(topDir)



################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print "\n"*2
        print "immettere il nome del progetto (Directory dello stesso)"
        print "\n"*2
        sys.exit()

    ACTION = ''
    if len(sys.argv) >= 2:
        PRJ_NAME    = sys.argv[1]
        PRJ_PKGNAME = PRJ_NAME                          # Nome della root directory all'interno del tar e nome del tar.
    if len(sys.argv) >= 3: ACTION   = sys.argv[2].upper()

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
            LnRmTree(workingDIR)
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
        copyTree(sourceDIR, destDIR, ignore=ignoreFunc)


    msg = textwrap.dedent("""\
            # =================================================================
            # = Effettua una copia di LnPackage sulla dir di BUILD
            # =================================================================
            """);print '\n' + msg
    LN_PKGNAME      = "LnFunctions"                                                # Nome del modulo che deve essere trasformato in pacchetto
    sourceDIR       = mySEP.join([rootDIR, LN_PKGNAME])
    destDIR         = mySEP.join([workingDIR, PRJ_PKGNAME, "SOURCE",LN_PKGNAME ])
    print "%s --> %s" % (sourceDIR, destDIR)
    if OpSys.upper() == 'WINDOWS':
        ignoreFunc = shutil.ignore_patterns('*.git*', 'tmp*', '*.json', '*.fmted', 'rpdb2.py', '*.sh' )
    else:
        ignoreFunc = shutil.ignore_patterns('*.git*', 'tmp*', '*.json', '*.fmted', 'rpdb2.py', '*.cmd' )

    if ACTION == '--GO':
        copyTree(sourceDIR, destDIR, ignore=ignoreFunc)



    msg = textwrap.dedent("""\
            # =================================================================
            # = Creating zipPackage
            # =================================================================
            """); print '\n' + msg
    sourceDIR   = mySEP.join([workingDIR, PRJ_PKGNAME, "SOURCE" ])
    zipName     = "%s/%s/bin/%s.zip" % (workingDIR, PRJ_PKGNAME, PRJ_PKGNAME)
    print "creating zipFile:", zipName
    print "  with directory:", sourceDIR
    excludePattern = ['.git' + os.sep]
    includePattern = ['*.py']
    if ACTION == '--GO':
        myZip = LnFuncs.LnZip.LnZipClass()
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
        LnRmTree(appoDir)
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
        now      = timeGetNow()
        newFname = mySEP.join([tarOutDir, "%s_%s.tgz" % (fileName, now)])
        os.rename(tarOutFile, newFname)

    EXcludeFromTAR = ['*.cfgc', '*/Exploded*', '*/.git*', 'LICENSE', 'README.md', '*.psproj', '*/data/*']
    excludePattern = ''
    for pattern in EXcludeFromTAR:
        excludePattern += ' --exclude=%s' % (pattern)

    TAR_CMD = "tar %s -cvzf %s *" % (excludePattern, tarOutFile)
    print "Executing...:", TAR_CMD

    if ACTION == '--GO':
        runCommand(TAR_CMD, wkdir=tarInputDir)

    msg = textwrap.dedent("""\
            # =================================================================
            # - Removing Working Directory
            # =================================================================
            """); print '\n' + msg

    if os.path.isdir(workingDIR):
        if ACTION == '--GO':
            print "removing directory tree [%s]" % (workingDIR)
            LnRmTree(workingDIR)
        else:
            print "directory tree [%s] would be removed." % (workingDIR)


    if ACTION == '--GO':
        print "\n"*3
        print "TGZ file is ready: %s" % (tarOutFile)
        print "\n"*3

