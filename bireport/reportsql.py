#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/23 11:23
# @Author  : shursulei
# @Site    : 
# @File    : reportsql.py
# @Software: PyCharm

import importlib,sys
import os
import re
import traceback

from optparse import OptionParser

import mysql
import ujson
import xlwt
from prettytable import PrettyTable, unicode

importlib.reload(sys)

class DBConfig(object):

    '''数据库配置'''

    def __init__(self, host, port, username, password, dbname):
        '''
        @param host 数据库主机
        @param port 端口
        @param username 用户名
        @param password 密码
        @param dbname 数据库名称
        '''
        self.host, self.port = host, port
        self.username, self.password = username, password
        self.dbname = dbname

    def __str__(self):
        return "{host:%s, port:%d, username:%s, dbname:%s}" % (
            self.host, self.port, self.username, self.dbname
        )
class Table(object):

    '''表格'''

    def __init__(self, headers, rows):
        '''
        @param headers 表头
        @param rows 数据行
        '''
        self.headers = headers
        self.rows = rows

    def show(self):
        tbl = PrettyTable(self.headers)
        for row in self.rows:
            tbl.add_row(row)
        print(tbl)
SQL_SEPERATOR = ";"

def load_db_config(cfg_file_path):
    with open(cfg_file_path, "r") as f:
        config_json = ujson.loads(f.read())
        return DBConfig(**config_json)


def execute_sqllist(db_config, report_sql):
    conn = gen_connection(db_config)
    report_sql_list = report_sql.split(SQL_SEPERATOR)
    map(check_sql, report_sql_list)  # 检查每个SQL格式是否正确
    cursor = conn.cursor()
    tables = []
    for sql in report_sql_list:
        tables.append(execute_sql(cursor, sql))
    conn.commit()
    cursor.close()
    conn.close()
    return tables
QUERY_SQL_PATTERN = re.compile(r'^select.*?from\s+([^\s]*?)', re.I)
def check_sql(report_sql):
    '''检查SQL格式，必须是select语句'''
    if not QUERY_SQL_PATTERN.search(report_sql):
        print(u"SQL '%s' 格式不合法，必须是select语句" % report_sql)
        exit(0)
def gen_connection(db_config):
    conn = mysql.connector.connect(
        host=db_config.host,
        user=db_config.username,
        passwd=db_config.password,
        db=db_config.dbname,
        charset="utf8"
    )
    return conn
def get_table_headers(db_cursor):
    return [i[0] for i in db_cursor.description]
def execute_sql(db_cursor, sql):
    db_cursor.execute(sql)
    table = Table(
        headers=get_table_headers(db_cursor),
        rows=db_cursor.fetchall()
    )
    table.show()
    return table
def gen_workbook(tables, sheet_names):
    workbook = xlwt.Workbook()
    for idx, table in enumerate(tables):
        sheet_name = sheet_names[idx]
        sheet = workbook.add_sheet(unicode(sheet_name))
        # 写入表头
        for header_idx, header_name in enumerate(table.headers):
            sheet.write(0, header_idx, unicode(header_name))
        for row_idx, row in enumerate(table.rows):
            for col_idx, cell_val in enumerate(row):
                sheet.write(row_idx + 1, col_idx, cell_val)
    return workbook


if __name__ == "__main__":
    parser = OptionParser(usage=__doc__)
    parser.add_option("--db",default="/etc/sqlreport/db.conf",help=u"数据库配置")
    parser.add_option("--sql",default=None,help=u"要生成报表的SQL,多条SQL用分号分割")
    parser.add_option("--xls",default=None,help=u"生成Excel文件的名称")
    parser.add_option("--savedir",default="",help=u"生成Excel文件的保存目录，默认保存在当前目录")
    parser.add_option("--sheets",default=None,help=u"导出的sheet名称列表,用逗号分割")
    options, _ = parser.parse_args()

    # 检查必备的参数是否齐全

    if not options.sql:
        print(u"必须指定至少一条SQL语句!")
        exit(0)

    if not options.db:
        print(u"必须指定数据库配置!")
        exit(0)

    # 加载数据库配置

    try:
        db_config = load_db_config(options.db)
    except:
        print(u"加载数据库连接配置出错!")
        traceback.print_exc()
        exit(0)

    # 遍历SQL语句生成table list
    tables = execute_sqllist(db_config, options.sql)

    # 不需要导出Excel,直接退出
    if not options.xls:
        exit(0)

    # 检查sheet names与tables数量是否匹配
    if not options.sheets:
        print(u"必须要指定Excel Sheet名称!")
        exit(0)
    sheet_names = options.sheets.split(',')
    if len(sheet_names) != len(tables):
        print(u"sheet 名称数量与table数量不匹配!")
        exit(0)

    workbook = gen_workbook(tables, sheet_names)
    workbook.save(os.path.join(options.savedir, options.xls))
