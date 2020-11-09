import os;
import pandas;
import pymysql
import matplotlib;
import matplotlib.pyplot as plt;

# 导入数据到MySQL
# 遍历目录，把里面的所有数据入库
rootDir = "E:/Python/workspace/code/7/7.1/";
for fileName in os.listdir(rootDir):
    path = os.path.join(rootDir, fileName)
    if ".txt" in fileName:
        print(path)
        # 转义
        # path = path.replace("\\", "\\\\");
        # 拿到文件名中的时间字段
        datetime = fileName[0:8];
        tableName = datetime;
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            passwd='root',
            db='pymysql',
            charset='utf8'
        );
        cur = connection.cursor()  # 获取一个游标
        # 建表、导入数据到表中
        # cur.execute("drop table if exists " + tableName)
        cur.executemany(
            "create table " + tableName + "(订单编号 int, 订购日期 datetime, 用户ID int, 产品 char(8), `单价(元)` int, 数量 int, 订购金额 int);");
        # cur.execute(
        #     "LOAD DATA LOCAL INFILE '" + path + "' INTO TABLE `" + tableName + "` CHARACTER SET 'UTF8' COLUMNS TERMINATED BY ',' LINES TERMINATED BY '\\n' IGNORE 1 ROWS;");
        cur.execute(
            "load data local infile '" + path + "' into table '" + tableName + "' character set 'UTF8' columns terminated by ',' LINES TERMINATED BY '\\n' IGNORE 1 ROWS;")
        # 建立日订购统计表
        cur.execute("create table if not exists 日订购统计表(统计日期 date, 订购用户数 int, 订购次数 int, 人均订购金额 double, 订购总额 double);");
        cur.execute("delete from 日订购统计表 where 统计日期='" + datetime + "';");
        cur.execute(
            "insert into 日订购统计表 select '" + datetime + "', count(distinct 用户ID), count(用户ID), sum(订购金额)/count(distinct 用户ID), sum(订购金额) from `" + tableName + "`;");
statDay = pandas.read_sql('select * from 日订购统计表;', con=connection);
# 记得用完要关闭连接
connection.close();

print('\n日订购统计表数据如下:');
print(statDay);

# LOAD DATA LOCAL INFILE "E:/Python/workspace/code/7/7.1/20110901.txt" INTO TABLE `订购明细20110901`;
# CHARACTER SET 'UTF8' COLUMNS TERMINATED BY ',' LINES TERMINATED BY '\\n' IGNORE 1 ROWS;
# ##drop table if exists 订购明细20110901
