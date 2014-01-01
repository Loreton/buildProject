#!/usr/bin/python -O
# -*- coding: iso-8859-15 -*-
# Enumerate


class enumerateClass(object):
    def __init__(self, names):
        for number, name in enumerate(names.split()):
            setattr(self, name, number)


'''
import types
def Enumerate(data):
    valueType    = type(data)
    retValue = None
    if valueType in [types.StringType, types.UnicodeType]:
        retValue =  enumerate(data.split())
    elif valueType in [types.ListType, types.TupleType]:
        retValue =  enumerate(data)

    return retValue

'''


