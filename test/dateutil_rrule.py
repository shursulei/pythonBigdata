#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/9 11:58
# @Author  : shursulei
# @Site    : 
# @File    : dateutil_rrule.py
# @Software: PyCharm
# @describe:
'''

from datetime import datetime
from dateutil.rrule import rrule, DAILY, MO, WE
def main():
    # 生成rrule 对象
    rrule_obj = rrule(DAILY, # 每天
    byweekday=(MO, WE), # 周一、周三
    dtstart=datetime(2012, 1, 1), # 2012 年1 月1 日起
    until=datetime(2012, 2, 1)) # 2012 年2 月1 日止
    # 逐个取出符合条件的日期对象并显示在屏幕上
    for dt in rrule_obj:
        print(dt)
if __name__ == '__main__':
    main()