#!/usr/bin/env python

#coding: utf-8

import xlsxwriter



workbook = xlsxwriter.Workbook('wugui.xlsx') #创建一个Excel文件

worksheet = workbook.add_worksheet()  #创建一个工作表对象

chart = workbook.add_chart({'type':'column'}) #创建一个图表对象

#定义数据表开头列表

title = [u'业务名称',u'星期一',u'星期二',u'星期三',u'星期四',u'星期五',u'星期六',u'星期日',u'平均流量']

buname = [u'乌龟运维官网',u'乌龟1',u'乌龟2',u'乌龟3',u'乌龟4'] #定义频道名称

#定义5频道一周七天数据列表

data = [

    [134,432,348,349,565,435,158],

    [176,168,94,53,68,700,91],

    [251,265,154,165,540,154,135],

    [77,76,75,74,73,73],

    [81,82,83,84,91,83,82],

]

format=workbook.add_format() #定义format格式对象

format.set_border(1) #定义format对象单元格边框加粗(1像素)的格式



format_title=workbook.add_format() #定义format_title格式对象

format_title.set_border(1) #定义format_title对象单元格边框加粗(1像素)的格式

format_title.set_bg_color('#cccccc') #定义format_title对象单元格背景颜色为‘cccccc’的格式

format_title.set_align('center') #定义format_title对象单元格剧中对齐的格式

format_title.set_bold() #定义format_title对象单元格内容加粗的格式



format_ave=workbook.add_format() #定义format_ave格式对象

format_ave.set_border(1) #定义format_ave对象单元格边框加粗(1像素)的格式

format_ave.set_num_format('0.00') #定义format_ave对象单元格数字类别显示格式



#下面分别以行或列写入方式将标题,业务名称,流量数据写入起初单元格，同时引用不同格式对象

worksheet.write_row('A1',title,format_title)

worksheet.write_column('A2',buname,format)

worksheet.write_row('B2',data[0],format)

worksheet.write_row('B3',data[1],format)

worksheet.write_row('B4',data[2],format)

worksheet.write_row('B5',data[3],format)

worksheet.write_row('B6',data[4],format)



#定义图表数据系列函数

def chart_series(cur_row):

    worksheet.write_formula('I'+cur_row,'=AVERAGE(B'+cur_row+':H'+cur_row+')',format_ave) #计算(AVERAGE函数)

   #频道周平均流量

    chart.add_series({

        'categories':'=Sheet1!$B$1:$H$1', #将“星期一至星期日”作为图标数据标签(X轴)

'values':      '=Sheet1!$B$'+cur_row+':$H$'+cur_row, #频道一周所有数据操作 为数据区域

'line':        {'color':'black'}, #线条颜色定义为black(黑色)

'name':'Sheet1!$A$'+cur_row,

   })

for row in range(2,7): #数据域以第2~6行进行图表数据系列函数调用

    chart_series(str(row))

#chart.set_table() #设置X轴表格格式，本示例不启用

#chart.set_style(30) #设置图表样式，本示例不启用

chart.set_size({'width': 577,'height':287}) #设置图表大小

chart.set_title({'name': u'业务流量周报报表'}) #设置图表(上方)大标题

chart.set_y_axis({'name': 'MB/s'}) #设置Y轴(左侧)小图标

worksheet.insert_chart('A8', chart) #在A8单元格插入图表

workbook.close() #关闭Excel文档