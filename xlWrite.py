import xlwt
from datetime import datetime
from xlrd import open_workbook
from xlutils.copy import copy
from pathlib import Path


def output(filename, xlsheet, rollNO, name, present):
    my_file = Path('Attendance/'+filename+str(datetime.now().date())+'.xls')

    # if the file is already present
    if my_file.is_file():
        rb = open_workbook('Attendance/'+filename+str(datetime.now().date())+'.xls')
        book = copy(rb)
        sh = book.get_sheet(0)
    else:
        # create a new workbook with a new sheet
        book = xlwt.Workbook()
        sh = book.add_sheet(xlsheet)

    style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on', num_format_str='#,##0.00')
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')
    sh.write(0, 0, datetime.now().date(), style1)

    col1_name = 'RollNo'
    col2_name = 'NAME'
    col3_name = 'PRESENT'

    sh.write(1, 0, col1_name, style0)
    sh.write(1, 1, col2_name, style0)
    sh.write(1, 2, col3_name, style0)

    sh.write(rollNO+1, 0, rollNO)
    sh.write(rollNO+1, 1, name)
    sh.write(rollNO+1, 2, present)

    fullname = filename+str(datetime.now().date())+'.xls'
    book.save('Attendance/'+fullname)
    return fullname
