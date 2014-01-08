#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-

import time


# *********************************************************************
# *********************************************************************
def timeGetNow(GMT=False):
    if GMT:
        Tuple   = time.gmtime()
    else:
        Tuple   = time.localtime()

    secs    = time.mktime(Tuple)
    return  secs

