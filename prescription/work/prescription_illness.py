import pandas as pd
from sqlalchemy import create_engine
import datetime,time
import random
from tqdm import tqdm

illness_list = ['拉肚子','腹泻','感冒','呼吸系统疾病','糖尿病','高血压']
weight_list = [20,20,30,15,5,10]
ill = random.choices(illness_list,weight_list)[0]
engine = create_engine("mysql+pymysql://xuwei:o0r$&OYLzo38df^X@rm-bp19or199ue896jkm.mysql.rds.aliyuncs.com:3306/ih")
connect = engine.connect()

for i in tqdm(range(44214)):
    ill = random.choices(illness_list,weight_list)[0]
    export_sql = 'UPDATE prescription SET illness= ' + "'" + '{ill}' + "'" + ' WHERE illness is null and gmt_create >= "2020-07-01" limit 1;'
#     print(export_sql)
    engine.execute(export_sql)
    
connect.close()