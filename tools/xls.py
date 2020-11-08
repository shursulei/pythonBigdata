#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/7 22:58
# @Author  : shursulei
# @Site    : 
# @File    : xls.py
# @Software: PyCharm Community Edition
# @describe: excel操作
'''
import csv

import xlrd


def xls_reader(f_in, has_title=True, sheet_idx=0):
    workbook = xlrd.open_workbook(f_in)
    sheet = workbook.sheet_by_index(sheet_idx)
    first_line = int(has_title)
    for row_num in range(first_line, sheet.nrows):
        row = sheet.row_values(row_num)
        yield row


def xls_reader_title(f_in, sheet_idx=0):
    """返回title的map结构"""
    title_map = {}
    workbook = xlrd.open_workbook(f_in)
    sheet = workbook.sheet_by_index(sheet_idx)
    row = sheet.row_values(0)
    for index in range(0, len(row)):
        title_map[row[index]] = index
    return title_map


def cell_to_datetime(cell):
    return xlrd.xldate_as_datetime(cell, 0)


def read_excel_to_obj(key_column_dict=None, f_in=None, sheet_idx=0):
    """
     读取 excel 为 dict 的obj对象
    :param key_column_dict:  dict规定 key为 obj对象的key的名字，value 为 excel首行 column的名字
    :param f_in: excel文件路径
    :param sheet_idx:
    :return:
    """
    obj_ist = []
    title_map = {}
    workbook = xlrd.open_workbook(f_in)
    sheet = workbook.sheet_by_index(sheet_idx)
    row = sheet.row_values(0)
    for index in range(0, len(row)):
        title_map[row[index]] = index
    for row_num in range(1, sheet.nrows):
        row = sheet.row_values(row_num)
        obj = {}
        for key in key_column_dict:
            obj[key] = row[title_map[key_column_dict[key]]]
        obj_ist.append(obj)
    return obj_ist


def read_csv_to_obj(key_column_dict=None, f_in=None, row_start=1):
    obj_ist = []
    with open(f_in, newline='', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, quotechar='"')
        read_row_index = 0
        for row in csv_reader:
            # 没到开始行 跳过
            if read_row_index < row_start:
                read_row_index = read_row_index + 1
                continue
            obj = {}
            for key in key_column_dict:
                obj[key] = row[key_column_dict[key]]
            obj_ist.append(obj)
    return obj_ist
