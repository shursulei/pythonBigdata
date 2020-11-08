from tools.db import select_by_mcp_with_dict
from prescription.work import OUTPUT_DIR


def gen_change_doctor(month_start, month_end):
    sql_file_path = OUTPUT_DIR + 'prescription_doctor_add_106699133/' + month_start + 'doctor_change.sql'
    with open(sql_file_path, 'w', encoding='UTF-8') as font:
        prescription_list = get_change_prescription(month_start, month_end)
        doctor_dick = get_add_doctor()
        i = 1
        num=0
        for key in doctor_dick:
            num = num+doctor_dick[key]
            while i <= num:
                id = prescription_list[i - 1]
                update_prescription_sql = update_prescription(key, id)
                font.write(update_prescription_sql + '\r\n')
                i += 1


# 需要添加订单量的医生
def get_add_doctor():
    get_add_doctor_sql = '''SELECT * FROM `doctor_add_tmp` where doctor_id not in (106699041,106699133,117799702);'''
    # get_add_doctor_sql = '''SELECT * FROM `doctor_add_tmp` where doctor_id = 106699041;'''
    # get_add_doctor_sql = '''SELECT * FROM `doctor_add_tmp` where doctor_id = 106699133;'''
    result = select_by_mcp_with_dict(get_add_doctor_sql)
    doctor_dick = {}
    for value in result:
        doctor_id = value['doctor_id']
        num = value['num']
        doctor_dick[doctor_id] = num
    return doctor_dick


# 去除所有可以替换的处方
def get_change_prescription(month_start, month_end):
    get_change_prescription_sql = '''SELECT p.id FROM prescription p,user_dataset.base_user_info u
    WHERE p.doctor_id not in(select CONCAT(d.doctor_id,'') from doctor_add_tmp d)
    and p.patient_id = u.id and u.referer is null AND p.gmt_create >= \'{}\' AND p.gmt_create < \'{}\' order by RAND() LIMIT 6500;;'''.format(
        month_start, month_end)
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
    gen_change_doctor('2019-11-01', '2019-12-01')
    gen_change_doctor('2019-12-01', '2020-01-01')
    gen_change_doctor('2020-01-01', '2020-02-01')
    gen_change_doctor('2020-02-01', '2020-03-01')
    gen_change_doctor('2020-03-01', '2020-04-01')
    gen_change_doctor('2020-04-01', '2020-05-01')
    gen_change_doctor('2020-05-01', '2020-06-01')
    gen_change_doctor('2020-06-01', '2020-07-01')
