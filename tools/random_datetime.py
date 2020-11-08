#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/8 9:32
# @Author  : shursulei
# @Site    : 
# @File    : random_datetime.py
# @Software: PyCharm Community Edition
# @describe:
'''
# 概率曲线：取到每个元素的概率值
# 概率表：展开后的概率
# 例如：
# 原始数据：[0, 1, 2]
# 概率曲线：[2, 3, 4]，这个概率曲线表示有2/(2+3+4)的概率取到原始数据中的0，3/(2+3+4)的概率取到原始数据中的1
# 概率表：按照原始数据和概率曲线展开后的表，上面的例子是：[0, 0, 1, 1, 1, 2, 2, 2, 2]。
# 这个list可以直接使用random.choice(list)来选择出满足概率曲线的数值。
import calendar
import random
from datetime import datetime

from tools.rand import random_avg_split


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


class RandomDatetimeGenerator:
    def __init__(self, year: int, probability):
        self.year = year
        self.day_probability = random_probabilities(probability, 365 + calendar.isleap(year))
        self.minute_table = [i for i in range(24 * 60)]

    def get_datetime(self, dt: datetime):
        # if self.year != dt.year:
        #     raise ValueError(f"Year {dt.year} from datetime not equals Generator's {self.year}")
        probability = self.day_probability[dt.timetuple().tm_yday - 1]
        minute_of_day = random_pick(self.minute_table, probability)
        return dt.replace(hour=minute_of_day // 60, minute=minute_of_day % 60, second=random.randint(0, 59))


