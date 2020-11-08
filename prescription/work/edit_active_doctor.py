#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/20 18:32
# @Author  : shursulei
# @Site    : 
# @File    : edit_active_doctor.py
# @Software: PyCharm
import random

from sqlalchemy import create_engine
import typing

from tools.datetime_util import all_format_str
from tools.db import select_by_mcp_with_dict, add_quote
from pathlib import Path
import pandas as pd

from tools.iterator_util import iterate_elements_page, DEFAULT_PAGE_SIZE
from prescription.work import OUTPUT_DIR

date_format_str = "%Y-%m-%d"

HOST = 'rm-bp1rk7fzef4jxu728.mysql.rds.aliyuncs.com'
DB = 'ih'
PASSWORD = 'ZTQzOTQ0NG'
USER = 'it_sj'
db_info = {'user': USER,
           'password': PASSWORD,
           'host': HOST,
           'port': 3306,
           'database': DB
           }
def connect_mysql(databasename):
    db_info['database']=databasename
    engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=UTF8MB4' % db_info, encoding='utf-8')
    return engine

PRES_INSERT_SQL = '''insert into update_doctor_active_prescription(`month`, uid, gmt_create, `date`, mark) values '''
PRES_TEMPLATE_SQL = '''
({month}, {uid}, {gmt_create}, {date}, {mark})'''


def get_prescription_order():
    sql = '''
       SELECT `month`,uid ,total
       FROM ih.doctor_month_uid
       '''
    month_uid = select_by_mcp_with_dict(sql)
    return month_uid
def get_prescription_order2(month,uid,total):
    sql = '''
       SELECT * 
       FROM ih.doctor_active_prescription
       where `month`={month} and uid={uid} order by rand() limit {total} 
       '''
    month_uid = select_by_mcp_with_dict(sql)
    return month_uid
def get_prescription_order3():
    sql = '''
       SELECT `month`,`uid`,`date`
       FROM ih.doctor_active_prescription
       '''
    month_uid = select_by_mcp_with_dict(sql)
    return month_uid

def write_pres_sql(pres_list: typing.List):
    pres_insert_sql = PRES_INSERT_SQL.replace('\n', '')

    pres_template_sql = PRES_TEMPLATE_SQL.replace('\n', '').replace(' ', '')

    out_dir = Path("{OUTPUT_DIR}/update_doctor_active_prescription")
    out_dir.mkdir(parents=True, exist_ok=True)

    sql_out = open(
        "{out_dir}/update_doctor_active_prescription.sql",
        'ab', buffering=33554432)
    # sql_out = open(
    #     f"{out_dir}/prescription_{arg_dict['ym_date'].year}_{arg_dict['ym_date'].month}.sql",
    #     'ab', buffering=0)
    sql_out.write(pres_insert_sql.encode('utf-8'))

    first = True

    for pres in pres_list:
        if first:
            first = False
        else:
            sql_out.write(b',')
        # logging.info(pres['t_order_id'])
        sql_out.write(pres_template_sql.format(**pres).encode('utf-8'))

    sql_out.write(b';\n')
    sql_out.flush()
    sql_out.close()

def add_dict(a):
    b = []
    for j in a:
        c={}
        c['month']=add_quote(j['month'])
        c['uid'] = add_quote(j['uid'])
        c['gmt_create'] = add_quote(j['gmt_create'].strftime(all_format_str))
        c['date'] = add_quote(j['date'].strftime(date_format_str))
        c['mark']=0
        b.append(c)
    return b
if __name__ == '__main__':
    month_uid=get_prescription_order()
    # updateid = get_prescription_order3()
    # a=[]
    # for i in month_uid:
    #     b = []
    #     for j in updateid:
    #         if i['month']==j['month'] and i['uid']==j['uid']:
    #             b.append(j)
    #         a.append(random.sample(b,int(len(b) * (random.uniform(40, 60) / 100))))
    a=[]
    for i in month_uid:
        updateid=get_prescription_order2(i['month'],i['uid'],i['total'])
        # a.append(add_dict(updateid))
        iterate_elements_page(add_dict(updateid), write_pres_sql, DEFAULT_PAGE_SIZE)
    # b=[]
    # for j in a:
    #     c={}
    #     c['month']=add_quote(j['month'])
    #     c['uid'] = add_quote(j['uid'])
    #     c['gmt_create'] = add_quote(j['gmt_create'].strftime(all_format_str))
    #     c['date'] = add_quote(j['date'].strftime(date_format_str))
    #     c['mark']=0
    #     b.append(c)

    # df = pd.DataFrame(a)
    # writedatabase="ih"
    # writetablename="update_doctor_active_prescription"
    # with connect_mysql(writedatabase).connect() as conn, conn.begin():
    #     df.to_sql(writetablename, connect_mysql(writedatabase), if_exists="replace",
    #               chunksize=100000)

