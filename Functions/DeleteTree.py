#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# =================================================================================
import os
import stat, shutil
import platform;    OpSys = platform.system()


def delTree(topDir, verbose=False):

    if OpSys.upper() == 'WINDOWS':
        shutil.rmtree(topDir)
        return

    else:
        for root, dirs, files in os.walk(topDir, topdown=False):
            for name in files:
                filename = os.path.join(root, name)
                if verbose: 
                    print "removing File:", filename
                os.chmod(filename, stat.S_IWUSR)
                os.remove(filename)
            for name in dirs:
                dirname = os.path.join(root, name)
                os.rmdir(dirname)
                if verbose:
                    print "removing dir:", dirname
        os.rmdir(topDir)
