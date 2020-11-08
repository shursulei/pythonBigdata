"""
病人
身高 体重等 工具类

"""
import random
import typing


def get_height_weitht_by_age(age: int, sex: int) -> typing.Tuple[int, float]:
    """
    通过 年龄和性别 获取 身高体重
    :param age: 年龄
    :param sex: 1 男 2 女
    :return:
    """

    # 男
    male_h_w_dict = {2: (102.2, 16.6),
                     3: (102.2, 16.6),
                     4: (107.8, 18.3),
                     5: (114, 20.6),
                     6: (119.7, 23),
                     7: (126.6, 26.6),
                     8: (132, 29.9),
                     9: (137.2, 33.6),
                     10: (142.1, 37.2),
                     11: (148.1, 41.9),
                     12: (154.5, 46.6),
                     13: (161.4, 52),
                     14: (166.5, 56.2),
                     15: (169.8, 59.5),
                     16: (171.4, 61.5),
                     17: (172.1, 63.3),
                     18: (172, 63.5),
                     19: (172.4, 63.5),
                     20: (171.9, 67.2),
                     21: (171.9, 67.2),
                     22: (171.9, 67.2),
                     23: (171.9, 67.2),
                     24: (171.9, 67.2),
                     25: (171.6, 70.4),
                     26: (171.6, 70.4),
                     27: (171.6, 70.4),
                     28: (171.6, 70.4),
                     29: (171.6, 70.4),
                     30: (170.8, 71.4),
                     31: (170.8, 71.4),
                     32: (170.8, 71.4),
                     33: (170.8, 71.4),
                     34: (170.8, 71.4),
                     35: (169.9, 71.5),
                     36: (169.9, 71.5),
                     37: (169.9, 71.5),
                     38: (169.9, 71.5),
                     39: (169.9, 71.5),
                     40: (169, 71.2),
                     41: (169, 71.2),
                     42: (169, 71.2),
                     43: (169, 71.2),
                     44: (169, 71.2),
                     45: (168.7, 71.2),
                     46: (168.7, 71.2),
                     47: (168.7, 71.2),
                     48: (168.7, 71.2),
                     49: (168.7, 71.2),
                     50: (168.3, 70.6),
                     51: (168.3, 70.6),
                     52: (168.3, 70.6),
                     53: (168.3, 70.6),
                     54: (168.3, 70.6),
                     55: (167.5, 69.1),
                     56: (167.5, 69.1),
                     57: (167.5, 69.1),
                     58: (167.5, 69.1),
                     59: (167.5, 69.1),
                     60: (166.1, 67.6),
                     61: (166.1, 67.6),
                     62: (166.1, 67.6),
                     63: (166.1, 67.6),
                     64: (166.1, 67.6),
                     65: (165.4, 66.6),
                     66: (165.4, 66.6),
                     67: (165.4, 66.6),
                     68: (165.4, 66.6),
                     69: (165.4, 66.6)}

    # 女
    female_h_w_dict = {2: (100.9, 15.9),
                       3: (100.9, 15.9),
                       4: (106.5, 17.5),
                       5: (112.7, 19.6),
                       6: (118.1, 21.6),
                       7: (125.1, 24.7),
                       8: (130.5, 27.6),
                       9: (136.3, 31.3),
                       10: (142.6, 35.5),
                       11: (149.3, 40.6),
                       12: (153.7, 44.5),
                       13: (157, 48),
                       14: (158.7, 50.4),
                       15: (159.4, 51.6),
                       16: (159.8, 52.7),
                       17: (159.8, 53),
                       18: (159.4, 52.6),
                       19: (160.2, 52.4),
                       20: (159.9, 53.8),
                       21: (159.9, 53.8),
                       22: (159.9, 53.8),
                       23: (159.9, 53.8),
                       24: (159.9, 53.8),
                       25: (159.6, 55.3),
                       26: (159.6, 55.3),
                       27: (159.6, 55.3),
                       28: (159.6, 55.3),
                       29: (159.6, 55.3),
                       30: (159.1, 56.8),
                       31: (159.1, 56.8),
                       32: (159.1, 56.8),
                       33: (159.1, 56.8),
                       34: (159.1, 56.8),
                       35: (158.5, 57.8),
                       36: (158.5, 57.8),
                       37: (158.5, 57.8),
                       38: (158.5, 57.8),
                       39: (158.5, 57.8),
                       40: (157.8, 59),
                       41: (157.8, 59),
                       42: (157.8, 59),
                       43: (157.8, 59),
                       44: (157.8, 59),
                       45: (157.7, 59.7),
                       46: (157.7, 59.7),
                       47: (157.7, 59.7),
                       48: (157.7, 59.7),
                       49: (157.7, 59.7),
                       50: (157.7, 60.4),
                       51: (157.7, 60.4),
                       52: (157.7, 60.4),
                       53: (157.7, 60.4),
                       54: (157.7, 60.4),
                       55: (156.8, 59.6),
                       56: (156.8, 59.6),
                       57: (156.8, 59.6),
                       58: (156.8, 59.6),
                       59: (156.8, 59.6),
                       60: (155.3, 59.7),
                       61: (155.3, 59.7),
                       62: (155.3, 59.7),
                       63: (155.3, 59.7),
                       64: (155.3, 59.7),
                       65: (154.4, 59.2),
                       66: (154.4, 59.2),
                       67: (154.4, 59.2),
                       68: (154.4, 59.2),
                       69: (154.4, 59.2)
                       }

    if age < 2:
        age = 2
    elif age > 69:
        age = 69
    if sex == 1:
        # 男
        hw = male_h_w_dict.get(age)
    else:
        hw = female_h_w_dict.get(age)

    # 身高标准差 0.1 / 3 体重标准差 hw[1] * 0.1 / 3
    return round(random.normalvariate(hw[0], hw[0] * 0.1 / 3)), round(
        random.normalvariate(hw[1], hw[1] * 0.1 / 3), 1)


def get_diabetes_type(disease:str):
    """
    疾病子类
    :param disease: 疾病大类 英文
    :return:
    """

    diabetes_type_f_dict = {
        'tumour': lambda: 1,
        'thyropathy': lambda: random.choices(range(11),
                                             weights=[5980, 582, 723, 120, 286, 945, 53, 66, 22, 15, 252])[0],
        'other': lambda: random.randint(0, 7),
        'obesity': lambda: 1 if random.random() < 0.99 else 2,
        'hyperuricemia': lambda: 1,
        'hypertension': lambda: 1,
        'dyslipidemia': lambda: random.choices((1, 2, 3), weights=[12, 7, 1])[0],
        'diabetes': lambda: random.choices(range(10),
                                           weights=[163, 528, 6269, 1568, 631, 2088, 191, 190, 122, 200])[0],
    }
    diabetes_type_f = diabetes_type_f_dict.get(disease, lambda: 0)

    return diabetes_type_f()