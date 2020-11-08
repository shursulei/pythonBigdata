#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/23 15:51
# @Author  : shursulei
# @Site    : 
# @File    : bireport.py
# @Software: PyCharm

import pandas as pd
from sqlalchemy import create_engine
from xlsxwriter import worksheet, chart

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

def panda_chart(df1,df2, workbookname,sheet_name):
    """
    data of narray
    index of data_frame:  [0,1,2,3]
    cols numbers of static columns
    """
    writer = pd.ExcelWriter(workbookname, engine='xlsxwriter')
    # for i, df in enumerate(df_list):
    df1.to_excel(writer, sheet_name=sheet_name, index=False)
    df2.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()


if __name__ == '__main__':
    # data = [(2, 4), ( 5, 7)]
    sql1='''select TIMESTAMPDIFF(MINUTE,p.prescription_reaudit_time,o.gmt_create) diff, count(1) from ih.prescription p,mall.orders o where p.t_order_id = o.order_id 
and p.gmt_create>="2019-01-01" and p.gmt_create<"2020-07-01"
group by diff order by diff;'''
    sql2='''	-- 医院分钟步长
SELECT
	TIMESTAMPDIFF( MINUTE, p.prescription_reaudit_time, o.gmt_create ) diff,
	count( 1 ) 
FROM
	ih.prescription p,
	mall.orders o ,
	user_dataset.base_user_info bui
WHERE
	p.t_order_id = o.order_id and p.patient_id = bui.id  
	and 	bui.utype = 2 
	AND bui.referer IS NOT NULL
	and p.gmt_create>="2019-01-01" and p.gmt_create<"2020-07-01"
GROUP BY
	diff 
ORDER BY
	diff;'''
    with connect_mysql('ih').connect() as conn,conn.begin():
        df1=pd.read_sql(sql1,conn)
        df2=pd.read_sql(sql1,conn)
        # panda_chart(df1, '处方曲线图.xlsx','分钟步长')
        panda_chart(df1,df2, '处方曲线图.xlsx', '医院分钟步长')