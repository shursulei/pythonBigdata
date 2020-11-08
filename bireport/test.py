#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/23 13:45
# @Author  : shursulei
# @Site    : 
# @File    : test.py
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

def panda_chart(df_list, max_cow,cols, title_x, title_y):
    """
    data of narray
    index of data_frame:  [0,1,2,3]
    cols numbers of static columns
    """

    writer = pd.ExcelWriter('pandas_chart_columns2.xlsx', engine='xlsxwriter')
    for i, df in enumerate(df_list):
        # df = pd.DataFrame(data, index=None, columns=["姓名", "饱和度", "人力"])
        sheet_name = 'Sheet{i}'
        sheet_name = 'Sheet1'
        df.to_excel(writer, sheet_name=sheet_name, index=False)
        workbook = writer.book
        worksheet = writer.sheets[sheet_name]
        chart = workbook.add_chart({'type': 'line'})
        # set colors for the chart each type .
        colors = ['#E41A1C', '#377EB8']  # , '#4DAF4A', '#984EA3', '#FF7F00']
        # Configure the series of the chart from the dataframe data.
        # chart.add_series({
        #     'name': [f'{sheet_name}'],
        #     'categories': [f'{sheet_name}', 1, 0, max_cow, 0],  # axis_x start row ,start col,end row ,end col
        #     'values': [f'{sheet_name}', 1, 1, max_cow, 1],  # axis_y value of
        #     # 'fill': {'color': colors[col_num - 1]},  # each type color choose
        #     # 'overlap': -10,
        # })
        # for col_num in range(1, max_cow + 1):
        #     chart.add_series({
        #         'name': [f'{sheet_name}', 0, col_num],
        #         'categories': [f'{sheet_name}', 1, 0, max_cow, 0],  # axis_x start row ,start col,end row ,end col
        #         'values': [f'{sheet_name}', 1, col_num, 4, col_num],  # axis_y value of
        #         # 'fill': {'color': colors[col_num - 1]},  # each type color choose
        #         # 'overlap': -10,
        #     })
        # chart.add_series({
        #         'name': '=Sheet1!$A$1',
        #         'categories': '=Sheet1!$A$2:$A$7',
        #         'values': '=Sheet1!$B$'+cur_row+':$H$'+cur_row,
        # })
        chart.add_series({
            'categories': [sheet_name, 1, 0, max_cow, 0],  # 将周一到周日作为图标x轴
            'values': '=Sheet1!$B$' + str(max_cow),  # 一周所有数据作为数据区域
            'line': {'color': 'black'},  # 线条颜色定义为黑色
            'name': '=Sheet1!$A$' + str(max_cow),  # 引用名称为图例
        })

        # Configure the chart axes.
        chart.set_x_axis({'name': '{title_x}'})
        chart.set_y_axis({'name': '{title_y}', 'major_gridlines': {'visible': False}})
        chart.set_size({'width': 900, 'height': 400})
        # Insert the chart into the worksheet.
        worksheet.insert_chart('H2', chart)
    writer.save()

def chart_series(cur_row):
    chart.add_series({
    'categories': '=Sheet1!$A$'+cur_row, # 将周一到周日作为图标x轴
    'values': '=Sheet1!$B$'+cur_row, # 一周所有数据作为数据区域
    'line': {'color': 'black'}, # 线条颜色定义为黑色
    'name': '=Sheet1!$A$'+cur_row, # 引用名称为图例
    })

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
        df=pd.read_sql(sql1,conn)
    # df = pd.DataFrame(data, index=None)
        panda_chart([df], len(df),2, "title x", "title y")