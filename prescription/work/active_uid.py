from prescription.work import INPUT_DIR, OUTPUT_DIR
from tools.datetime_util import get_ym
from tools.serial import serial_result


@serial_result
def get_yearmonth_act_uid(utype):
    """
    两个CSV文件来自道斌制作的带留存活跃。

    :param utype: 1 医院用户，0 非医院用户
    :return: {201905: {123,234,345} }
    """
    ym_uid = {}

    with open(INPUT_DIR + 'active_uid/' + ('医院用户月活.csv' if utype else '非医院用户.csv')) as fin:
        for idx, line in enumerate(fin):
            line_content = line.split(',')
            yearmonth, uid = int(line_content[0]), int(line_content[1])

            if yearmonth not in ym_uid:
                ym_uid[yearmonth] = set()

            ym_uid[yearmonth].add(uid)

            if idx % 1000000 == 0:
                print('ym active_uid %s lines processed.' % idx)

    return ym_uid


def get_yearmonth_act_uid_by_year(utype, ym):
    """
    按年获取 月活
    :param utype:
    :param year:
    :return:
    """
    return get_yearmonth_act_uid(utype).get(ym, set())


@serial_result
def get_member_yearmonth_act_uid(level: int):
    """
    两个CSV文件来自道斌制作的会员带留存活跃。

    :param level: 1 黄金会员 2 钻石会员 3 企业会员 4 保险
    :return: {201905: {123,234,345} }
    """
    ym_uid = {}

    level_file_dict = {1: 'gold.csv', 2: 'diamond.csv', 3: 'enterprise.csv', 4: 'insurance.csv'}

    with open(INPUT_DIR + 'active_uid/' + level_file_dict[level]) as fin:
        for idx, line in enumerate(fin):
            line_content = line.split(',')
            yearmonth, uid = int(line_content[0]), int(line_content[1])

            if yearmonth not in ym_uid:
                ym_uid[yearmonth] = set()

            ym_uid[yearmonth].add(uid)

            if idx % 1000000 == 0:
                print('member ym active_uid %s lines processed.' % idx)

    return ym_uid


@serial_result
def get_doctor_act_uid():
    """
    获取 医生月活
    :param utype:
    :param year:
    :return: {201905: {123,234,345} }
    """

    ym_uid = {}

    with open(INPUT_DIR + 'active_uid/doctor.csv') as fin:
        for idx, line in enumerate(fin):
            line_content = line.split(',')
            yearmonth, uid = int(line_content[0]), int(line_content[1])

            if yearmonth not in ym_uid:
                ym_uid[yearmonth] = set()

            ym_uid[yearmonth].add(uid)

            if idx % 1000000 == 0:
                print('doctor ym active_uid %s lines processed.' % idx)

    return ym_uid


def get_doctor_act_by_ym(ym):
    """
    ym获取医生月活
    :param ym:
    :return:
    """
    return get_doctor_act_uid().get(ym, set())


def convert_txt():
    for k, v in get_yearmonth_act_uid(1).items():
        print('processing %s' % k)
        with open(OUTPUT_DIR + 'active_uid/inhosp_%s.txt' % k, 'w') as fout:
            fout.writelines(str(i) + '\n' for i in v)
    for k, v in get_yearmonth_act_uid(0).items():
        print('processing %s' % k)
        with open(OUTPUT_DIR + 'active_uid/outhosp_%s.txt' % k, 'w') as fout:
            fout.writelines(str(i) + '\n' for i in v)


# 读取活跃数据,根据type读取不同csv文件
# @serial_result
def get_active_user(utype):
    active_user_dict = {}
    fileName = INPUT_DIR
    if utype == 1:
        fileName = INPUT_DIR + 'active_uid/医生月活.csv'
    elif utype == 2:
        fileName = INPUT_DIR + 'active_uid/医院用户月活.csv'
    elif utype == 3:
        fileName = INPUT_DIR + 'active_uid/非医院用户月活.csv'
    elif utype == 4:
        fileName = INPUT_DIR + 'active_uid/company_active.csv'
    elif utype == 5:
        fileName = INPUT_DIR + 'active_uid/insurance_active.csv'
    elif utype == 6:
        fileName = INPUT_DIR + 'active_uid/yiye_active.csv'

    with open(fileName) as fin:
        for idx, line in enumerate(fin):
            if idx == 0:
                continue
            line_content = line.split(',')
            yearmonth, uid = line_content[0].replace('"', ''), int(line_content[1].replace('"', ''))
            if yearmonth not in active_user_dict:
                active_user_dict[yearmonth] = set()
            active_user_dict[yearmonth].add(uid)
    return active_user_dict


# 判断是否是活跃用户
def is_active(user_id, time, active_user_dict):
    ym = get_ym(time)
    if str(ym) not in active_user_dict.keys():
        return False
    user_id_list = active_user_dict['{ym}']
    if user_id in user_id_list:
        return True
    else:
        return False
