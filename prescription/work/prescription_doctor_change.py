import calendar
import datetime
import random
import os
from tools.db import select_by_mcp_with_dict
from prescription.work import OUTPUT_DIR
from prescription.work.gen_prescription_V2_old import get_active_user_data, get_user_list_group_by_month, \
    get_month_day_user_register


# def gen_doctor_dick(ym, prescription_doctor_num):
#     sql_file_path = OUTPUT_DIR + 'prescription/' + ym + 'doctor_change.sql'
#     with open(sql_file_path, 'w', encoding='UTF-8') as font:
#         # 获取当月活跃医生
#         active_doctor_list = get_active_user_data(str(ym), 1)
#         # 获取有处方权的医生
#         active_prescription_doctor_list = [d for d in active_doctor_list if d['tag'] == 'PRESCRIPTION']
#         # 从活跃处方医生中选取一定数量的处方医生组成医生池
#         doctor_pool_list = random.sample(active_prescription_doctor_list, int(prescription_doctor_num))
#
#         yearmonth_datetime = datetime.datetime.strptime(ym, '%Y%m')
#         month_days = calendar.monthrange(yearmonth_datetime.year, yearmonth_datetime.month)[1]
#         start_day = datetime.date(yearmonth_datetime.year, yearmonth_datetime.month, 1)
#         end_day = datetime.date(yearmonth_datetime.year, yearmonth_datetime.month, day=month_days)
#         prescription_dick = get_change_prescription(start_day, end_day)
#         # 将医生按照注册日期分为当前月注册与历史月注册
#         history_month_doctor_list, current_month_doctor_list = get_user_list_group_by_month(doctor_pool_list, start_day)
#         day_user_dict = get_month_day_user_register(current_month_doctor_list)
#
#         first_day = start_day
#         day_doctor_pool_list = history_month_doctor_list
#         while start_day <= end_day:
#             # 每天将当天注册医生放入医生池
#             before_day = start_day - datetime.timedelta(days=1)
#             if before_day >= first_day:
#                 if day_user_dict.get(before_day):
#                     day_doctor_pool_list = day_doctor_pool_list + day_user_dict[before_day]
#             if len(day_doctor_pool_list) > 0:
#                 doctor_list = random.sample(day_doctor_pool_list,
#                                             int(len(day_doctor_pool_list) * (random.uniform(70, 80) / 100)))
#                 random.shuffle(doctor_list)
#                 prescription_dick_key = datetime.datetime.strftime(start_day, '%Y-%m-%d')
#                 if prescription_dick.keys().__contains__(prescription_dick_key):
#                     prescription_list = prescription_dick[prescription_dick_key]
#                     for id in prescription_list:
#                         doctor = random.choice(doctor_list)
#                         update_prescription_sql = update_prescription(doctor['id'], id)
#                         font.write(update_prescription_sql + '\r\n')
#                 start_day = start_day + datetime.timedelta(days=1)

def gen_doctor_dick(ym):
    print(ym)
    sql_file_path = OUTPUT_DIR +  os.sep+ ym + 'doctor_change.sql'
    with open(sql_file_path, 'w', encoding='UTF-8') as font:
        # 获取当月活跃医生
        active_doctor_list = get_active_user_data(str(ym), 1)
        # 获取有处方权的医生
        active_prescription_doctor_list = [d for d in active_doctor_list if d['tag'] == 'PRESCRIPTION']

        yearmonth_datetime = datetime.datetime.strptime(ym, '%Y%m')
        month_days = calendar.monthrange(yearmonth_datetime.year, yearmonth_datetime.month)[1]
        start_day = datetime.date(yearmonth_datetime.year, yearmonth_datetime.month, 1)
        end_day = datetime.date(yearmonth_datetime.year, yearmonth_datetime.month, day=month_days)
        prescription_list = get_change_prescription_v2(start_day, end_day)
        # 将医生按照注册日期分为当前月注册与历史月注册
        history_month_doctor_list, current_month_doctor_list = get_user_list_group_by_month(
            active_prescription_doctor_list, start_day)
        history_month_doctor_id_list=[]
        for doctor in history_month_doctor_list:
            history_month_doctor_id_list.append(doctor['id'])
        # 当月已经使用的医生id
        doctor_id_list = get_doctor_id(start_day, end_day)
        print(set(doctor_id_list))
        print(set(history_month_doctor_id_list))
        # 当月已经使用的医生id和历史月注册医生交集
        day_doctor_pool_list = list(set(doctor_id_list).intersection(set(history_month_doctor_id_list)))
        random.shuffle(day_doctor_pool_list)
        for id in prescription_list:
            doctor = random.choice(day_doctor_pool_list)
            update_prescription_sql = update_prescription(doctor, id)
            font.write(update_prescription_sql + '\r\n')


def get_doctor_id(start_day, end_day):
    get_doctor_id_sql = '''
    SELECT DISTINCT doctor_id FROM ih.prescription WHERE
	gmt_create >= \'{}\'
    AND gmt_create <= \'{}\'
    AND redundancy in (113,1)'''.format(start_day, end_day)
    result = select_by_mcp_with_dict(get_doctor_id_sql)
    doctor_list=[]
    for value in result:
        id = int(value['doctor_id'])
        doctor_list.append(id)
    return doctor_list



def get_change_prescription(start_day, end_day):
    get_change_prescription_sql = '''SELECT
	id,gmt_create
    FROM
	ih.prescription
    WHERE
	gmt_create >= \'{}\'
    AND gmt_create <= \'{}\'
    AND redundancy = 112'''.format(start_day, end_day)
    result = select_by_mcp_with_dict(get_change_prescription_sql)
    prescription_dick = {}
    for value in result:
        id = value['id']
        gmt_create = value['gmt_create']
        gmt_day = datetime.datetime.strftime(gmt_create, '%Y-%m-%d')
        if gmt_day not in prescription_dick:
            prescription_dick[gmt_day] = []

        prescription_dick[gmt_day].append(id)
    return prescription_dick


def get_change_prescription_v2(start_day, end_day):
    get_change_prescription_sql = '''SELECT
	id
    FROM
	ih.prescription
    WHERE
	gmt_create >= \'{}\'
    AND gmt_create <= \'{}\'
    AND redundancy = 112'''.format(start_day, end_day)
    result = select_by_mcp_with_dict(get_change_prescription_sql)
    prescription_list = []
    for value in result:
        id = value['id']
        prescription_list.append(id)
    return prescription_list


def update_prescription(doctor_id, id):
    update_prescription_sql = 'UPDATE prescription SET doctor_id=\'{}\' WHERE id=\'{}\';'.format(doctor_id, id)
    return update_prescription_sql


if __name__ == '__main__':
    # gen_doctor_dick('201902')
    # gen_doctor_dick('201903')
    # gen_doctor_dick('201904')
    # gen_doctor_dick('201905')
    # gen_doctor_dick('201906')
    # gen_doctor_dick('201907')
    # gen_doctor_dick('201908')
    # gen_doctor_dick('201909')
    # gen_doctor_dick('201910')
    # gen_doctor_dick('201911')
    # gen_doctor_dick('201912')
    # gen_doctor_dick('202001')
    # gen_doctor_dick('202002')
    # gen_doctor_dick('202003')
    # gen_doctor_dick('202004')
    # gen_doctor_dick('202005')
    # gen_doctor_dick('202006')
    gen_doctor_dick('202007')
    gen_doctor_dick('202008')
    gen_doctor_dick('202009')
    gen_doctor_dick('202010')
    gen_doctor_dick('202011')


