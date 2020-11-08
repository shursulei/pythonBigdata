import calendar
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import logging
from datetime import datetime
import datetime

from tools.db import select_by_mcp_with_dict

HOST = 'rm-bp19or199ue896jkm.mysql.rds.aliyuncs.com'
DB = 'user_dataset'
PASSWORD = 'M0N0F5wzWhKhqCtl'
USER = 'sulei'
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


def read_sql_table_rearrangeid_todatabase(sql,writetablename,writedatabase):
    with connect_mysql(writedatabase).connect() as conn,conn.begin():
        print("begin start add")
        print(datetime.datetime.now())
        df=pd.read_sql(sql,conn)
        # print(df['gmt_create'].min())
        p = df['id'][df['gmt_create'] == df['gmt_create'].min()].values[0]
        # print(p)
        df['new_id'] = df.index + p
        # print(df.all)
        df.to_sql(writetablename+"_adjuct_id_new_map",connect_mysql(writedatabase),if_exists="replace",chunksize=100000)
        print("write to sql end")
        print(datetime.datetime.now())

def SplicingReadSql(databasename,originaltablename):
    ReadSql = '''
        SELECT
    	id,
    	gmt_create,
    	t_order_id
    FROM
    	{databasename}.{tablename}
    ORDER BY gmt_create asc;
    '''.format(databasename=databasename, tablename=originaltablename)
    return ReadSql
def get_month_range(start_date):
    '''
    获取某个月份的第一日和最后一日的日期
    :param start_date: 传入一个datetime类型日期，返回的为传入时间所在月份的首日和最后一日的日期
    :return:
    '''
    if start_date is None:
        start_date = date.today().replace(day=1)
    else:
        # print(start_date.today())
        start_date = start_date.replace(day=1)
    _, days_in_month = calendar.monthrange(start_date.year, start_date.month)
    end_date = start_date + timedelta(days=days_in_month-1)
    return (start_date, end_date)

#获取当前表中最小的月份和最大的月份
def getMinAndMaxByDatetimeBytable(databasename,originaltablename):
    minsql='''select min(gmt_create) as gmt_create from {databasename}.{tablename};'''.format(databasename=databasename, tablename=originaltablename)
    maxsql='''select max(gmt_create) as gmt_create from {databasename}.{tablename};'''.format(databasename=databasename, tablename=originaltablename)
    mintime=select_by_mcp_with_dict(minsql)
    maxtime=select_by_mcp_with_dict(maxsql)
    # print(type(mintime[0]['gmt_create']),maxtime[0]['gmt_create'])
    mintimestart,mintimeend=get_month_range(mintime[0]['gmt_create'])
    maxtimestart,maxtimeend=get_month_range(maxtime[0]['gmt_create'])
    # print(mintimestart.strftime('%Y-%m-%d'),maxtimeend.strftime('%Y-%m-%d'))
    return mintimestart.strftime('%Y-%m-%d'),maxtimeend.strftime('%Y-%m-%d')

def generate_data(databasename,originaltablename):
    # databasename='ih'
    # originaltablename='prescription_20201011_v2'
    ReadSql = SplicingReadSql(databasename, originaltablename)
    read_sql_table_rearrangeid_todatabase(ReadSql, originaltablename, databasename)
if __name__ == '__main__':
    generate_data('ih','prescription')
