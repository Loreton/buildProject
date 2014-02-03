#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# =================================================================================
import os

import stat, shutil
################################################################################
def rmTree(topDir):
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