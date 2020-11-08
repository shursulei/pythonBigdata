#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/7 16:39
# @Author  : shursulei
# @Site    : 
# @File    : Engine.py
# @Software: PyCharm Community Edition

'''

'''
º∆À„“˝«Ê
'''
class Engine:
    def __init__(self, f_input, f_output):
        self.g = None
        self.f_input = f_input
        self.f_output = f_output
        self._load_func = None
        self._row_func = None
        self._convert_func = None

    def start(self):
        data = []
        for row in self.load():
            one_row_data = self.process_one_row(row)
            data.extend(one_row_data)

        for d in data:
            self.convert(d)

    def load(self):
        def decorator(f):
            self._load_func = f
            return f

        return decorator

    def row_processor(self):
        def decorator(f):
            self._row_func = f
            return f

        return decorator

    def convert(self):
        def decorator(f):
            self._convert_func = f
            return f

        return decorator
