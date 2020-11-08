#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/17 11:03
# @Author  : shursulei
# @Site    : 
# @File    : Mysql_kafka_json.py
# @Software: PyCharm
import datetime
import json
from queue import Queue

import numpy as np
import pandas as pd
import pykafka
from pykafka.connection import BrokerConnection
from sqlalchemy import create_engine
from pykafka import KafkaClient, topic, common, broker, cluster

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


kafkahosts='127.0.0.1'
kafkaport=9092

#json的data类型转换
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)
#读取mysql数据
def read_sql_table_rearrangeid_todatabase(databasename,originaltablename):
    client = KafkaClient(hosts=kafkahosts + ":" + str(kafkaport))
    with connect_mysql(databasename).connect() as conn, conn.begin():
        try:
            sql = '''
                SELECT
            	id,
            	patient_id,
            	`name`,
            	gmt_create 
            FROM
            	{databasename}.{tablename};
            '''.format(databasename=databasename, tablename=originaltablename)
            df = pd.read_sql(sql, conn)
            # 获取列名
            column_list = list(df.columns)
            df1 = np.array(df)
            lst = []
            str2=[]
            for row in df1:
                # 循环每一行数据，组装成一个字典，然后得到字典的列表
                lst.append(dict(zip(column_list, list(row))))
                # 导入json,将列表转为json字符串
                # son.dumps序列化时候对中文默认使用的ascii编码，想要输出真正的中文需要指定ensure_ascii=False
                str1 = json.dumps(lst, ensure_ascii=False,cls=DateEncoder)
                str2.append(str1)
                # print(str1)
                # print(type(str1))
            print(type(str2))
            #写入kafka
            topic = client.topics[originaltablename]
            with topic.get_sync_producer() as producer:
                for i in str2:
                    print(i)
                    print(type(i))
                    producer.produce(originaltablename,i.encode("gbk"))
        except Exception as ex:
            print(ex)

def Conversiondata(orginstring):
    return bytes(orginstring,encoding='utf8')
def metdataoperate():
    print(broker.MetadataRequest("prescription").topics)
    # print(topic.OffsetType.EARLIEST)
    # print(topic.Partition)
    print(broker.Broker.id.getter)
    print(broker.Broker.list_groups)
    client = KafkaClient(hosts=kafkahosts + ":" + str(kafkaport))
    for i in client.topics.values():
        print(i.name+"1".encode("utf8"))
    # topic = client.topics['prescription']
    # print('Topic: {}'.format(topic.name))
    # print('Partitions: {}'.format(len(topic.partitions)))
    # print('Replicas: {}'.format(len(list(topic.partitions.values())[0].replicas)))
    # print(topic.Topic.name)
    # print(BrokerConnection.connect())
    # print(cluster.Broker.create_topics("prescription2"))
if __name__ == '__main__':
    metdataoperate()
    # read_sql_table_rearrangeid_todatabase("ih", "prescription")
    # topic.Topic('127.0.0.1:9092','prescription')
    # client = KafkaClient(hosts=kafkahosts+":"+str(kafkaport))
    # #获取所有topic
    # print(client.topics.get("my.test"))
    # topic=client.topics['prescription']
    # print(client.topics.keys())
    # print(client.cluster.topics)
    # print(client.brokers.values())
    # print(client.update_cluster())
    #procducer 同步
    # a='''[{"id": 5200319, "patient_id": 13160441, "name": "徐春玲", "gmt_create": "2019-01-01 00:00:03"}]'''
    # with topic.get_sync_producer() as producer:
    #     for i in range(4):
    #         producer.produce(bytes(a, encoding='utf8'))

    # with topic.get_producer(delivery_reports=True) as producer:
    #     count = 0
    #     while True:
    #         count += 1
    #         producer.produce(stringconvbyte('test msg'), partition_key=stringconvbyte('{}'.format(count)))
    #         if count % 10 ** 5 == 0:  # adjust this or bring lots of RAM ;)
    #             while True:
    #                 try:
    #                     msg, exc = producer.get_delivery_report(block=False)
    #                     if exc is not None:
    #                          print('Failed to deliver msg {}: {}').format(msg.partition_key, repr(exc))
    #                     else:
    #                         print('Successfully delivered msg {}').format(msg.partition_key)
    #                 except Queue.Empty:
    #                     break
    # consumer = topic.get_simple_consumer()
    # consumer = topic.get_simple_consumer(consumer_group='my.test', auto_commit_enable=True, auto_commit_interval_ms=1,
    #                                      consumer_id='my.test')
    # for message in consumer:
    #     if message is not None:
    #         print(message.offset, message.value)

