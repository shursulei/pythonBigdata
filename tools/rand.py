#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/8 9:31
# @Author  : shursulei
# @Site    : 
# @File    : rand.py
# @Software: PyCharm Community Edition
# @describe: 随机分配的工具
'''
import datetime
# import calendar
# import math
# import random
#
#
# def random_split(total, num):
#     """
#     将total随机分配到num。例如：将100个血糖，随机分配给50个用户，使用random_split(100, 50)分配
#     :param total:
#     :param num:
#     :return: 长度为num，总和为total的list
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
#     将total按照基本平均值随机分配到num
#     :param total:
#     :param num:
#     :param rate: 保底比例，0到1之间。1表示完全平均分配，0表示完全随机分配。
#     :return: 长度为num，总和为total的list
#     """
#     base = int(total / num * rate)  # 80%分配到每个num中，保证大致平衡
#     random_result = random_split(total - base * num, num)
#     return [base + random_result[i] for i in range(num)]
#
#
# def random_split_with_limit(total, num, min_value, max_value):
#     """将total随机分配到num中"""
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
#     至少分配 base 到 结果中
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
#     产生多个浮动的概率表。配合random.choices(list, weights=weight)[0]或者probability table（在gen_doctor.py 112行）
#     :param origin_probability:原始的概率表，例如[2,15,5,2]
#     :param num:需要的波动过的概率表数量，如果传2，就按照原始概率表，产生2个新的概率表
#     :param rate:波动率，0完全随机，1完全平均
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, num, rate) for y in [x * int(num * 10) for x in origin_probability]]))
#
#
# def random_year_probabilities(origin_probability):
#     """
#     按原始概率随机生成365个每日的概率.
#     :param origin_probability:
#     :return:
#     """
#     return random_year_probabilities_with_rate(origin_probability, 0.5)
#
#
# def random_year_probabilities_with_rate(origin_probability, rate):
#     """
#     按原始概率随机生成365个每日的概率
#     :param origin_probability:
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, 365, rate) for y in [x * 10000 for x in origin_probability]]))
#
#
# def random_month_probabilities(origin_probability):
#     """
#     按原始概率随机生成31个每日的概率
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
#     按原始概率随机生成365个每日的概率
#     :param origin_probability:
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, 1700, 0.5) for y in [x * 100000 for x in origin_probability]]))
#
#
# def random_hos_time_probabilities(origin_probability, day_count):
#     """
#     按原始概率随机生成365个每日的概率
#     :param origin_probability:
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, day_count, 0.5) for y in [x * 100000 for x in origin_probability]]))
#
#
# def random_percentage_value(obj_list, key, float_value):
#     """
#     key属性的比例值进行波动
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
    按年给数据
    月日 随机类
    需要参数
    日小时权重曲线 24个点
    月日曲线权重权重 31个点
    """

    def __init__(self, origin_hour_probabilities, origin_month_day_probabilities, month_hour_probabilities_wave=0.7,
                 month_day_hour_probabilities_wave=0.65,
                 month_day_probabilities_wave=0.7):
        """

        :param origin_hour_probabilities: 小时概率 24个点
        :param origin_month_day_probabilities: 每月天分布概率 31 个点
        :param hour_probabilities_wave: 小时概率波动
        :param month_day_hour_probabilities_wave: 每月天分布概率 波动
        """
        self._origin_hour_probabilities = origin_hour_probabilities
        self._origin_month_day_probabilities = origin_month_day_probabilities

        # 生成 12个月的概率
        self._month_hour = list(zip(
            *[random_avg_split(y, 12, month_hour_probabilities_wave) for y in
              [x * 100 for x in origin_hour_probabilities]]))
        # 每天时间概率
        self._year_hour_weight = [
            list(zip(*[random_avg_split(y, 31, month_day_hour_probabilities_wave) for y in [x * 100 for x in m]])) for m
            in
            self._month_hour]

        self._month_day_hour = list(zip(*[random_avg_split(y, 12, month_day_probabilities_wave) for y in
                                          [x * 100 for x in origin_month_day_probabilities]]))
#
    def get_dt(self, day: datetime.date):
        """
        获取当天 时间点
        通过 origin_hour_probabilities 计算得出
        :param day:
        :return:
        """
        hour = random.choices(range(24), self._year_hour_weight[day.month - 1][day.day - 1])[0]
        return datetime.datetime(day.year, day.month, day.day, hour, minute=random.randint(0, 59),
                                 second=random.randint(0, 59))

#     def get_day(self, ym: int):
#         """
#         获取当月 天时间点
#         通过 origin_month_day_probabilities 计算
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
# 根据权重随机获取元素
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
#     将total随机分配到num。例如：将100个血糖，随机分配给50个用户，使用random_split(100, 50)分配
#     :param total:
#     :param num:
#     :return: 长度为num，总和为total的list
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
#     将total按照基本平均值随机分配到num
#     :param total:
#     :param num:
#     :param rate: 保底比例，0到1之间。1表示完全平均分配，0表示完全随机分配。
#     :return: 长度为num，总和为total的list
#     """
#     base = int(total / num * rate)  # 80%分配到每个num中，保证大致平衡
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
# # 概率曲线：取到每个元素的概率值
# # 概率表：展开后的概率
# # 例如：
# # 原始数据：[0, 1, 2]
# # 概率曲线：[2, 3, 4]，这个概率曲线表示有2/(2+3+4)的概率取到原始数据中的0，3/(2+3+4)的概率取到原始数据中的1
# # 概率表：按照原始数据和概率曲线展开后的表，上面的例子是：[0, 0, 1, 1, 1, 2, 2, 2, 2]。
# # 这个list可以直接使用random.choice(list)来选择出满足概率曲线的数值。
#
# def random_probabilities(origin_probability, num, rate=0.8):
#     """
#     产生多个浮动的概率曲线。配合random_pick或者probability table（在下方）
#     :param origin_probability:原始的概率曲线，例如[2,15,5,2]
#     :param num:需要的波动过的概率表数量，如果传2，就按照原始概率表，产生2个新的概率表
#     :param rate:波动率，0完全随机，1完全平均
#     :return:
#     """
#     return list(zip(*[random_avg_split(y, num, rate) for y in [x * int(num * 10) for x in origin_probability]]))
#
#
# def expand_probability_table(origin, origin_probability):
#     """
#     按照概率曲线把原始数据展开成概率表。
#     :param origin: 原始数据list。比如[0, 1]
#     :param origin_probability: 概率表。比如[2, 3]，这个概率表表示有2 / (2 + 3)的概率取到0，3 / (2 + 3)的概率取到1
#     :return: [0, 0, 1, 1, 1]。这个结果使用random.choice()，即满足入参的概率条件。
#     """
#     return [z for x, y in zip(origin, origin_probability) for z in [x] * int(y)]
#
#
# def random_probability_tables(origin, origin_probability, num, rate=0.8):
#     """
#     产生多个概率表并展开，可以使用__probability_demo中的方法来产生概率数据
#     :param origin: 原始数据list。比如[0, 1]
#     :param origin_probability: 概率表。比如[2, 3]，这个概率表表示有2 / (2 + 3)的概率取到0，3 / (2 + 3)的概率取到1
#     :param num: 产生的概率表数量（比如从1个年概率曲线生成每日展开的概率表，那么要传365）
#     :param rate: 波动率，0完全随机，1完全平均
#     :return: 多个概率表
#     """
#     probabilities = random_probabilities(origin_probability, num, rate)
#     return [expand_probability_table(origin, i) for i in probabilities]
#
#
# def random_pick(target_list, weights):
#     return random.choices(target_list, weights)[0]
#
#
# # 小时概率曲线demo。
# # 把小时按照每个点的概率展开成概率表，这样直接从概率表中随机取1个数，即为按小时概率取出的结果值。
# # 这个方案（random.choice直接从展开的概率表取数）的速度要远比random_pick快
# # 注意这个方法只是演示如何生成概率table，因为效率问题，不能直接调用。
# def __probability_demo():
#     _24hour = [i for i in range(24)]
#     hour_probability = [5, 3, 1, 2, 1, 1, 2, 3, 8, 10, 14, 12, 10, 12, 12, 11, 10, 8, 8, 20, 8, 8, 8, 5]
#     hour_probability_table = expand_probability_table(_24hour, hour_probability)  # 保存这个引用，供random.choice反复调用
#     hour = random.choice(hour_probability_table)  # 随机出来的小时
#     return hour
#


import datetime
import random


def random_split(total, num):
    """
    将total随机分配到num。例如：将100个血糖，随机分配给50个用户，使用random_split(100, 50)分配
    :param total:
    :param num:
    :return: 长度为num，总和为total的list
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
    将total按照基本平均值随机分配到num
    :param total:
    :param num:
    :param rate: 保底比例，0到1之间。1表示完全平均分配，0表示完全随机分配。
    :return: 长度为num，总和为total的list
    """
    base = int(total / num * rate)  # 80%分配到每个num中，保证大致平衡
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


# 概率曲线：取到每个元素的概率值
# 概率表：展开后的概率
# 例如：
# 原始数据：[0, 1, 2]
# 概率曲线：[2, 3, 4]，这个概率曲线表示有2/(2+3+4)的概率取到原始数据中的0，3/(2+3+4)的概率取到原始数据中的1
# 概率表：按照原始数据和概率曲线展开后的表，上面的例子是：[0, 0, 1, 1, 1, 2, 2, 2, 2]。
# 这个list可以直接使用random.choice(list)来选择出满足概率曲线的数值。

def random_probabilities(origin_probability, num, rate=0.8):
    """
    产生多个浮动的概率曲线。配合random_pick或者probability table（在下方）
    :param origin_probability:原始的概率曲线，例如[2,15,5,2]
    :param num:需要的波动过的概率表数量，如果传2，就按照原始概率表，产生2个新的概率表
    :param rate:波动率，0完全随机，1完全平均
    :return:
    """
    return list(zip(*[random_avg_split(y, num, rate) for y in [x * int(num * 10) for x in origin_probability]]))


def expand_probability_table(origin, origin_probability):
    """
    按照概率曲线把原始数据展开成概率表。
    :param origin: 原始数据list。比如[0, 1]
    :param origin_probability: 概率表。比如[2, 3]，这个概率表表示有2 / (2 + 3)的概率取到0，3 / (2 + 3)的概率取到1
    :return: [0, 0, 1, 1, 1]。这个结果使用random.choice()，即满足入参的概率条件。
    """
    return [z for x, y in zip(origin, origin_probability) for z in [x] * int(y)]


def random_probability_tables(origin, origin_probability, num, rate=0.8):
    """
    产生多个概率表并展开，可以使用__probability_demo中的方法来产生概率数据
    :param origin: 原始数据list。比如[0, 1]
    :param origin_probability: 概率表。比如[2, 3]，这个概率表表示有2 / (2 + 3)的概率取到0，3 / (2 + 3)的概率取到1
    :param num: 产生的概率表数量（比如从1个年概率曲线生成每日展开的概率表，那么要传365）
    :param rate: 波动率，0完全随机，1完全平均
    :return: 多个概率表
    """
    probabilities = random_probabilities(origin_probability, num, rate)
    return [expand_probability_table(origin, i) for i in probabilities]


def random_pick(target_list, weights):
    return random.choices(target_list, weights)[0]


# 小时概率曲线demo。
# 把小时按照每个点的概率展开成概率表，这样直接从概率表中随机取1个数，即为按小时概率取出的结果值。
# 这个方案（random.choice直接从展开的概率表取数）的速度要远比random_pick快
# 注意这个方法只是演示如何生成概率table，因为效率问题，不能直接调用。
def __probability_demo():
    _24hour = [i for i in range(24)]
    hour_probability = [5, 3, 1, 2, 1, 1, 2, 3, 8, 10, 14, 12, 10, 12, 12, 11, 10, 8, 8, 20, 8, 8, 8, 5]
    hour_probability_table = expand_probability_table(_24hour, hour_probability)  # 保存这个引用，供random.choice反复调用
    hour = random.choice(hour_probability_table)  # 随机出来的小时
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
