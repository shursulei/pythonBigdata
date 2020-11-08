# -*- coding:utf-8 -*-
from datetime import datetime

from __init__ import INPUT_DIR, set_delimiter, OUTPUT_DIR


def Main():
    source_dir = set_delimiter(INPUT_DIR,'detail_prescription_detail_.sql')
    target_dir = OUTPUT_DIR
    # 计数器
    flag = 0
    # 文件名
    name = 1
    # 存放数据
    dataList = []

    print("开始。。。。。")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    with open(source_dir, 'r',encoding='utf-8') as f_source:
        for line in f_source:
            flag += 1
            dataList.append(line)
            if flag == 200000:
                with open(target_dir + "prescription" + str(name) + ".sql", 'w+',encoding='utf-8') as f_target:
                    for data in dataList:
                        f_target.write(data)
                name += 1
                flag = 0
                dataList = []

    # 处理最后一批行数少于20万行的
    with open(target_dir + "prescription" + str(name) + ".sql", 'w+',encoding='utf-8') as f_target:
        for data in dataList:
            f_target.write(data)

    print("完成。。。。。")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == "__main__":
    Main()

