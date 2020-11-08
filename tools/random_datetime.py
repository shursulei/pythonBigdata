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


