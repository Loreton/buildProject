#!/usr/bin/python
# -*- coding: latin-1 -*-
# -*- coding: iso-8859-1 -*-
#                                               by Loreto Notarantonio 2013, February
# ######################################################################################
import sys
import types

def CSSData():
    '''
    "<style>"
    "    body   {color:red;}"               # colore di default
    "    h1     {color:#00ff00;}"
    "    p.ex   {color:rgb(0,0,255);}"
    "</style>"

    <style>
        body            {font-size:100%;}
        h1              {font-size:2.5em;}
        p.sansserif     {font-family:Arial,Helvetica,sans-serif;}
        p.NRed  {font-family:Arial,Helvetica,sans-serif; color:red}
        p.IRed          {font-family:Arial,Helvetica,sans-serif; color:red; font-style:italic;}
        p.BRed          {font-family:Arial,Helvetica,sans-serif; color:red; font-style:italic;}
        h2              {font-size:1.875em; color:red; }
        p               {font-size:0.875em;}
        p.right         {text-align:right;}
        p.justify       {text-align:justify;}
        p.uppercase     {text-transform:uppercase;}
        p.lowercase     {text-transform:lowercase;}
        p.capitalize    {text-transform:capitalize;}
        p               {text-indent:50px;}
    </style>

    <!-- CSS goes in the document HEAD or added to your external stylesheet -->
    <style type="text/css">
        table.gridtable {
            font-family: verdana,arial,sans-serif;
            font-size:      11px;
            color:          #333333;
            border-width:   1px;
            border-color:   #666666;
            border-collapse: collapse;
        }
        table.gridtable th {
            border-width: 1px;
            padding: 8px;
            border-style: solid;
            border-color: #666666;
            background-color: #dedede;
        }
        table.gridtable td {
            border-width: 1px;
            padding: 8px;
            border-style: solid;
            border-color: #666666;
            background-color: #ffffff;
        }
    </style>


    <!-- Table goes in the document BODY -->
    <table class="gridtable">
    <tr>
        <th>Info Header 1</th><th>Info Header 2</th><th>Info Header 3</th>
    </tr>
    <tr>
        <td>Text 1A</td><td>Text 1B</td><td>Text 1C</td>
    </tr>
    <tr>
        <td>Text 2A</td><td>Text 2B</td><td>Text 2C</td>
    </tr>
    </table>




    '''

def htmlString(value, bold=False, italic=False, color="black", face="verdana", size="3" ):

    FONT    = 'color="%s" size="%s" face="%s' % (color, size, face)

    retValue = '<font %s>%s</font>' % (value)

    if bold:    retValue = '<b>' + retValue + '</b>'
    if italic:  retValue = '<i>' + retValue + '</i>'

    return retValue



def cssTable(className):
    #  http://www.w3schools.com/css/css_table.asp
    # color:          # colore del text
    # padding:        # determina l'altezza della riga
         # <!DOCTYPE HTML>
    data = """
        <style type="text/css">
            table.%s {
                font-family: verdana,arial,sans-serif;
                font-size:          11px;
                color:              DarkRed;    background-color: white;
                border-width:       1px;        border-color: grey;

                # border-collapse: collapse;
            }
            table.%s th {
                padding:            8px;
                border-color:       gray;       border-style: solid;    border-width: 3px;
                color:              DarkRed;    background-color: LightGray;
                text-align:         center;     vertical-align: center;
            }

            table.%s td {
                padding:            2px;
                border-color:       green;      border-style: solid;  border-width: 1px;
                color:              DarkRed;    background-color:   LightCyan ;
                text-align:         center;       vertical-align:     center;
            }
         </style>

    """ % (className, className, className)

    # per usarla scrivere: <table class=className></table>
    data = data.replace('\n', '')




    return data

# ########################################################################################################
#  def htmlTable(table=None, header=False, rowData=[])
#   - Prima CALL
#       htmlTable("tableNAME", header=True, rowData=['Col1', 'Col2', 'col3', 'col4', 'col5'])
#   - Successive CALL
#       htmlTable("tableNAME", rowData=['Col1', 'Col2', 'col3', 'col4', 'col5'])
# ########################################################################################################
def htmlTable(className, table=None, header=False, rowData=[]):

    if table==None:
        table = []

            # if not hasattr(htmlTable, "tableCols"): htmlTable.tableCols = tableCols              # it doesn't exist yet, so initialize it
        htmlTable.tableCols = len(rowData)              # impostiamo una variabile STATICA per mantenere il numero max di colonne

            # Inizio Table
        table.append('<table class=%s align="left" border="1" cellpadding="1" cellspacing="1" style="width: 100px; height: 10px">'% (className))

            # Fine Table
        table.append('</table>')
        htmlTable.insertRow = -1              # punto dove inserire le altre righe (prima della </table>


    if header:
        TAG_TYPE = 'th'
    else:
        TAG_TYPE = 'td'


    ptr = htmlTable.insertRow
        # Inizio Riga
    table.insert(ptr, "<tr>")

    reqCols = len(rowData)
    MaxIndex = htmlTable.tableCols -1
    colSpan = 1
    spanVal = []
    rowval = []

    if reqCols < htmlTable.tableCols: colSpan += htmlTable.tableCols - reqCols
    for index, colValue in reversed(list(enumerate(rowData))):
        if colValue == None or colValue == '':
            colSpan += 1
            continue

        if colSpan > 1:
            TAG_OPEN = '<%s colspan="%d">' % (TAG_TYPE, colSpan)
        else:
            TAG_OPEN = '<%s>' % (TAG_TYPE)


        TAG_END = '</%s>' % (TAG_TYPE)
        rowval.insert(0, '%s%s%s' % (TAG_OPEN, colValue, TAG_END))
        colSpan = 1


    table.insert(ptr, ''.join(rowval))

        # Fine Riga
    table.insert(ptr, "</tr>")


    return table



# ########################################################################################################
#  def htmlTable(table=None, header=False, rowData=[])
#   - Prima CALL
#       htmlTable("tableNAME", header=True, rowData=['Col1', 'Col2', 'col3', 'col4', 'col5'])
#   - Successive CALL
#       htmlTable("tableNAME", rowData=['Col1', 'Col2', 'col3', 'col4', 'col5'])
# ########################################################################################################
def htmlTableCSS(className, table=None, header=False, rowData=[], tableAlign='left'):

    if header or table==None:
        table = []

            # if not hasattr(htmlTable, "tableCols"): htmlTable.tableCols = tableCols              # it doesn't exist yet, so initialize it
        htmlTable.tableCols = len(rowData)              # impostiamo una variabile STATICA per mantenere il numero max di colonne

        table.append(cssTable(className))

            # Inizio Table
        table.append('<table class=%s align="%s">' % (className, tableAlign))

            # Fine Table
        table.append('</table>')


        htmlTable.insertRow = -1              # punto dove inserire le altre righe (prima della </table>
        TAG_TYPE = 'th'

    else:
        TAG_TYPE = 'td'

    ptr = htmlTable.insertRow
        # Inizio Riga
    table.insert(ptr, "<tr>")

    reqCols = len(rowData)
    MaxIndex = htmlTable.tableCols -1
    colSpan = 1
    spanVal = []
    rowval = []

    if reqCols < htmlTable.tableCols: colSpan += htmlTable.tableCols - reqCols
    for index, colValue in reversed(list(enumerate(rowData))):
        if colValue == None or colValue == '':
            colSpan += 1
            continue

        if colSpan > 1:
            TAG_OPEN = '<%s colspan="%d">' % (TAG_TYPE, colSpan)
        else:
            TAG_OPEN = '<%s>' % (TAG_TYPE)


        TAG_END = '</%s>' % (TAG_TYPE)
        rowval.insert(0, '%s%s%s' % (TAG_OPEN, colValue, TAG_END))
        colSpan = 1

    # table.append(''.join(rowval))
    table.insert(ptr, ''.join(rowval))

        # Fine Riga
    table.insert(ptr, "</tr>")


    return table




################################################################################
# - M A I N
################################################################################
if __name__ == "__main__":
    # print cssTable("Loreto")
    table =  htmlTable("ciaoLoreto", rowData=['Col1', 'Col2', 'col3', 'col4', 'col5'])
    table =  htmlTable("ciaoLoreto", table=table, rowData=['Col13', '', '', 'col43'])
    table =  htmlTable("ciaoLoreto", table=table, rowData=['Col11', 'Col21', 'col31', 'col41', 'col51'])
    table =  htmlTable("ciaoLoreto", table=table, rowData=['Col12', 'Col22', 'col32', 'col42', ''])
    table =  htmlTable("ciaoLoreto", table=table, rowData=['Col13', 'Col23', 'col33', 'col43'])
    table =  htmlTable("ciaoLoreto", table=table, rowData=['', 'Col23', 'col33', 'col43']) # Viene male perché non devo mandare il primo campo nullo
    for line in table:
        print line



