#!/usr/bin/python -O
# -*- coding: utf-8 -*-
# ......... -*- coding: latin-1 -*-

import xlrd

def getRow(gv, sheet, row, wb, wantTupleDate, startCol=0):
    Prj         = gv.Prj
    LN          = gv.LN
    logger      = gv.LN.logger
    calledBy    = gv.LN.sys.calledBy
    logger.info('entered - [called by:%s]' % (calledBy(1)))


    returnRow = []
    types,values = sheet.row_types(row),sheet.row_values(row)
    try:
        for i in range(len(types)):
            type,value = types[i],values[i]

            if type == 2:
                if value == int(value):
                    value = int(value)

            elif type == 3:
                datetuple = xlrd.xldate_as_tuple(value, wb.datemode)
                if wantTupleDate:
                    value = datetuple
                else:
                        # time only no date component
                    if datetuple[0] == 0 and datetuple[1] == 0 and \
                       datetuple[2] == 0:
                        value = "%02d:%02d:%02d" % datetuple[3:]

                        # date only, no time
                    elif datetuple[3] == 0 and datetuple[4] == 0 and \
                         datetuple[5] == 0:
                        value = "%04d/%02d/%02d" % datetuple[:3]

                        # full date
                    else:
                        value = "%04d/%02d/%02d %02d:%02d:%02d" % datetuple

            elif type == 5:
                value = xlrd.error_text_from_code[value]

            # else:
                # value.encode('latin-1')
                # print '-----', value

            returnRow.append(value)

        logger.debug('exiting - [called by:%s]' % (calledBy(1)))
        return returnRow[startCol:]

    except StandardError, why:
        Msg1 = "Error running program [%s]\n\n ....%s\n"  % (sys.argv[0], why)
        Title = "%s [line:%d]" % (functionName(), sourceLine())
        logger.info(Title, Msg1, Exit=True, deep=1)


def excelFormat():
    fnt         = xlwt.Font()
    style       = xlwt.XFStyle()
    fnt.height  = 16*20
    fnt.bold    = False
    fnt.italic  = False
    fnt.name    = "Arial"
    fnt.name    = "Courier New"

    style.font  = fnt
    # fnt = Font()
    # fnt.name = 'Arial'
    # fnt.colour_index = 4
    # fnt.bold = True

    # borders = Borders()
    # borders.left = 6
    # borders.right = 6
    # borders.top = 6
    # borders.bottom = 6

    # style = XFStyle()
    # style.font = fnt
    # style.borders = borders
    # colWidth = 14
    # colBaseWidth = 184                                  # Width=0 ==> 184 pixels  Width=1 ==> 439 pixels
    # colOneUnitWidth = int(1*36.5*7)                     # Espansione di una unita' =~ 255.5 pixels
    # colsWidth = colBaseWidth + colOneUnitWidth*colWidth    # in pixels

    logger.debug('exiting - [called by:%s]' % (calledBy(1)))


if __name__ == "__main__":
    excelFileName = 'MP3_Master_NewType.xls'
    excelFileName = 'dates.xls'
    excelFileName = '\\Loreto\\Office\\Excel\\Samples\\IP_Address.xls'
    excelFileName = '\\Loreto\\ProjectsAppl\\Python\\MP3Catalog\\MP3_Master_NewTypeProva.xls'
    wb = xlrd.open_workbook(excelFileName)
    for sheet in wb.sheets():
        print 'SheetName:',sheet.name
        START_ROW=0
        LAST_ROW=10
        for row in range(sheet.nrows):
            if row<START_ROW:
                continue

            if row>LAST_ROW:
                print "."*60
                print "MAX_ROWs has been reached......."
                print "."*60
                break

            rowValue = ExcelGetRow(sheet, row, wb, wantTupleDate=False)
            nFields  = sheet.ncols
            for j, val in zip(range(nFields), rowValue):
                print "[colNum:%4d] - %s" % (j, val)

