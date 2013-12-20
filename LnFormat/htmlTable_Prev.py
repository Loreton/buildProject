#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types

#############################################################################################
# - htmlTable
# - tableCols viene passato sollo alla prima richiesta
#############################################################################################

def htmlTable(table=None, colLIST=[], align=[], tableCols=None):


    # impostiamo una variabile STATICA
    if not hasattr(htmlTable, "tableCols"):
        htmlTable.tableCols = tableCols              # it doesn't exist yet, so initialize it

        # INIT della tabella
    if tableCols or table == None:
        htmlTable.tableCols = tableCols
                # --------------------------------------------
                # - JVM Info (formato tabella due colonne)
                # --------------------------------------------
        table = [
            '<html>',
            '<body>',
            '<table align="left" border="0" cellpadding="1" cellspacing="1" style="width: 400px; height: 10px" summary="Summary">',
                '<tbody> ',

        ]
            # scrivi chiusura tabella
        table.append(
                '</tbody>'
            '</table>'
            '</body>'
            '</html>'
            )
        return table


    nCols   = len(colLIST)
    ColSPAN = (htmlTable.tableCols - nCols) +1 # Se il numero di colonne della seguente riga è inferiore al  num di tabelle, facciamo SPAN delle ultime colonne

    if isinstance(colLIST, list):
        insertLine=len(table)-1
        tableRow = '<tr>'                                            # open Table line

        for index, colValue in enumerate(colLIST):
            if ColSPAN > 1 and (index+1) == nCols:
                tableRow += '<td colspan="%d">%s</td>' % (ColSPAN, colValue)   # non lo prende
            else:
                tableRow += '<td>%s</td>' % (colValue)

        tableRow += '</tr>'                                 # close Table line
        table.insert(insertLine, tableRow)



    return table

# per verificare parametri strani
def htmlTable0(table=None, colLIST=[], align=[], tableCols=4):
            # --------------------------------------------
            # - JVM Info (formato tabella due colonne)
            # --------------------------------------------
    if table == None:
        table = [
            '<html>',
            '<body>',
            '<table align="left" border="0" cellpadding="0" cellspacing="0" style="width: 100px; height: 5px" summary="Summary">',
                '<tbody> ',

        ]
            # scrivi chiusura tabella
        table.append(
                '</tbody>'
            '</table>'
            '</body>'
            '</html>'
            )
        return table



    nCols  = len(colLIST)
    ColSPAN = (tableCols - nCols) +1

    print
    print
    print "...................", tableCols, nCols, ColSPAN
    print "...................", colLIST
    print
    print


    # if tableColLen > thisColLen:
        # ColSPAN = True
        # nCols =

    if isinstance(colLIST, list):
        insertLine=len(table)-1
        tableRow = '<tr>'                                            # open Table line
        # for colValue in colLIST:
        for index, colValue in enumerate(colLIST):
            # print index, ColSPAN
            if ColSPAN > 1 and (index+1) == nCols:
                tableRow += '<td colspan="%d">%s</td>' % (ColSPAN, colValue)   # non lo prende
                # tableRow += '<td style="text-align: right;">%s</td>' % (colValue)   # non lo prende
            else:
                tableRow += '<td>%s</td>' % (colValue)
        tableRow += '</tr>'                                 # close Table line
        table.insert(insertLine, tableRow)
        print
        print
        print
        print tableRow
        print
        print
        print


    return table

