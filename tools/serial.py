#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/7 23:37
# @Author  : shursulei
# @Site    : 
# @File    : serial.py
# @Software: PyCharm Community Edition
# @describe: 数据序列化到磁盘
'''
import logging
import os
import pickle
from functools import wraps
import inspect

# SERIAL_FILE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/serial'
from work import IS_CLOSE_SERIAL

SERIAL_FILE_DIR = os.getcwd() + '/serial/'
DUMP_FILE_EXT = '.dump'

if not os.path.exists(SERIAL_FILE_DIR):
    os.makedirs(SERIAL_FILE_DIR)


def serial_result(func):
    """
    将函数返回值序列化到磁盘。相同参数直接读取。
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        func_filename = inspect.getmodule(func).__file__[
                        inspect.getmodule(func).__file__.rfind('/') if '/' in inspect.getmodule(func).__file__ else inspect.getmodule(func).__file__.rfind('\\') + 1:inspect.getmodule(func).__file__.rfind('.py')]
        func_args = func.__name__ + ('.' + str(args) if args else '') + ('.' + str(kwargs) if kwargs else '')
        dump_fname = func_filename + '.' + func_args + DUMP_FILE_EXT
        serial_file = SERIAL_FILE_DIR + dump_fname
        if os.path.exists(serial_file):
            logging.debug('[serial_result] is loading results of function %s ' % (func_args,))
            print('[serial_result] is loading results of function %s ' % (func_args,))
            with open(serial_file, 'rb') as fin:
                return pickle.load(fin)
        else:
            logging.debug('[serial_result] is calling function %s ' % (func_args,))
            print('[serial_result] is calling function %s ' % (func_args,))
            result = func(*args, **kwargs)
            logging.debug('[serial_result] is dumping results of function %s ' % (func_args,))
            print('[serial_result] is dumping results of function %s ' % (func_args,))
            with open(serial_file, 'wb') as fout:
                pickle.dump(result, fout)
            return result

    return wrapper
