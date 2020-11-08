#!/usr/bin/env python

# encoding: utf-8
'''
# @Time    : 2020/11/8 9:38
# @Author  : shursulei
# @Site    : 
# @File    : random_probability.py
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

from lru import LRU

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


class HourMinuteProbabilityGenerator:
    """
    使用方法：
    generator = HourMinuteProbabilityGenerator(2019, [1,2,3,4,...,1440])
    new_create_time = generator.get_datetime(datetime(2019, 1, 12, x, x, x)) 传入时间为任意值的datetime类型

    注意：这个class很重，需要保存generator引用反复使用，不要每次new一个新的Generator。
    """

    def __init__(self, year: int, probability):
        """
        :param year: 每个Generator只负责1年的概率，这里传年份
        :param probability: 概率曲线，要有1440个点
        """
        if len(probability) != 24 * 60:
            raise Exception("Since every day has 24 * 60 minutes, param probability must have 1440 elements.")

        self.year = year
        year_total_days = 365 + calendar.isleap(year)
        self.day_probability = random_probabilities(probability, year_total_days)
        self.minute_sequence = [i for i in range(24 * 60)]

        # 缓存机制，缓存展开的概率表
        # 概率表展开后的速度远快于使用weights
        self.probability_table_cache = LRU(50)
        self.day_missed_times = {i: 0 for i in range(1, year_total_days + 1)}

    def get_datetime(self, dt: datetime):
        if self.year != dt.year:
            raise Exception("Year {dt.year} from datetime not equals Generator's {self.year}")

        day_of_year = dt.timetuple().tm_yday - 1

        if self.day_missed_times[day_of_year] > 5:
            self.probability_table_cache[day_of_year] = expand_probability_table(self.minute_sequence,
                                                                                 self.day_probability[day_of_year])
            self.day_missed_times[day_of_year] = 0

        if day_of_year in self.probability_table_cache:
            minute_of_day = random.choice(self.probability_table_cache[day_of_year])
        else:
            minute_of_day = random_pick(self.minute_sequence, self.day_probability[day_of_year])
            self.day_missed_times[day_of_year] += 1

        return dt.replace(hour=minute_of_day // 60, minute=minute_of_day % 60, second=random.randint(0, 59))

    def batch_get_datetime(self, year: int, month: int, num: int):
        result = []
        month_days = calendar.monthrange(year, month)[1]  # 当前月有几天
        num_each_day = random_avg_split(num, month_days, 0.9)  # 计算每天分配多少数量

        for day, day_num in zip(range(1, month_days + 1), num_each_day):
            this_day = datetime(year, month, day)  # 当天00:00:00，作为基础数据
            result.extend([self.get_datetime(this_day) for i in range(day_num)])
        return result
