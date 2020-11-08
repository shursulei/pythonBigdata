#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/8 9:31
# @Author  : shursulei
# @Site    : 
# @File    : rand.py
# @Software: PyCharm Community Edition
# @describe: �������Ĺ���
'''
import datetime
# import calendar
# import math
# import random
#
#
# def random_split(total, num):
#     """
#     ��total������䵽num�����磺��100��Ѫ�ǣ���������50���û���ʹ��random_split(100, 50)����
#     :param total:
#     :param num:
#     :return: ����Ϊnum���ܺ�Ϊtotal��list
#     """
#     if num > total:
#         result = []
#         for i in range(total):
#             result.append(1)
#         for i in range(num - total):
#             result.append(0)
#         return result
#     elif num == 0:
#         return []
#     else:
#         dividers = sorted(random.sample(range(1, total), num - 1))
#         return [a - b for a, b in zip(dividers + [total], [0] + dividers)]
#
#
# def random_avg_split(total, num, rate=.8):
#     """
#     ��total���ջ���ƽ��ֵ������䵽num
#     :param total:
#     :param num:
#     :param rate: ���ױ�����0��1֮�䡣1��ʾ��ȫƽ�����䣬0��ʾ��ȫ������䡣
#     :return: ����Ϊnum���ܺ�Ϊtotal��list
#     """
#     base = int(total / num * rate)  # 80%���䵽ÿ��num�У���֤����ƽ��
#     random_result = random_split(total - base * num, num)
#     return [base + random_result[i] for i in range(num)]
#
#
# def random_split_with_limit(total, num, min_value, max_value):
#     """��total������䵽num��"""
#     while True:
#         num_array = [random.randint(min_value, max_value) for _ in range(num)]
#         if sum(num_array) == total:
#             return num_array
#
#
# def random_date(start, end):
#     """
#     This function will return a random datetime between two datetime
#     objects.
#     """
#     if start > end:
#         print('start time bigger than end, use start.')
#         return start
#     delta = end - start
#     int_delta = ((delta.days * 24 * 60 * 60) + delta.seconds) or 1
#     random_second = random.randrange(int_delta)
#     return start + datetime.timedelta(seconds=random_second)
#
#
# def random_split_with_base(total, num, base):
#     """
#     ���ٷ��� base �� �����
#     :param base:
#     :param total:
#     :param num:
#     :return:
#     """
#     if total < num * base:
#         raise ValueError(f'total {total} < num {num} * base_num {base}')
#
#     random_result = random_split(total - base * num, num)
#     return [base + random_result[i] for i in range(num)]
#
#
# def random_probabilities(origin_probability, num, rate=.8):
#     """
#     ������������ĸ��ʱ����random.choices(list, weights=weight)[0]����probability table����gen_doctor.py 112�У�
#     :param origin_probability:ԭʼ�ĸ��ʱ�����[2,15,5,2]
#     :param num:��Ҫ�Ĳ������ĸ��ʱ������������2���Ͱ���ԭʼ���ʱ�����2���µĸ��ʱ�
#     :param rate:�����ʣ�0��ȫ�����1��ȫƽ��
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, num, rate) for y in [x * int(num * 10) for x in origin_probability]]))
#
#
# def random_year_probabilities(origin_probability):
#     """
#     ��ԭʼ�����������365��ÿ�յĸ���.
#     :param origin_probability:
#     :return:
#     """
#     return random_year_probabilities_with_rate(origin_probability, 0.5)
#
#
# def random_year_probabilities_with_rate(origin_probability, rate):
#     """
#     ��ԭʼ�����������365��ÿ�յĸ���
#     :param origin_probability:
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, 365, rate) for y in [x * 10000 for x in origin_probability]]))
#
#
# def random_month_probabilities(origin_probability):
#     """
#     ��ԭʼ�����������31��ÿ�յĸ���
#     :param origin_probability:
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, 31, 0.5) for y in [x * 10000 for x in origin_probability]]))
#
#

# todo
def random_probabilities_by_num_rate(origin_probability, num, rate):
    return list(zip(*[random_avg_split(y, num, rate) for y in [x * 1000 for x in origin_probability]]))
#
#
# def random_hos_probabilities(origin_probability):
#     """
#     ��ԭʼ�����������365��ÿ�յĸ���
#     :param origin_probability:
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, 1700, 0.5) for y in [x * 100000 for x in origin_probability]]))
#
#
# def random_hos_time_probabilities(origin_probability, day_count):
#     """
#     ��ԭʼ�����������365��ÿ�յĸ���
#     :param origin_probability:
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, day_count, 0.5) for y in [x * 100000 for x in origin_probability]]))
#
#
# def random_percentage_value(obj_list, key, float_value):
#     """
#     key���Եı���ֵ���в���
#     :param obj_list:
#     :param key:
#     :param float_value:
#     :return:
#     """
#     random_array = list(
#         zip(*[random_avg_split(y, 2, float_value) for y in [int(x[key] * 1000000) for x in obj_list]]))[0]
#     total_value = sum(random_array)
#     idx = 0
#     for obj in obj_list:
#         obj[key] = random_array[idx] / total_value
#         idx += 1
#     return obj_list
#
#
# def random_pick(some_list, probabilities):
#     x = random.uniform(0, 1)
#     cumulative_probability = 0.0
#     for item, item_probability in zip(some_list, probabilities):
#         cumulative_probability += item_probability
#         if x < cumulative_probability: break
#     return item
#
#
# def get_rand_one_from_list(ids, index=None):
#     if ids is None:
#         return None
#     if index is not None:
#         return ids[index]
#     l = len(ids)
#     if l == 0:
#         return None
#     if l > 1:
#         rid = random.randint(0, l - 1)
#     else:
#         rid = 0
#     return ids[rid]
#
#
# def get_random_patient_code(code_random_bit):
#     random_code = random.randint(math.pow(10, code_random_bit - 1) + 1, math.pow(10, code_random_bit) - 1)
#     return random_code
#
#
class Day_Hour_Dim_Randomer():
    """
    ���������
    ���� �����
    ��Ҫ����
    ��СʱȨ������ 24����
    ��������Ȩ��Ȩ�� 31����
    """

    def __init__(self, origin_hour_probabilities, origin_month_day_probabilities, month_hour_probabilities_wave=0.7,
                 month_day_hour_probabilities_wave=0.65,
                 month_day_probabilities_wave=0.7):
        """

        :param origin_hour_probabilities: Сʱ���� 24����
        :param origin_month_day_probabilities: ÿ����ֲ����� 31 ����
        :param hour_probabilities_wave: Сʱ���ʲ���
        :param month_day_hour_probabilities_wave: ÿ����ֲ����� ����
        """
        self._origin_hour_probabilities = origin_hour_probabilities
        self._origin_month_day_probabilities = origin_month_day_probabilities

        # ���� 12���µĸ���
        self._month_hour = list(zip(
            *[random_avg_split(y, 12, month_hour_probabilities_wave) for y in
              [x * 100 for x in origin_hour_probabilities]]))
        # ÿ��ʱ�����
        self._year_hour_weight = [
            list(zip(*[random_avg_split(y, 31, month_day_hour_probabilities_wave) for y in [x * 100 for x in m]])) for m
            in
            self._month_hour]

        self._month_day_hour = list(zip(*[random_avg_split(y, 12, month_day_probabilities_wave) for y in
                                          [x * 100 for x in origin_month_day_probabilities]]))
#
    def get_dt(self, day: datetime.date):
        """
        ��ȡ���� ʱ���
        ͨ�� origin_hour_probabilities ����ó�
        :param day:
        :return:
        """
        hour = random.choices(range(24), self._year_hour_weight[day.month - 1][day.day - 1])[0]
        return datetime.datetime(day.year, day.month, day.day, hour, minute=random.randint(0, 59),
                                 second=random.randint(0, 59))

#     def get_day(self, ym: int):
#         """
#         ��ȡ���� ��ʱ���
#         ͨ�� origin_month_day_probabilities ����
#         :param ym:
#         :return:
#         """
#         m = int(ym % 100)
#         year = int(ym / 100)
#         month_days = calendar.monthrange(year, m)[1]
#         return datetime.date(year, m,
#                              random.choices(range(1, month_days + 1), self._month_day_hour[m - 1][0:month_days])[0])
#
#     def get_month_datatime_list(self, ym: int, need_count: int):
#         r = []
#         for i in range(need_count):
#             day = self.get_day(ym)
#             r.append(self.get_dt(day))
#
#         return r
#
#
# ����Ȩ�������ȡԪ��
def get_element_by_random(target_list, weight_list):
    return random.choices(target_list, weight_list)[0]
#
#
#
#
# import datetime
# import random
#
#
# def random_split(total, num):
#     """
#     ��total������䵽num�����磺��100��Ѫ�ǣ���������50���û���ʹ��random_split(100, 50)����
#     :param total:
#     :param num:
#     :return: ����Ϊnum���ܺ�Ϊtotal��list
#     """
#     if num > total:
#         result = []
#         for i in range(total):
#             result.append(1)
#         for i in range(num - total):
#             result.append(0)
#         return result
#     elif num == 0:
#         return []
#     else:
#         dividers = sorted(random.sample(range(1, total), num - 1))
#         return [a - b for a, b in zip(dividers + [total], [0] + dividers)]
#
#
# def random_avg_split(total, num, rate=0.8):
#     """
#     ��total���ջ���ƽ��ֵ������䵽num
#     :param total:
#     :param num:
#     :param rate: ���ױ�����0��1֮�䡣1��ʾ��ȫƽ�����䣬0��ʾ��ȫ������䡣
#     :return: ����Ϊnum���ܺ�Ϊtotal��list
#     """
#     base = int(total / num * rate)  # 80%���䵽ÿ��num�У���֤����ƽ��
#     random_result = random_split(total - base * num, num)
#     return [base + random_result[i] for i in range(num)]
#
#
# def random_date(start, end):
#     """
#     This function will return a random datetime between two datetime
#     objects.
#     """
#     if start > end:
#         print('start time bigger than end, use start.')
#         return start
#     delta = end - start
#     int_delta = ((delta.days * 24 * 60 * 60) + delta.seconds) or 1
#     random_second = random.randrange(int_delta)
#     return start + datetime.timedelta(seconds=random_second)
#
#
# # �������ߣ�ȡ��ÿ��Ԫ�صĸ���ֵ
# # ���ʱ�չ����ĸ���
# # ���磺
# # ԭʼ���ݣ�[0, 1, 2]
# # �������ߣ�[2, 3, 4]������������߱�ʾ��2/(2+3+4)�ĸ���ȡ��ԭʼ�����е�0��3/(2+3+4)�ĸ���ȡ��ԭʼ�����е�1
# # ���ʱ�����ԭʼ���ݺ͸�������չ����ı�����������ǣ�[0, 0, 1, 1, 1, 2, 2, 2, 2]��
# # ���list����ֱ��ʹ��random.choice(list)��ѡ�������������ߵ���ֵ��
#
# def random_probabilities(origin_probability, num, rate=0.8):
#     """
#     ������������ĸ������ߡ����random_pick����probability table�����·���
#     :param origin_probability:ԭʼ�ĸ������ߣ�����[2,15,5,2]
#     :param num:��Ҫ�Ĳ������ĸ��ʱ������������2���Ͱ���ԭʼ���ʱ�����2���µĸ��ʱ�
#     :param rate:�����ʣ�0��ȫ�����1��ȫƽ��
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, num, rate) for y in [x * int(num * 10) for x in origin_probability]]))
#
#
# def expand_probability_table(origin, origin_probability):
#     """
#     ���ո������߰�ԭʼ����չ���ɸ��ʱ�
#     :param origin: ԭʼ����list������[0, 1]
#     :param origin_probability: ���ʱ�����[2, 3]��������ʱ��ʾ��2 / (2 + 3)�ĸ���ȡ��0��3 / (2 + 3)�ĸ���ȡ��1
#     :return: [0, 0, 1, 1, 1]��������ʹ��random.choice()����������εĸ���������
#     """
#     return [z for x, y in zip(origin, origin_probability) for z in [x] * int(y)]
#
#
# def random_probability_tables(origin, origin_probability, num, rate=0.8):
#     """
#     ����������ʱ�չ��������ʹ��__probability_demo�еķ�����������������
#     :param origin: ԭʼ����list������[0, 1]
#     :param origin_probability: ���ʱ�����[2, 3]��������ʱ��ʾ��2 / (2 + 3)�ĸ���ȡ��0��3 / (2 + 3)�ĸ���ȡ��1
#     :param num: �����ĸ��ʱ������������1���������������ÿ��չ���ĸ��ʱ���ôҪ��365��
#     :param rate: �����ʣ�0��ȫ�����1��ȫƽ��
#     :return: ������ʱ�
#     """
#     probabilities = random_probabilities(origin_probability, num, rate)
#     return [expand_probability_table(origin, i) for i in probabilities]
#
#
# def random_pick(target_list, weights):
#     return random.choices(target_list, weights)[0]
#
#
# # Сʱ��������demo��
# # ��Сʱ����ÿ����ĸ���չ���ɸ��ʱ�����ֱ�ӴӸ��ʱ������ȡ1��������Ϊ��Сʱ����ȡ���Ľ��ֵ��
# # ���������random.choiceֱ�Ӵ�չ���ĸ��ʱ�ȡ�������ٶ�ҪԶ��random_pick��
# # ע���������ֻ����ʾ������ɸ���table����ΪЧ�����⣬����ֱ�ӵ��á�
# def __probability_demo():
#     _24hour = [i for i in range(24)]
#     hour_probability = [5, 3, 1, 2, 1, 1, 2, 3, 8, 10, 14, 12, 10, 12, 12, 11, 10, 8, 8, 20, 8, 8, 8, 5]
#     hour_probability_table = expand_probability_table(_24hour, hour_probability)  # ����������ã���random.choice��������
#     hour = random.choice(hour_probability_table)  # ���������Сʱ
#     return hour
#


import datetime
import random


def random_split(total, num):
    """
    ��total������䵽num�����磺��100��Ѫ�ǣ���������50���û���ʹ��random_split(100, 50)����
    :param total:
    :param num:
    :return: ����Ϊnum���ܺ�Ϊtotal��list
    """
    if num > total:
        result = []
        for i in range(total):
            result.append(1)
        for i in range(num - total):
            result.append(0)
        return result
    elif num == 0:
        return []
    else:
        dividers = sorted(random.sample(range(1, total), num - 1))
        return [a - b for a, b in zip(dividers + [total], [0] + dividers)]


def random_avg_split(total, num, rate=0.8):
    """
    ��total���ջ���ƽ��ֵ������䵽num
    :param total:
    :param num:
    :param rate: ���ױ�����0��1֮�䡣1��ʾ��ȫƽ�����䣬0��ʾ��ȫ������䡣
    :return: ����Ϊnum���ܺ�Ϊtotal��list
    """
    base = int(total / num * rate)  # 80%���䵽ÿ��num�У���֤����ƽ��
    random_result = random_split(total - base * num, num)
    return [base + random_result[i] for i in range(num)]


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    if start > end:
        print('start time bigger than end, use start.')
        return start
    delta = end - start
    int_delta = ((delta.days * 24 * 60 * 60) + delta.seconds) or 1
    random_second = random.randrange(int_delta)
    return start + datetime.timedelta(seconds=random_second)


# �������ߣ�ȡ��ÿ��Ԫ�صĸ���ֵ
# ���ʱ�չ����ĸ���
# ���磺
# ԭʼ���ݣ�[0, 1, 2]
# �������ߣ�[2, 3, 4]������������߱�ʾ��2/(2+3+4)�ĸ���ȡ��ԭʼ�����е�0��3/(2+3+4)�ĸ���ȡ��ԭʼ�����е�1
# ���ʱ�����ԭʼ���ݺ͸�������չ����ı�����������ǣ�[0, 0, 1, 1, 1, 2, 2, 2, 2]��
# ���list����ֱ��ʹ��random.choice(list)��ѡ�������������ߵ���ֵ��

def random_probabilities(origin_probability, num, rate=0.8):
    """
    ������������ĸ������ߡ����random_pick����probability table�����·���
    :param origin_probability:ԭʼ�ĸ������ߣ�����[2,15,5,2]
    :param num:��Ҫ�Ĳ������ĸ��ʱ������������2���Ͱ���ԭʼ���ʱ�����2���µĸ��ʱ�
    :param rate:�����ʣ�0��ȫ�����1��ȫƽ��
    :return:
    """
    return list(zip(*[random_avg_split(y, num, rate) for y in [x * int(num * 10) for x in origin_probability]]))


def expand_probability_table(origin, origin_probability):
    """
    ���ո������߰�ԭʼ����չ���ɸ��ʱ�
    :param origin: ԭʼ����list������[0, 1]
    :param origin_probability: ���ʱ�����[2, 3]��������ʱ��ʾ��2 / (2 + 3)�ĸ���ȡ��0��3 / (2 + 3)�ĸ���ȡ��1
    :return: [0, 0, 1, 1, 1]��������ʹ��random.choice()����������εĸ���������
    """
    return [z for x, y in zip(origin, origin_probability) for z in [x] * int(y)]


def random_probability_tables(origin, origin_probability, num, rate=0.8):
    """
    ����������ʱ�չ��������ʹ��__probability_demo�еķ�����������������
    :param origin: ԭʼ����list������[0, 1]
    :param origin_probability: ���ʱ�����[2, 3]��������ʱ��ʾ��2 / (2 + 3)�ĸ���ȡ��0��3 / (2 + 3)�ĸ���ȡ��1
    :param num: �����ĸ��ʱ������������1���������������ÿ��չ���ĸ��ʱ���ôҪ��365��
    :param rate: �����ʣ�0��ȫ�����1��ȫƽ��
    :return: ������ʱ�
    """
    probabilities = random_probabilities(origin_probability, num, rate)
    return [expand_probability_table(origin, i) for i in probabilities]


def random_pick(target_list, weights):
    return random.choices(target_list, weights)[0]


# Сʱ��������demo��
# ��Сʱ����ÿ����ĸ���չ���ɸ��ʱ�����ֱ�ӴӸ��ʱ������ȡ1��������Ϊ��Сʱ����ȡ���Ľ��ֵ��
# ���������random.choiceֱ�Ӵ�չ���ĸ��ʱ�ȡ�������ٶ�ҪԶ��random_pick��
# ע���������ֻ����ʾ������ɸ���table����ΪЧ�����⣬����ֱ�ӵ��á�
def __probability_demo():
    _24hour = [i for i in range(24)]
    hour_probability = [5, 3, 1, 2, 1, 1, 2, 3, 8, 10, 14, 12, 10, 12, 12, 11, 10, 8, 8, 20, 8, 8, 8, 5]
    hour_probability_table = expand_probability_table(_24hour, hour_probability)  # ����������ã���random.choice��������
    hour = random.choice(hour_probability_table)  # ���������Сʱ
    return hour



import numpy as np

if __name__ == '__main__':
    '''
    test
    '''
    split = random_split(100, 4)
    print(split)
    print(np.sum(split))

    print("---------------")
    avg_split = random_avg_split(100, 4, 0.5)
    print(avg_split)
