#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

# ##############################################################################################
# - rmTree()
# - Per cancellare anche i file read-only
# -                                        by: Loreto Notarantonio (2014-01-05)
# ##############################################################################################
import os

import stat
def LnRmTree(topDir):
    for root, dirs, files in os.walk(topDir, topdown=False):
        for name in files:
            filename = os.path.join(root, name)
            os.chmod(filename, stat.S_IWUSR)
            os.remove(filename)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(topDir)