#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/9 12:04
# @Author  : shursulei
# @Site    : 
# @File    : flask_demo.py
# @Software: PyCharm
# @describe:
'''
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello World!'
if __name__=='__main_':
    app.debug=True
    app.run(host='0.0.0.0',port=9000)