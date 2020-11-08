import calendar
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import logging
from datetime import datetime

from tools.db import select_by_mcp_with_dict

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


def read_sql_table_rearrangeid_todatabase(sql,writetablename,begindate,writedatabase):
    with connect_mysql(writedatabase).connect() as conn,conn.begin():
        print("beggin read sql {begindate}".format(begindate=begindate))
        df=pd.read_sql(sql,conn)
        # print(df['gmt_create'].min())
        p = df['id'][df['gmt_create'] == df['gmt_create'].min()].values[0]
        # print(p)
        df['new_id'] = df.index + p
        # print(df.all)
        df.to_sql(writetablename+"tmp"+begindate[0:7],connect_mysql(writedatabase),if_exists="replace",chunksize=100000)
        print("write to sql {begindate}".format(begindate=begindate))

def SplicingReadSql(databasename,originaltablename,begindate,enddate):
    ReadSql = '''
        SELECT
    	id,
    	gmt_create 
    FROM
    	{databasename}.{tablename} 
    WHERE
    	gmt_create >= '{begindate}' 
    	AND gmt_create <= '{enddate}'
    ORDER BY gmt_create asc;
    '''.format(databasename=databasename, tablename=originaltablename, begindate=begindate,enddate=enddate)
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
if __name__ == '__main__':
    databasename='medical'
    originaltablename='member_equity_service_record'
    beginDate,endDate=getMinAndMaxByDatetimeBytable(databasename,originaltablename)
    # print(beginDate,endDate)
    # beginDate = '2020-01-01'
    # endDate = '2020-08-30'
    date_index = pd.date_range(beginDate, endDate)
    days = [pd.Timestamp(x).strftime("%Y-%m-%d") for x in date_index.values]
    tmp = []
    for index, v in enumerate(days):
        if index == len(days) - 1:
            tmp.append(days[index])
        if index == 0:
            tmp.append(days[0])
        else:
            _ = v.split('-')[2]
            if _ == '01':
                tmp.append(days[index - 1])
                tmp.append(days[index])
    # print(tmp)
    for i in range(len(tmp) // 2):
        # print(tmp[i * 2], tmp[i * 2 + 1])
        ReadSql=SplicingReadSql(databasename,originaltablename,tmp[i * 2],tmp[i * 2 + 1])
        read_sql_table_rearrangeid_todatabase(ReadSql,originaltablename,tmp[i * 2],databasename)
