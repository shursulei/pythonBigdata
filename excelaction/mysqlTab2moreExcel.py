#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/9 17:40
# @Author  : shursulei
# @Site    :
# @File    : moreExcelMergeOne.py
# @Software: PyCharm
# @describe: 将多个excel文件合并成一个
'''

import xlwt
import MySQLdb
import warnings
import datetime

warnings.filterwarnings("ignore")

mysqlDb_config = {
    'host': 'xxxx',
    'user': 'xxxx',
    'passwd': 'xxxx',
    'port': 3306,
    'db': 'xxxx'
}

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)


def getDB(dbConfigName):
    dbConfig = eval(dbConfigName)
    try:
        conn = MySQLdb.connect(host=dbConfig['host'], user=dbConfig['user'], passwd=dbConfig['passwd'],
                               port=dbConfig['port'], charset='utf8')
        conn.autocommit(True)
        curr = conn.cursor()
        curr.execute("SET NAMES utf8");
        curr.execute("USE %s" % dbConfig['db']);

        return conn, curr
    except MySQLdb.Error as e:
        print
        "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return None, None


def mysqlTabStructure2excel(dbConfigName, tabName, schemaName, exportPath):
    # 边框的定义
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    borders.bottom_colour = 0x3A
    # Initialize a style for frist row
    style_fristRow = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True
    font.colour_index = 1
    style_fristRow.font = font

    badBG = xlwt.Pattern()
    badBG.pattern = badBG.SOLID_PATTERN
    badBG.pattern_fore_colour = 6
    style_fristRow.pattern = badBG

    style_fristRow.borders = borders

    # Initialize a style for data row
    style_dataRow = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = u'隶变-简 常规体'
    font.bold = False
    style_dataRow.font = font

    style_dataRow.borders = borders

    selectSql = "SELECT  TABLE_SCHEMA userName, \
    	table_name tabName, \
    	ORDINAL_POSITION colNo, \
    	COLUMN_NAME colName, \
    	COLUMN_TYPE dataType, \
    	IS_NULLABLE isNull, \
    	COLUMN_COMMENT colComment \
    FROM information_schema. COLUMNS \
    WHERE TABLE_SCHEMA = '{schemaName}' \
    AND table_name = '{tabName}';".format(schemaName=schemaName, tabName=tabName)

    conn, curr = getDB(dbConfigName)
    curr.execute(selectSql)
    datas = curr.fetchall()
    fields = curr.description
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('{tabName}'.format(tabName=tabName[0:31]), cell_overwrite_ok=True)

    # 写上字段信息
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field][0], style_fristRow)

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1, len(datas) + 1):
        for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % datas[row - 1][col], style_dataRow)

    workbook.save(r'{exportPath}/{exportName}.xls'.format(exportPath=exportPath, exportName=schemaName + '-' + tabName))

    curr.close()
    conn.close()


def getSchemaTab(dbConfigName, schemaName, exportPath):
    selectSql = "select TABLE_NAME tabName from information_schema.TABLES where TABLE_SCHEMA='{schemaName}';".format(
        schemaName=schemaName)
    conn, curr = getDB(dbConfigName)
    curr.execute(selectSql)
    datas = curr.fetchall()
    for tabName in datas:
        mysqlTabStructure2excel(dbConfigName, tabName[0], schemaName, exportPath)


# Batch Test
if __name__ == '__main__':
    dbConfigName = 'mysqlDb_config'
    schemaName = 'henan'
    exportPath = 'E:/pycharm/yirongworkspace/excel'
    getSchemaTab(dbConfigName, schemaName, exportPath)
