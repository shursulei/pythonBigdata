import datetime

from dateutil.relativedelta import relativedelta

from tools.datetime_util import get_ym, get_month_start_end_time
from tools.db import select_by_mcp_with_dict
from tools.serial import serial_result


@serial_result
def get_prescription_doctor_by_reg_month():
    """
    处方医生 ym 注册 row
    :return:
    """

    sql = """select bui.id as id,bui.name as name,bui.dept as dept,bui.title as title,
                        h.name as hospital_name,convert(bui.biz_id , SIGNED) as hospital_id,bui.gmt_create
                            from base_user_info bui left join hospital h on bui.biz_id = h.id 
                            where tag = 'PRESCRIPTION' and utype = 1
                            """
    doctor_list = select_by_mcp_with_dict(sql)
    result = {}
    for d in doctor_list:
        ym = get_ym(d['gmt_create'])
        if ym not in result:
            result[ym] = []
        result[ym].append(d)

    return result


@serial_result
def get_doctor_by_reg_month():
    """
    处方医生 ym 注册 row
    :return:
    """

    sql = """select bui.id as id,bui.name as name,bui.dept as dept,bui.title as title,
                        h.name as hospital_name,convert(bui.biz_id , SIGNED) as hospital_id,bui.gmt_create
                            from base_user_info bui left join hospital h on bui.biz_id = h.id 
                            where utype = 1
                            """
    doctor_list = select_by_mcp_with_dict(sql)
    result = {}
    for d in doctor_list:
        ym = get_ym(d['gmt_create'])
        if ym not in result:
            result[ym] = []
        result[ym].append(d)

    return result


# def get_drp_by_ids(patient_ids):
#     """
#     医患关系 查询
#     :param patient_ids:
#     :return:
#     """
#     result = select_by_mcp_with_dict(f"""
#        SELECT patient_id,doctor_id FROM doctor_patient_relationship
#        where status = 0 and patient_id in (  {','.join([str(i) for i in patient_ids])}  )
#            """)
#
#     return {dpr['patient_id']: dpr['doctor_id'] for dpr in result}


def get_ym_orders(ym_date: datetime.date):
    """
    按月份返回订单

    {gmt_create月份: [row,row]}

    { 201905: {123,124} }

    :param dtype: 0 非医院 1 医院
    :returns
    """
    ym_date = ym_date.replace(day=1)
    next_ym_date = ym_date + relativedelta(months=1)
    next_ym_date = next_ym_date.replace(day=1)

    order_result = select_by_mcp_with_dict(
        '''select user_id,order_id,gmt_create,gmt_modify
        from orders
        -- order_type 2 6 处方订单
        where order_type in (2,6) and  gmt_create >= '{ym_date:%Y-%m-%d}' and gmt_create < '{next_ym_date:%Y-%m-%d}'
        ''')
    result = []
    for order in order_result:
        result.append(order)

    return result


def get_user_dict_by_ids(sql, ids):
    users = select_by_mcp_with_dict(sql.format(','.join([str(i) for i in ids])))

    u_list = {i['id']: i for i in users}

    return u_list


def get_user_list_by_ids(ids):
    sql = '''
    select * from base_user_info where id in ({})
    '''
    return select_by_mcp_with_dict(sql.format(','.join([str(i) for i in ids])), database='user_dataset')




def get_prescription_order(date):
    sql = '''
       SELECT o.order_id AS order_id, o.gmt_create AS order_time, a.`id` AS patient_id, a.`name` AS patient_name, 
         a.`sex`, a.`birthday`, a.`disease_name`, a.`referer`, a.`tag` AS patient_tag
           , convert(a.biz_id, SIGNED) AS hospital_id, a.province
           , a.city, a.gmt_create AS patient_register_time, a.mobile
       FROM mall.orders o
       INNER JOIN base_user_info a ON o.user_id = a.id
       WHERE o.order_type IN (2, 6) AND DATE_FORMAT(o.`gmt_create`, '%Y-%m-%d') = '{date}'
        AND o.delete_status = 0
    order by o.gmt_create
       '''
    order_result = select_by_mcp_with_dict(sql)

    return order_result
def get_prescription_order7(date):
    sql = '''
       SELECT o.order_id AS order_id, o.gmt_create AS order_time, a.`id` AS patient_id, a.`name` AS patient_name, 
        t.gmt_create AS pay_time,o.sent_time AS sent_time,o.order_type AS order_type,
         a.`sex`, a.`birthday`, a.`disease_name`, a.`referer`, a.`tag` AS patient_tag
           , convert(a.biz_id, SIGNED) AS hospital_id, a.province
           , a.city, a.gmt_create AS patient_register_time, a.mobile
       FROM mall.orders o
       INNER JOIN base_user_info a ON o.user_id = a.id
       INNER JOIN mall.pay t on o.pay_id=t.PAY_ID
       WHERE o.order_type IN (2,6,7) AND DATE_FORMAT(o.`gmt_create`, '%Y-%m-%d') = '{date}'
        AND o.delete_status = 0 
        and (o.parent_id is null or o.order_id=o.parent_id)
    order by o.gmt_create
       '''
    order_result = select_by_mcp_with_dict(sql)

    return order_result


# 获取医患绑定关系
def get_patient_doctor_relation(patient_ids):
    patient_doctor_id_dict = {}
    sql = '''
     SELECT a.`id` AS patient_id,
           b.`id` AS doctor_id
     FROM `base_user_info` a
     INNER JOIN `base_user_info` b ON a.`referer`= b.code
     WHERE a.`id` IN ({patient_ids})
    '''
    result = select_by_mcp_with_dict(sql)
    for value in result:
        patient_id = value['patient_id']
        doctor_id = value['doctor_id']
        if patient_doctor_id_dict.get(patient_id) is None:
            doctor_id_set = set()
            doctor_id_set.add(doctor_id)
            patient_doctor_id_dict[patient_id] = doctor_id_set
        else:
            doctor_id_set = patient_doctor_id_dict[patient_id]
            doctor_id_set.add(doctor_id)
            patient_doctor_id_dict[patient_id] = doctor_id_set

    return patient_doctor_id_dict


# 从处方表中获取医生信息
def get_doctor_from_prescription(year_month_time):
    start_date_str, end_date_str = get_month_start_end_time(year_month_time)
    sql = '''
        SELECT DISTINCT(doctor_id)
        FROM ih.prescription
        WHERE gmt_create >= '{start_date_str}'
        AND gmt_create <= '{end_date_str}'
    '''
    result = select_by_mcp_with_dict(sql)
    return [value['doctor_id'] for value in result]

#获取排除连续活跃医生的月活医生
def get_active_doctor(active_table_name):
    get_active_doctor_sql='''SELECT uid FROM user_dataset.{active_table_name} WHERE utype =1 AND uid NOT IN 
    (SELECT DISTINCT(uid) FROM ih.doctor_active_prescription)'''.format(active_table_name=active_table_name)
    result = select_by_mcp_with_dict(get_active_doctor_sql)
    return [value['uid'] for value in result]

def get_all_active_doctor():
    get_all_active_doctor_sql='''SELECT d.date,u.* from user_dataset.base_user_info u,ih.doctor_active_prescription d
WHERE u.id=d.uid and d.mark=1'''
    result = select_by_mcp_with_dict(get_all_active_doctor_sql)
    all_active_doctor_dick={}
    for value in  result:
        if not all_active_doctor_dick.keys().__contains__(value['date']):
            all_active_doctor_dick[value['date']]=[]
        all_active_doctor_dick[value['date']].append(value)
    return all_active_doctor_dick

def get_doctor_list_by_date():
    sql = '''
    select * from user_dataset.base_user_info where id in (SELECT DISTINCT(uid) FROM ih.doctor_active_prescription)
    '''
    return select_by_mcp_with_dict(sql)


def get_doctor_active_prescription_len(ym):
    sql = '''
    SELECT DISTINCT(uid) FROM ih.doctor_active_prescription where `month`= '{ym}'
    '''
    return select_by_mcp_with_dict(sql)