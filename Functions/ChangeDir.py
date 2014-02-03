#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# =================================================================================
import os
import sys

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

