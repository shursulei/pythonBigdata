#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/9 18:56
# @Author  : shursulei
# @Site    : 
# @File    : ExeclUtils.py
# @Software: PyCharm
# @describe:EXCEL的工具类
'''


import xlwt

class ExeclUtils():
    @staticmethod
    def create_execl(sheet_name,row_titles):
        '''
        :param sheet_name:表格名
        :param row_titles:行标题
        :return:
        '''
        f = xlwt.Workbook()
        sheet_info = f.add_sheet(sheet_name,cell_overwrite_ok=True)
        for i in range(0,len(row_titles)):
            sheet_info.write(0,i,row_titles[i])
        return f, sheet_info

    @staticmethod
    def write_execl(execl_file,execl_sheet,count,data,execl_name):
        '''
        :param execl_file:文件对象
        :param execl_sheet:表格名
        :param count:数据插入到哪一行
        :param data:传入的数据 []类型
        :param execl_name:execl文件名
        :return:
        '''
        for j in range(len(data)):
            execl_sheet.write(count,j,data[j])
        execl_file.save(execl_name)