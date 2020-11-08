#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/7 22:55
# @Author  : shursulei
# @Site    : 
# @File    : iterator_util.py
# @Software: PyCharm Community Edition
# @describe: 分页
'''
from math import ceil


def iterate_elements_page(list_data, action, page_size, **kwargs):
    """
    分页迭代list
    :param list_data:
    :param action: 分页动作
    :param page_size: 分页大小
    :return:
    """

    page_start = 0
    total = len(list_data)

    if total == 0:
        return

    if page_size >= total:
        if len(kwargs) != 0:
            action(list_data, kwargs)
        else:
            action(list_data)
        return

    stop = ceil(total / page_size)
    for i in range(stop):
        # kwargs 非空
        page_list = list_data[page_start * page_size: (page_start + 1) * page_size]

        if len(kwargs) != 0:
            action(page_list, kwargs)
        else:
            action(page_list)
        page_start += 1


DEFAULT_PAGE_SIZE = 10000
