from math import ceil
from random import randint
import logging
import typing
import datetime
import os
from pathlib import Path
# from prescription import OUTPUT_DIR, INPUT_DIR
from tools.iterator_util import DEFAULT_PAGE_SIZE, iterate_elements_page
from tools.db import quote_or_MYSQL_NULL
from tools.db import select_by_mcp_with_dict
from tqdm import tqdm

PRES_DETAIL_INSERT_SQL = '''insert into prescription_id_reorder(`old_id`, gmt_create, new_id) values '''

PRES_DETAIL_TEMPLATE_SQL = '''
({old_id},{gmt_create},{new_id})
'''


# def write_pres_detail_sql(pres_detail_list: typing.List, arg_dict):
#     if not pres_detail_list:
#         logging.warning('empty list return')
#         return
#
#     pres_detail_insert_sql = PRES_DETAIL_INSERT_SQL.replace('\n', '')
#
#     pres_detail_template_sql = PRES_DETAIL_TEMPLATE_SQL.replace('\n', '').replace(' ', '')
#
#     sql_out = open(OUTPUT_DIR + "prescription_id_reorder/prescription_id_{arg_dict['ym_date'].year}.sql", 'ab',
#                    buffering=33554432)
#     sql_out.write(pres_detail_insert_sql.encode('utf-8'))
#
#     first = True
#
#     for pres_detail in pres_detail_list:
#         if first:
#             first = False
#         else:
#             sql_out.write(b',')
#         sql_out.write(pres_detail_template_sql.format(**pres_detail).encode('utf-8'))
#
#     sql_out.write(b';\n')
#     sql_out.flush()
#     sql_out.close()


def write_pres_detail_sql(pres_detail_list: typing.List, arg_dict):
    work_dir = Path("{os.getcwd()}")
    data_dir = work_dir.joinpath('output').joinpath("prescription_id_reorder")
    data_dir.mkdir(parents=True, exist_ok=True)

    if not pres_detail_list:
        logging.warning('empty list return')
        return

    pres_detail_insert_sql = PRES_DETAIL_INSERT_SQL.replace('\n', '')

    pres_detail_template_sql = PRES_DETAIL_TEMPLATE_SQL.replace('\n', '').replace(' ', '')
    # filename=OUTPUT_DIR + set_delimiter('prescription\\detail','detail')+"_prescription_detail_{arg_dict['ym_date'].year}.sql";
    filename = Path(data_dir, "prescription_id_{arg_dict['ym_date'].year}_{arg_dict['ym_date'].month}.sql")

    # filename = OUTPUT_DIR + "prescription_detail.sql"
    # if not os.path.exists(filename):
    #     print(filename + ' is not exists, creating...')
    #     fid = open(filename, 'w')
    #     fid.close()
    sql_out = open(filename, 'ab', buffering=33554432)

    sql_out.write(pres_detail_insert_sql.encode('utf-8'))

    first = True

    for pres_detail in pres_detail_list:
        if first:
            first = False
        else:
            sql_out.write(b',')
        sql_out.write(pres_detail_template_sql.format(**pres_detail).encode('utf-8'))

    sql_out.write(b';\n')
    sql_out.flush()
    sql_out.close()


def id_sequence(from_id):
    i = from_id
    while True:
        i += 1
        yield i


def reorder(online_max_id, gap, data):
    """

    :param online_max_id: 线上表的最大ID
    :param gap: 两个ID段的间隔
    :param data: 待排序的数据
            [(10020, datetime(2019,9,18,23,45,56)), (10031, datetime(2019,9,18,23,46,56))]
    :return: 新ID
            [(10020, datetime(2019,9,18,23,45,56), 100001), (10031, datetime(2019,9,18,23,46,56), 100002)]
    """
    # 计算需要分多少个段
    seg = [id_sequence(i * (online_max_id + gap)) for i in range(1, ceil(len(data) / online_max_id) + 1)]
    return [(*d, next(seg[randint(0, len(seg) - 1)])) for idx, d in enumerate(sorted(data, key=lambda x: x[1]))]

def init_reorder_seg(online_max_id, gap, ids):
    """
    根据已分段重排的ID，重新初始化seg，用于继续生成随机ID。
    :param online_max_id: 在重排时使用的online_max_id
    :param gap: 在重排时使用的gap
    :param ids: 当前的所有ID
    :return:
    """
    global seg
    sorted_id = sorted([i for i in ids if i >= (online_max_id + gap)])

    current = sorted_id[0]
    for i in sorted_id:
        if current != i:
            seg.append(id_sequence(current - 1))
            current = i + 1
        else:
            current += 1

def get_id_time_tuple(id_time_dict_list, num):
    id_time_tuple_list = []
    for i in tqdm(range(num)):
        # print(i)
        t_id = id_time_dict_list[i]['id']
        t_time = id_time_dict_list[i]['gmt_create']
        id_time_tuple_list.append((t_id, t_time))
    return id_time_tuple_list


if __name__ == '__main__':
    sql = """
    select id, gmt_create from ih.prescription
    """  # where DATE_FORMAT(gmt_create,'%Y') >= '2019' and DATE_FORMAT(gmt_create,'%Y') < '2020'
    id_time_dict_list = select_by_mcp_with_dict(sql)
    # print(get_id_time_tuple(id_time_dict_list, len(id_time_dict_list)))
    data = get_id_time_tuple(id_time_dict_list, len(id_time_dict_list))

    # 重新生成id
    """
    处方表：
    Max_id = 1916357
    Gap = 989623
    
    处方详情表：
    Max_id = 1919927
    Gap = 993635
    """
    old_time_new_list = reorder(1916357, 989623, data)
    # pres_detail_list = []
    # print(old_time_new_list)
    out_dict_list = []
    for old_time_new in old_time_new_list:
        old_time_new_dict = {}
        old_time_new_dict['old_id'] = old_time_new[0]
        old_time_new_dict['gmt_create'] = quote_or_MYSQL_NULL(old_time_new[1])
        old_time_new_dict['new_id'] = old_time_new[2]
        out_dict_list.append(old_time_new_dict)
    # print(out_dict_list)

    iterate_elements_page(out_dict_list, write_pres_detail_sql, DEFAULT_PAGE_SIZE,
                          ym_date=datetime.datetime.now().date())
