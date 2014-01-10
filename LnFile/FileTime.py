#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import os
import time

---------------------DA PROVARE-------------
def getFileTimeGMT(file):
    fTime       = os.path.getmtime(file)           # get modified time
    Tuple       = time.gmtime(fTime)
    epochTime   = time.mktime(Tuple)
    return epochTime                            # return file time



def getFileTimeLT(file):
    fTime       = os.path.getmtime(file)           # get modified time
    return fTime                            # return file time


def getFileTime(file, GMT=False):

    try:
        fileSTAT = os.stat(file)                        # get modified time
        fTime    = fileSTAT.st_mtime                   # get modified time
        if GMT:
            # fTime   = os.path.gmtime(file)           # get modified time
            Tuple   = time.gmtime(fileSTAT.st_mtime)
            fTime   = time.mktime(Tuple)

    except (TypeError, IOError, os.error), why:
        msg = "File %s doesn't exists" % file
        if exitOnError:
            print msg
            sys.exit()
        else:
            return 0

    return int(fTime)                            # return file time