#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
#
# Scope:  Funzioni per operare sul python dictionary
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################


import types


# #########################################################################################
# = Merge di due Dictionary.
# = I valori del secondo sovrascrivono le chiavi del primo
# = Se non si vuole ricoprire il primo dict bisogna preventivamente averne fatto una copia
# =   dictCopia = dict.copy()
# #########################################################################################
def dictMerge(dict1, dict2, level=0, logger=None):


        # la copia non è effettiva. Prestare attenzione
    dictNew = dict1.copy()


    if level == 0:
        if logger: logger.info("Merging dictionaries - started")

    for key, val in sorted(dict2.items()):                  # per tutte le chiavi del dict2
        sectID2  = dict2.get(key)                           # prendiamo il pointer del secondo
        sectType = type(sectID2)                            # otteniamo il TYPE
        sectID1 = getDictPrt(dictNew, key)                  # prendi il pointer nel dictNew

        if (sectType == types.StringType) or \
           (sectType == types.BooleanType) or \
           (sectType == types.FloatType) or \
           (sectType == types.LongType) or \
           (sectType == types.IntType):
            dictNew[key] = dict2.get(key)      # Assegnamo il valore

            # - Se è una LIST copiamo valore per valore
        elif isinstance(sectID2, types.ListType):
            for line in sectID2:                    # - cerchiamo l'item nella lista1.
                try:
                    inx = sectID1.index(line)       # - cerchiamo l'item nella lista1.
                    sectID1[inx] = line             # - FOUND - Replace it
                except ValueError:                  # no match
                    sectID1.append(line)            # - Aggiungiamolo

        elif isinstance(sectID2, types.TupleType):
            pass

            # - Se è un DICT iteriamo
        elif isinstance(sectID2, types.DictType):
            dummy = dictMerge(sectID1, sectID2, level=level+1)    # in questo caso il return value non mi interessa

    if level == 0:
        if logger: logger.info("Merging dictionaries - completed")
    return dictNew



