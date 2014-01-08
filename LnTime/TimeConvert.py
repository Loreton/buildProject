#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-

import time


# *********************************************************************
# *********************************************************************
def timeConvert(out='SEC', GMT=False, outputFormat="%Y/%m/%d %H:%M:%S", secs=-1, Tuple=None, str=None, inputFormat="%Y/%m/%d %H:%M:%S"):

        # ----------------------------------------------------------------------------------------
        # - secs=0 significa '1970/01/01 01:00:00'
        # - quindi se voglio ritornare anche le ore mi conviene aggiungere 23 ore al minimo
        # - in modo da partire con le ore a '0'
        # - secs = 23*3600 ==> '1970/01/02 00:00:00'
        # ----------------------------------------------------------------------------------------

    if Tuple:
        pass
    elif secs>=0:
        secs = int(secs)
        minSecs=23*3600
        if secs < minSecs:
            secs += minSecs
        Tuple = time.localtime(secs)
    elif str:
        Tuple = time.strptime(str, inputFormat)
    else:
        Tuple   = time.localtime()

    if GMT:
        Seconds = time.mktime(Tuple)    # converti in secondi
        Tuple   = time.gmtime(Seconds)  # Tuple GMT

    if out == 'SEC':
        return int(time.mktime(Tuple))
    elif out == 'STR':
        return time.strftime(outputFormat, Tuple)
    else:
        return time.strftime(outputFormat, Tuple)

