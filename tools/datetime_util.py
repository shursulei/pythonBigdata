#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/7 22:37
# @Author  : shursulei
# @Site    : 
# @File    : datetime_util.py
# @Software: PyCharm Community Edition

'''
"""
datetime转化需要的东西
"""
import datetime
import calendar
import random

all_format_str = "%Y-%m-%d %H:%M:%S"

generate_date = datetime.datetime.strptime("2020-08-31 12:00:00", all_format_str)


def get_ym(dt):
    """
    年月 int
    :param dt:  datetime
    :return:
    """
    return dt.year * 100 + dt.month


def get_pre_month(ym):
    y = int(ym / 100)
    m = int(ym % 100)
    m -= 1
    if m < 1:
        m = 12
        y -= 1
    return y * 100 + m


def get_next_month(ym):
    y = int(ym / 100)
    m = int(ym % 100)
    m += 1
    if m > 12:
        m = 1
        y += 1
    return y * 100 + m


def get_month_range(start_date=None):
    if start_date is None:
        start_date = datetime.date.today()
    start_date = start_date.replace(day=1)
    day1, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + datetime.timedelta(days=days_in_month)
    return start_date, end_date


def random_start_end_time(start, end, fmt="%Y-%m-%d %H:%M:%S"):
    """
    随机获取start-end之间的时间
    """
    start_time = datetime.datetime.strptime(start, fmt)
    end_time = datetime.datetime.strptime(end, fmt)
    return (random.random() * (end_time - start_time) + start_time).strftime(fmt)


def random_start_end_date(start, end):
    """
    随机获取start-end之间的时间
    """
    return start + datetime.timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )


# 获取某月开始结束，字符串表示
def get_month_start_end_time(yearmonth_datetime):
    month_days = calendar.monthrange(yearmonth_datetime.year, yearmonth_datetime.month)[1]
    start_day = datetime.date(yearmonth_datetime.year, yearmonth_datetime.month, 1)
    end_day = datetime.date(yearmonth_datetime.year, yearmonth_datetime.month, day=month_days)
    month_start_day_time = datetime.datetime.combine(start_day, datetime.datetime.min.time())
    month_last_day_time = datetime.datetime.combine(end_day, datetime.datetime.max.time())

    start_date_str = month_start_day_time.strftime(all_format_str)
    end_date_str = month_last_day_time.strftime(all_format_str)

    return start_date_str, end_date_str
