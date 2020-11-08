import csv
import logging
import os
import sys
import time
import typing
from datetime import datetime

from dateutil.relativedelta import relativedelta


from tools.datetime_util import get_ym
from tools.db import select_by_mcp_with_dict, MYSQL_NULL, add_quote, quote_or_MYSQL_NULL
from tools.iterator_util import DEFAULT_PAGE_SIZE, iterate_elements_page
from tools.rand import random_pick
from tools.xls import xls_reader, cell_to_datetime
from prescription.work import INPUT_DIR, OUTPUT_DIR

PRES_DETAIL_INSERT_SQL = '''
insert into prescription_detail_v2(prescription_id, sku_id, `name`, drug_name, num, unit, `usage`, per_amount, 
times, remark, usage_frequency_code, usage_frequency_name, per_num, per_unit, dose, spec, chemical_name, gmt_create, gmt_modify)
values 
'''
PRES_DETAIL_TEMPLATE_SQL = '''
({prescription_id},{sku_id},{name},{drug_name},{num},{unit},{usage},{per_amount},{
times},{remark},{usage_frequency_code},{usage_frequency_name},{per_num},{per_unit},{dose},{spec},{chemical_name},
{gmt_create},{gmt_modify})
'''


def read_drug_detail():
    drug_dict = {}
    with open(INPUT_DIR + 'online_pres_detail.csv', 'r', encoding='utf-8') as file:
    # with open(INPUT_DIR + 'prescription/drug.csv', 'r',encoding='utf-8') as file:
        cr = csv.reader(file)
        next(cr)
        for row in cr:
            drug_dict[row[21]] = {
                'name': row[7],
                'drug_name': row[8],
                'num': row[9],
                'unit': row[10],
                'usage': row[11],
                'per_amount': row[12],
                'times': row[13],
                'remark': row[14],
                'usage_frequency_code': row[15],
                'usage_frequency_name': row[16],
                'per_num': row[17],
                'per_unit': row[18],
                'dose': row[19],
                'spec': row[20],
            }
    return drug_dict


def write_pres_detail_sql(pres_detail_list: typing.List, arg_dict):
    if not pres_detail_list:
        logging.warning('empty list return')
        return

    pres_detail_insert_sql = PRES_DETAIL_INSERT_SQL.replace('\n', '')

    pres_detail_template_sql = PRES_DETAIL_TEMPLATE_SQL.replace('\n', '').replace(' ', '')
    # filename=OUTPUT_DIR + set_delimiter('prescription\\detail','detail')+f"_prescription_detail_{arg_dict['ym_date'].year}.sql";
    filename = OUTPUT_DIR + "prescription_detail_all_v2.sql";
    if not os.path.exists(filename):
        print(filename + ' is not exists, creating...')
        fid = open(filename, 'w')
        fid.close()
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


def gen_prescription_detail(this_year):
    """
    处方详情数据
    :return:
    """
    for row in xls_reader(INPUT_DIR + 'prescription/处方数据all.xlsx', True, 0):
        pres_detail_list = []
        # 时间轴
        yearmonth_datetime = cell_to_datetime(row[0])
        ym = get_ym(yearmonth_datetime)
        ym_date = yearmonth_datetime.date()
        ym_date = ym_date.replace(day=1)
        next_ym_date = yearmonth_datetime.date() + relativedelta(months=1)
        next_ym_date = next_ym_date.replace(day=1)
        logging.info("generate data: {}".format(ym))
        origin_pres_detail_list = select_by_mcp_with_dict(
            """SELECT
	p.id AS id,
	p.gmt_create AS gmt_create,
	i.item_id AS item_id,
	od.item_name AS item_name,
	i.drug_name AS drug_name,
	i.drug_unit AS unit,
	i.drug_usage AS `usage`,
	i.chemical_name AS chemical_name,
	i.drug_spec AS spec,
    od.item_num as item_num
FROM
	ih.prescription p,mall.orders o ,mall.orders_detail od ,mall.item i
WHERE  p.t_order_id = o.parent_id and o.order_id = od.order_id and od.item_id = i.item_id and
	p.gmt_create >= '{ym_date:%Y-%m-%d}'
	AND p.gmt_create < '{next_ym_date:%Y-%m-%d}' -- flag&1=1 处方药
	AND i.is_drug = 1
UNION
SELECT
	p.id AS id,
	p.gmt_create AS gmt_create,
	i.item_id AS item_id,
	od.item_name AS item_name,
	i.drug_name AS drug_name,
	i.drug_unit AS unit,
	i.drug_usage AS `usage`,
	i.chemical_name AS chemical_name,
	i.drug_spec AS spec,
    od.item_num as item_num
FROM
	ih.prescription p ,mall.orders_detail od ,mall.item i
WHERE  p.t_order_id = od.order_id and od.item_id = i.item_id
	and p.gmt_create >= '{ym_date:%Y-%m-%d}'
	AND p.gmt_create < '{next_ym_date:%Y-%m-%d}' -- flag&1=1 处方药
	AND i.is_drug = 1
                        """)

        ym_pres_detail_count = len(origin_pres_detail_list)

        precent_10 = (ym_pres_detail_count * 0.1)
        logging.info('month total pres detail {ym_pres_detail_count}')
        ym_pres_process_count = 0

        for pres_detail in origin_pres_detail_list:
            detail_dict = {}

            detail_dict['prescription_id'] = pres_detail['id']
            detail_dict['sku_id'] = pres_detail['item_id']
            detail_dict['chemical_name'] = quote_or_MYSQL_NULL(pres_detail['chemical_name'])
            detail_dict['name'] = quote_or_MYSQL_NULL(pres_detail['item_name'])
            detail_dict['drug_name'] = quote_or_MYSQL_NULL(pres_detail['drug_name'])
            if pres_detail['item_num']:
                detail_dict['num'] = pres_detail['item_num']
            else:
                detail_dict['num'] = random_pick([1, 2, 3, 4, 5], [0.9, 0.05, 0.03, 0.01, 0.01])
            detail_dict['unit'] = quote_or_MYSQL_NULL(pres_detail['unit'])
            detail_dict['usage'] = quote_or_MYSQL_NULL(pres_detail['usage'])
            detail_dict['per_amount'] = MYSQL_NULL
            detail_dict['times'] = MYSQL_NULL
            detail_dict['remark'] = MYSQL_NULL
            detail_dict['usage_frequency_code'] = MYSQL_NULL
            detail_dict['usage_frequency_name'] = quote_or_MYSQL_NULL(
                    random_pick(['1次/天', '3次/天', '2次/天'], [0.5, 0.4, 0.1]))
            detail_dict['per_num'] = MYSQL_NULL
            detail_dict['per_unit'] = MYSQL_NULL
            detail_dict['dose'] = MYSQL_NULL
            detail_dict['spec'] = quote_or_MYSQL_NULL(pres_detail['spec'])
            gmt_create_f = "{pres_detail['gmt_create']:%Y-%m-%d %H:%M:%S}"
            detail_dict['gmt_create'] = quote_or_MYSQL_NULL(gmt_create_f)
            detail_dict['gmt_modify'] = quote_or_MYSQL_NULL(gmt_create_f)

            pres_detail_list.append(detail_dict)
            ym_pres_process_count += 1

            if ym_pres_process_count % precent_10 == 0:
                logging.info(
                    '{ym} process month pres detail {ym_pres_process_count} precent {ym_pres_process_count / ym_pres_detail_count :.1%}')

        pres_detail_list.sort(key=lambda x: x['gmt_create'])

        logging.info('{ym} has {len(pres_detail_list)} pres detail')

        iterate_elements_page(pres_detail_list, write_pres_detail_sql, DEFAULT_PAGE_SIZE,
                              ym_date=yearmonth_datetime.date())


if __name__ == '__main__':
    gen_prescription_detail(2020)
