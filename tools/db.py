#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/7 22:45
# @Author  : shursulei
# @Site    : 
# @File    : db.py
# @Software: PyCharm Community Edition
# @describe:
'''
import mysql.connector
import pymysql
MYSQL_NULL = 'NULL'
HOST = 'xxxx'
DB = 'xxxx'
PASSWORD = 'xxxx'
USER = 'xxxx'

def select(sql):
    db_conn = pymysql.connect(HOST, USER, PASSWORD, DB)
    db_conn.set_charset('utf8')
    cur = db_conn.cursor()
    cur.execute(sql)
    return cur.fetchall()


def selectByMcp(sql):
    """
    ͨ��mysql-connector-python ��ѯ
    ��ԭʼC������չ��ѯ ���ܻ�úܶ�
    :param sql:
    :return: �����
    """

    cnx = mysql.connector.connect(user=USER, password=PASSWORD,
                                  host=HOST,
                                  database=DB
                                  )

    cursor = cnx.cursor()
    cursor.execute(sql)

    return cursor.fetchall()


def select_by_mcp_with_dict(sql, *, host=HOST, user=USER, password=PASSWORD, database=DB):
    """
    ͨ��mysql-connector-python ��ѯ

    ��ԭʼC������չ��ѯ ���ܻ�úܶ�

    ����һ��list �а���row dict

    :param database:
    :param password:
    :param user:
    :param host:
    :param sql:
    :return: �����
    """

    cnx = mysql.connector.connect(user=user, password=password,
                                  host=host,
                                  database=database
                                  )

    cursor = cnx.cursor(dictionary=True)
    print("start get data ...")
    cursor.execute(sql)
    return cursor.fetchall()


add_quote = lambda x: "'{x}'"
add_quote_v2 = lambda x: "''{x}''"

def quote_or_MYSQL_NULL(s):
    return "'{s}'" if s is not None else MYSQL_NULL

def quote_or_MYSQL_NULL_v2(s):
    return s if s is not None else MYSQL_NULL
