#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/8 11:18
# @Author  : shursulei
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm Community Edition
# @describe:
'''
import os
import sys
import logging

import sys
sys.path.append('/home/sulei')

INPUT_DIR = os.getcwd() + '/input/'


if not os.path.exists(INPUT_DIR):
    print(INPUT_DIR + ' is not exists, creating...')
    os.makedirs(INPUT_DIR)

OUTPUT_DIR = os.getcwd() +os.sep+ 'output'+os.sep
if not os.path.exists(OUTPUT_DIR):
    print(OUTPUT_DIR + ' is not exists, creating...')
    os.makedirs(OUTPUT_DIR)

LOG_DIR = os.getcwd() + '/log/'


logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO,
                    handlers=[logging.StreamHandler(stream=sys.stdout)])

# 开发环境 加速验证
IS_DEV = True if os.getenv("DEV") == '1' else False
IS_CLOSE_SERIAL = True if os.getenv("CLOSE_SERIAL") == '1' else False
IS_ONLINE_RUN = True if os.getenv("ONLINE_RUN") == '1' else False

def get_dev_value(v, d_value):
    if IS_DEV:
        return d_value
    else:
        v
