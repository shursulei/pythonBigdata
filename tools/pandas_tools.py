from sqlalchemy import create_engine
import pymysql
import pandas as pd
from tools.dbconfigure import USER, PASSWORD, HOST, DB
db_info = {'user': USER,
           'password': PASSWORD,
           'host': HOST,
           'port': 3306,
           'database': DB
           }
engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=UTF8MB4' % db_info, encoding='utf-8')
def connect_mysql():
    engine = create_engine('mysql+pymysql://%(user)s:%(password)s@%(host)s:%(port)d/%(database)s?charset=UTF8MB4' % db_info, encoding='utf-8')
    return engine

def get_data_by_sql(sql,engine):
    return pd.read_sql(sql,engine)


# print(df)
def read_sql_table_test():
    with connect_mysql().connect() as conn,conn.begin():
        df=pd.read_sql_table('myusertable',conn,chunksize=9000)
        print(df.c)

def excel_operator():
    df=pd.read_excel(r'C:\Users\ks\Desktop\全职医生.xlsx', sheet_name='Sheet1')
    df['new_doctor_id']
    print(df)
if __name__ == '__main__':
    # read_sql_table_test()
    # excel_operator()
    sql='''
    SELECT
    	p.id,p.patient_id,
    	bui.gmt_create AS '医生注册时间',
    	p.gmt_create AS '处方创建时间',
    	b.gmt_create AS '订单生成时间'
    FROM
    	ih.prescription_min_patient_20200823 p
    	JOIN user_dataset.base_user_info bui ON p.patient_id = bui.id
    	JOIN mall.orders b ON p.t_order_id = b.order_id and b.user_id=p.patient_id;
    '''
    df=pd.read_sql(sql,engine)
    print(df.count())