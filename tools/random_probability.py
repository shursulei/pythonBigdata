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
# �������ߣ�ȡ��ÿ��Ԫ�صĸ���ֵ
# ���ʱ�չ����ĸ���
# ���磺
# ԭʼ���ݣ�[0, 1, 2]
# �������ߣ�[2, 3, 4]������������߱�ʾ��2/(2+3+4)�ĸ���ȡ��ԭʼ�����е�0��3/(2+3+4)�ĸ���ȡ��ԭʼ�����е�1
# ���ʱ�����ԭʼ���ݺ͸�������չ����ı�����������ǣ�[0, 0, 1, 1, 1, 2, 2, 2, 2]��
# ���list����ֱ��ʹ��random.choice(list)��ѡ�������������ߵ���ֵ��
import calendar
import random
from datetime import datetime

from lru import LRU

from tools.rand import random_avg_split


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


class HourMinuteProbabilityGenerator:
    """
    ʹ�÷�����
    generator = HourMinuteProbabilityGenerator(2019, [1,2,3,4,...,1440])
    new_create_time = generator.get_datetime(datetime(2019, 1, 12, x, x, x)) ����ʱ��Ϊ����ֵ��datetime����

    ע�⣺���class���أ���Ҫ����generator���÷���ʹ�ã���Ҫÿ��newһ���µ�Generator��
    """

    def __init__(self, year: int, probability):
        """
        :param year: ÿ��Generatorֻ����1��ĸ��ʣ����ﴫ���
        :param probability: �������ߣ�Ҫ��1440����
        """
        if len(probability) != 24 * 60:
            raise Exception("Since every day has 24 * 60 minutes, param probability must have 1440 elements.")

        self.year = year
        year_total_days = 365 + calendar.isleap(year)
        self.day_probability = random_probabilities(probability, year_total_days)
        self.minute_sequence = [i for i in range(24 * 60)]

        # ������ƣ�����չ���ĸ��ʱ�
        # ���ʱ�չ������ٶ�Զ����ʹ��weights
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
        month_days = calendar.monthrange(year, month)[1]  # ��ǰ���м���
        num_each_day = random_avg_split(num, month_days, 0.9)  # ����ÿ������������

        for day, day_num in zip(range(1, month_days + 1), num_each_day):
            this_day = datetime(year, month, day)  # ����00:00:00����Ϊ��������
            result.extend([self.get_datetime(this_day) for i in range(day_num)])
        return result
