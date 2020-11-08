# -*- coding: utf-8 -*-
import calendar
import datetime
import logging
import random
import sys
import typing
from pathlib import Path
from tools.random_datetime import RandomDatetimeGenerator
from tqdm import tqdm

from prescription.work import INPUT_DIR, OUTPUT_DIR
from prescription.work.active_uid import get_active_user
from prescription.work.gen_pres_util import get_prescription_order, get_user_list_by_ids, get_patient_doctor_relation, \
    get_active_doctor, get_all_active_doctor, get_doctor_list_by_date, get_doctor_active_prescription_len, \
    get_prescription_order7
from tools.body_util import get_height_weitht_by_age
from tools.datetime_util import all_format_str, get_ym, random_start_end_date
from tools.db import MYSQL_NULL, add_quote, quote_or_MYSQL_NULL, add_quote_v2, quote_or_MYSQL_NULL_v2
from tools.iterator_util import iterate_elements_page, DEFAULT_PAGE_SIZE
from tools.rand import random_avg_split, random_probabilities_by_num_rate, Day_Hour_Dim_Randomer, get_element_by_random, \
    random_probabilities
from tools.xls import xls_reader, cell_to_datetime

PRES_INSERT_SQL = '''insert into prescription(`type`, user_base_info_id, patient_id, `name`, age, gender, symptom, illness, doctor_id,
                          doctor_name, doctor_title, doctor_hospital_name, doctor_dept_name, dept, auditor_id,
                          auditor_name, audit_time, order_time, expired_time, self_image_url, supply_image_url,
                          phone_number, remark, prescription_auditor_name, prescription_auditor_id,
                          prescription_audit_time, prescription_reauditor_id, prescription_reauditor_name,
                          prescription_reaudit_time, prescription_audit_status, status, gmt_create, gmt_modify,
                          prescription_remark, doctor_sign_url, prescription_auditor_sign_url,
                          prescription_reauditor_sign_url, region, height, weight, patient_advisory_id,
                          replace_prescription_id, mall_order_time, audit_type,t_order_id,redundancy) values '''
PRES_TEMPLATE_SQL = '''
({type}, {user_base_info_id}, {patient_id}, {name}, {age}, 
{gender}, {symptom}, {illness}, {doctor_id}, {doctor_name}, 
{doctor_title}, {doctor_hospital_name}, {doctor_dept_name}, {dept}, {auditor_id}, 
{auditor_name}, {audit_time}, {order_time}, {expired_time}, {self_image_url}, 
{supply_image_url}, {phone_number}, {remark}, {prescription_auditor_name}, {prescription_auditor_id}, 
{prescription_audit_time}, {prescription_reauditor_id}, {prescription_reauditor_name}, {prescription_reaudit_time}, {prescription_audit_status}, 
{status}, {gmt_create}, {gmt_modify}, {prescription_remark}, {doctor_sign_url}, 
{prescription_auditor_sign_url}, {prescription_reauditor_sign_url}, {region}, {height}, {weight}, 
{patient_advisory_id}, {replace_prescription_id}, {mall_order_time}, {audit_type},{t_order_id},{redundancy})'''

# 医院24小时分布
hospital_three_hour_probabilities = random_probabilities_by_num_rate(
    [446, 524, 516, 500, 721, 1156, 2298, 3226, 4703, 5057, 5045, 5500, 5315, 5787, 6048, 5894, 5698, 6356, 5947, 6244,
     6534, 6476, 6221, 3778], 3, 0.9)

# 非医院24小时分布
common_three_hour_probabilities = random_probabilities_by_num_rate(
    [55, 58, 58, 57, 83, 135, 252, 346, 488, 515, 501, 563, 495, 531, 573, 563, 559, 549, 576, 631, 645, 647, 593, 504],
    3, 0.9)

# 月份概率分布
three_month_day_probabilities = random_probabilities_by_num_rate([1 for i in range(31)], 3, 0.9)

# 医院患者小时分布
HOSPITAL_DHDR_dict = {
    2018: Day_Hour_Dim_Randomer(hospital_three_hour_probabilities[0], three_month_day_probabilities[0], 0.9, 0.9, 0.8),
    2019: Day_Hour_Dim_Randomer(hospital_three_hour_probabilities[1], three_month_day_probabilities[1], 0.9, 0.9, 0.8),
    2020: Day_Hour_Dim_Randomer(hospital_three_hour_probabilities[2], three_month_day_probabilities[2], 0.9, 0.9, 0.8)
}

# 非医院患者小时分布
COMMON_DHDR_dict = {
    2018: Day_Hour_Dim_Randomer(common_three_hour_probabilities[0], three_month_day_probabilities[0], 0.9, 0.9, 0.8),
    2019: Day_Hour_Dim_Randomer(common_three_hour_probabilities[1], three_month_day_probabilities[1], 0.9, 0.9, 0.8),
    2020: Day_Hour_Dim_Randomer(common_three_hour_probabilities[2], three_month_day_probabilities[2], 0.9, 0.9, 0.8)
}

# 1天1440个分钟
hour_minute = [i for i in range(1440)]
# 1440分钟对应的概率
# hour_minute_probability = [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
#                            7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
#                            7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
#                            7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
#                            7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6,
#                            6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
#                            7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8,
#                            8, 8, 8, 8, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11,
#                            11, 11, 11, 12, 12, 12, 12, 12, 13, 13, 13, 13, 13, 13, 13, 14, 14, 14, 14, 14, 14, 14, 14,
#                            15, 15, 15, 15, 15, 15, 16, 16, 16, 17, 17, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20, 20, 21,
#                            21, 21, 21, 22, 22, 22, 23, 23, 23, 24, 24, 24, 24, 25, 25, 25, 26, 26, 26, 27, 27, 27, 28,
#                            28, 28, 28, 29, 29, 30, 30, 30, 30, 31, 31, 31, 32, 33, 33, 33, 34, 34, 34, 35, 35, 36, 36,
#                            37, 37, 38, 38, 39, 39, 39, 40, 40, 41, 41, 41, 42, 42, 43, 43, 44, 44, 45, 45, 45, 46, 46,
#                            47, 47, 47, 48, 48, 48, 49, 49, 50, 50, 50, 51, 51, 51, 52, 52, 53, 53, 54, 54, 54, 55, 55,
#                            55, 56, 56, 57, 57, 58, 58, 59, 59, 59, 60, 60, 61, 61, 61, 62, 62, 63, 63, 63, 64, 64, 65,
#                            65, 65, 66, 66, 66, 67, 67, 68, 68, 68, 69, 69, 69, 69, 70, 70, 70, 70, 71, 71, 71, 71, 72,
#                            72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 73, 73, 73, 73, 73, 73, 73, 73,
#                            73, 73, 74, 74, 74, 74, 74, 74, 75, 75, 75, 75, 76, 76, 76, 77, 77, 77, 77, 78, 78, 78, 79,
#                            79, 79, 79, 80, 80, 80, 81, 81, 82, 82, 82, 83, 83, 83, 84, 84, 84, 85, 85, 86, 86, 86, 87,
#                            87, 88, 88, 88, 89, 89, 90, 90, 90, 91, 91, 92, 92, 93, 93, 94, 94, 95, 96, 96, 97, 97, 98,
#                            98, 99, 100, 100, 101, 102, 102, 103, 104, 104, 105, 106, 106, 107, 107, 108, 108, 109, 109,
#                            110, 110, 110, 111, 111, 111, 111, 111, 111, 111, 112, 112, 112, 112, 112, 112, 112, 112,
#                            112, 112, 112, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113,
#                            113, 113, 113, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 114, 115, 115, 115, 115,
#                            115, 115, 115, 115, 116, 116, 116, 116, 116, 116, 116, 117, 117, 117, 117, 117, 117, 118,
#                            118, 118, 118, 118, 119, 119, 119, 119, 120, 120, 120, 120, 121, 121, 121, 121, 121, 122,
#                            122, 123, 123, 123, 123, 124, 124, 124, 125, 125, 125, 125, 125, 126, 126, 126, 126, 126,
#                            127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
#                            127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 126, 126, 126, 126, 126, 126, 126,
#                            125, 125, 125, 125, 125, 124, 124, 124, 124, 123, 123, 123, 122, 122, 122, 121, 121, 121,
#                            121, 120, 120, 120, 120, 119, 119, 119, 118, 118, 118, 118, 118, 117, 117, 117, 117, 117,
#                            116, 116, 116, 116, 116, 115, 115, 115, 115, 115, 114, 114, 114, 114, 114, 113, 113, 113,
#                            113, 112, 112, 112, 112, 112, 111, 111, 111, 111, 110, 110, 110, 110, 110, 109, 109, 109,
#                            109, 109, 108, 108, 108, 108, 107, 107, 107, 107, 107, 106, 106, 106, 106, 106, 106, 105,
#                            105, 105, 105, 105, 104, 104, 104, 104, 104, 104, 104, 104, 103, 103, 103, 103, 103, 103,
#                            103, 103, 102, 102, 102, 102, 102, 102, 102, 102, 102, 101, 101, 101, 101, 101, 101, 101,
#                            101, 101, 101, 101, 101, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100,
#                            100, 100, 100, 100, 100, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99,
#                            99, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 97,
#                            97, 97, 97, 97, 97, 97, 97, 97, 97, 97, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98, 98,
#                            99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 99, 100, 100, 100, 100, 100, 100, 101, 101,
#                            101, 101, 101, 101, 102, 102, 102, 102, 102, 102, 103, 103, 103, 103, 104, 104, 104, 104,
#                            105, 105, 105, 105, 106, 106, 107, 107, 107, 107, 108, 108, 108, 108, 109, 109, 109, 109,
#                            109, 109, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110,
#                            110, 110, 110, 110, 110, 110, 110, 110, 110, 109, 109, 109, 109, 109, 109, 109, 109, 108,
#                            108, 108, 108, 108, 108, 108, 108, 107, 107, 107, 107, 106, 106, 106, 106, 106, 106, 105,
#                            105, 105, 105, 105, 105, 105, 105, 105, 104, 104, 104, 104, 104, 104, 104, 104, 104, 104,
#                            104, 104, 104, 104, 104, 104, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103, 103,
#                            103, 103, 103, 103, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102, 102,
#                            102, 102, 102, 102, 102, 102, 102, 102, 102, 103, 103, 103, 103, 103, 103, 103, 103, 103,
#                            104, 104, 104, 104, 104, 105, 105, 105, 105, 105, 106, 106, 106, 107, 107, 107, 108, 108,
#                            108, 109, 109, 109, 110, 110, 110, 111, 111, 112, 112, 113, 113, 113, 114, 114, 115, 115,
#                            116, 116, 117, 117, 118, 118, 118, 119, 119, 120, 120, 121, 121, 122, 122, 123, 123, 123,
#                            124, 124, 125, 125, 125, 126, 126, 127, 127, 127, 127, 128, 128, 128, 129, 129, 129, 130,
#                            130, 130, 130, 131, 131, 131, 132, 132, 132, 132, 133, 133, 133, 134, 134, 134, 134, 135,
#                            135, 135, 135, 135, 136, 136, 136, 136, 136, 137, 137, 137, 137, 137, 137, 138, 138, 138,
#                            138, 138, 138, 138, 138, 138, 138, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139, 139,
#                            139, 139, 139, 139, 139, 140, 140, 140, 140, 140, 140, 140, 140, 141, 141, 141, 141, 142,
#                            142, 142, 142, 143, 143, 143, 144, 144, 144, 144, 145, 145, 145, 146, 146, 146, 147, 147,
#                            147, 147, 148, 148, 148, 148, 149, 149, 149, 149, 149, 149, 149, 150, 150, 150, 150, 150,
#                            150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150,
#                            150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 150, 149, 149, 149, 149, 149, 149,
#                            149, 149, 149, 149, 149, 148, 148, 148, 148, 148, 148, 148, 148, 147, 147, 147, 147, 147,
#                            147, 147, 146, 146, 146, 146, 146, 145, 145, 145, 145, 145, 144, 144, 144, 143, 143, 143,
#                            143, 142, 142, 141, 141, 141, 140, 140, 139, 139, 138, 138, 138, 137, 137, 136, 136, 135,
#                            134, 134, 133, 132, 132, 131, 131, 130, 129, 128, 127, 127, 126, 125, 124, 123, 122, 121,
#                            120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 105, 104, 103, 102,
#                            100, 99, 98, 96, 95, 93, 92, 91, 89, 87, 86, 85, 83, 81, 80, 78, 77, 76, 75, 73, 71, 70, 68,
#                            66, 65, 63, 61, 60, 58, 56, 55, 53, 51, 49, 48, 46, 44, 43, 41, 39, 37, 35, 34, 32, 30, 28,
#                            27, 25, 23, 21, 19, 17, 15, 14, 12, 10, 7]

hour_minute_probability = [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
                           18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
                           19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19,
                           19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
                           18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
                           18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18,
                           18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20,
                           20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21,
                           21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22,
                           22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22,
                           22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24,
                           24, 24, 24, 24, 24, 25, 25, 25, 25, 25, 25, 25, 26, 26, 26, 26, 26, 26, 26, 27, 27, 27, 27,
                           27, 28, 28, 28, 28, 28, 28, 29, 29, 29, 29, 29, 30, 30, 30, 30, 30, 31, 31, 31, 31, 31, 32,
                           32, 32, 32, 32, 33, 33, 33, 33, 33, 34, 34, 34, 34, 34, 35, 35, 35, 35, 35, 36, 36, 36, 36,
                           36, 37, 37, 37, 37, 38, 38, 38, 38, 38, 39, 39, 39, 39, 40, 40, 40, 41, 41, 41, 41, 42, 42,
                           42, 43, 43, 43, 44, 44, 44, 45, 45, 46, 46, 47, 47, 47, 48, 48, 49, 49, 50, 50, 51, 51, 52,
                           52, 53, 54, 54, 55, 55, 56, 56, 57, 58, 58, 59, 59, 60, 61, 61, 62, 63, 63, 64, 64, 65, 66,
                           66, 67, 68, 68, 69, 69, 70, 71, 71, 72, 72, 73, 74, 74, 75, 75, 76, 76, 77, 77, 78, 79, 79,
                           79, 80, 80, 81, 81, 82, 82, 83, 83, 83, 84, 84, 84, 85, 85, 86, 86, 86, 87, 87, 87, 88, 88,
                           88, 88, 89, 89, 89, 90, 90, 90, 90, 91, 91, 91, 91, 92, 92, 92, 92, 92, 93, 93, 93, 93, 94,
                           94, 94, 94, 95, 95, 95, 95, 95, 96, 96, 96, 96, 96, 97, 97, 97, 97, 97, 98, 98, 98, 98, 98,
                           99, 99, 99, 99, 99, 99, 100, 100, 100, 100, 100, 100, 101, 101, 101, 101, 101, 101, 101, 102,
                           102, 102, 102, 102, 102, 102, 102, 103, 103, 103, 103, 103, 103, 103, 103, 103, 104, 104,
                           104, 104, 104, 104, 104, 104, 104, 105, 105, 105, 105, 105, 105, 105, 105, 105, 106, 106,
                           106, 106, 106, 106, 106, 106, 106, 107, 107, 107, 107, 107, 107, 107, 107, 108, 108, 108,
                           108, 108, 108, 108, 108, 108, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 110, 110,
                           110, 110, 110, 110, 110, 110, 110, 110, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111,
                           111, 111, 111, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112,
                           112, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113,
                           113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113,
                           113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113,
                           113, 113, 113, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 111, 111, 111, 111,
                           111, 111, 110, 110, 110, 110, 110, 110, 109, 109, 109, 109, 108, 108, 108, 108, 108, 107,
                           107, 107, 107, 107, 106, 106, 106, 106, 106, 106, 106, 105, 105, 105, 105, 105, 105, 105,
                           105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105,
                           105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 106, 106, 106, 106, 106, 106,
                           106, 106, 106, 106, 106, 106, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107,
                           107, 107, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108,
                           109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 110, 110, 110, 110,
                           110, 110, 110, 110, 110, 110, 110, 110, 110, 111, 111, 111, 111, 111, 111, 111, 111, 111,
                           111, 111, 111, 111, 111, 111, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112,
                           112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112,
                           112, 112, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 112,
                           112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112,
                           112, 112, 112, 112, 112, 112, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111,
                           111, 111, 111, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 109, 109, 109,
                           109, 109, 109, 109, 109, 109, 109, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 107,
                           107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 106, 106, 106, 106, 106, 106, 106,
                           106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106,
                           106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106,
                           106, 106, 106, 106, 106, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107,
                           107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 108, 108, 108, 108, 108,
                           108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 109, 109, 109, 109, 109, 109, 109,
                           109, 109, 109, 109, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 111, 111,
                           111, 111, 111, 111, 111, 111, 111, 111, 112, 112, 112, 112, 112, 112, 112, 112, 113, 113,
                           113, 113, 113, 113, 113, 114, 114, 114, 114, 114, 114, 115, 115, 115, 115, 115, 116, 116,
                           116, 116, 116, 117, 117, 117, 117, 117, 118, 118, 118, 118, 118, 119, 119, 119, 119, 119,
                           120, 120, 120, 120, 120, 121, 121, 121, 121, 121, 121, 121, 122, 122, 122, 122, 122, 122,
                           122, 122, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 124, 124, 124,
                           124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124,
                           124, 124, 124, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125,
                           125, 125, 125, 125, 125, 125, 125, 125, 125, 126, 126, 126, 126, 126, 126, 126, 126, 126,
                           126, 126, 126, 126, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127,
                           127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 126, 126, 126, 126, 126, 126,
                           126, 126, 126, 126, 125, 125, 125, 125, 125, 125, 125, 124, 124, 124, 124, 124, 124, 124,
                           124, 123, 123, 123, 123, 123, 123, 123, 122, 122, 122, 122, 122, 122, 122, 121, 121, 121,
                           121, 121, 121, 121, 121, 121, 121, 121, 121, 120, 120, 120, 120, 120, 120, 120, 120, 120,
                           120, 120, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121,
                           121, 121, 121, 121, 121, 120, 120, 120, 120, 120, 120, 120, 119, 119, 119, 119, 119, 118,
                           118, 118, 118, 117, 117, 117, 116, 116, 116, 115, 115, 115, 114, 114, 113, 113, 112, 112,
                           112, 111, 110, 110, 109, 109, 108, 108, 107, 106, 106, 105, 104, 104, 103, 102, 101, 100, 99,
                           97, 96, 95, 93, 91, 90, 88, 86, 84, 83, 81, 79, 77, 75, 73, 71, 69, 67, 65, 63, 61, 59, 58,
                           56, 54, 52, 50, 48, 46, 45, 43, 41, 39, 38, 36, 34, 33, 32, 30, 29, 28, 26, 25, 24, 23, 22,
                           21, 20, 20, 19, 19, 18, 18, 18]
# 按月拆成每天生成处方(历史处方)
month_redundancy_dict = {}


def gen_history_prescription_by_month(yearmonth_datetime, prescription_doctor_num,
                                      patient_hospital_num, patient_common_num, prescription_num):
    ym = get_ym(yearmonth_datetime)  # datetime.datetime(2020, 1, 7, 0, 0) -> 202001
    # 获取当月活跃医生
    # active_doctor_list = get_active_user_data(str(ym), 1)
    active_table_name='new_all_user_month_active'+str(ym)
    active_doctor_id_list = get_active_doctor(active_table_name)
    active_doctor_list = get_user_list_by_ids(set(active_doctor_id_list))
    # 获取有处方权的医生 todo
    active_prescription_doctor_list = [d for d in active_doctor_list if d['tag'] == 'PRESCRIPTION']
    #获取连续月活医生的数量
    doctor_active_prescription_len=get_doctor_active_prescription_len(ym)
    if doctor_active_prescription_len:
        doctor_active_prescription_len_int=len(doctor_active_prescription_len)
    else:
        doctor_active_prescription_len_int=0
    # 从活跃处方医生中选取一定数量的处方医生组成医生池 todo
    #YANGHAO,3379为doctor_active_prescription处方量值
    if ym==202011:
        #数不够
        doctor_pool_list = random.sample(active_prescription_doctor_list,int(len(active_prescription_doctor_list)))
    else:
        doctor_pool_list = random.sample(active_prescription_doctor_list, int(prescription_doctor_num)-doctor_active_prescription_len_int)
    # doctor_pool_list = random.sample(active_prescription_doctor_list, int(len(active_prescription_doctor_list)*2/3))

    month_days = calendar.monthrange(yearmonth_datetime.year, yearmonth_datetime.month)[1]
    start_day = datetime.date(yearmonth_datetime.year, yearmonth_datetime.month, 1)
    end_day = datetime.date(yearmonth_datetime.year, yearmonth_datetime.month, day=month_days)

    # 将医生按照注册日期分为当前月注册与历史月注册
    history_month_doctor_list, current_month_doctor_list = get_user_list_group_by_month(doctor_pool_list, start_day)
    day_user_dict = get_month_day_user_register(current_month_doctor_list)

    # 取每天连续活跃医生
    # YANGHAO
    all_active_doctor_dick = get_all_active_doctor()
    # 当月处方订单先直接生成处方
    order_hospital_patient_id_set, order_common_patient_id_set, order_prescription_num = gen_order_prescription_by_month(
        start_day, end_day, history_month_doctor_list, day_user_dict, all_active_doctor_dick)

    # 根据订单生成数据统计剩余处方量，并构造剩余患者池
    redundancy_prescription_num, patient_pool_list = get_patient_doctor_pool(yearmonth_datetime,
                                                                             order_hospital_patient_id_set,
                                                                             order_common_patient_id_set,
                                                                             order_prescription_num, prescription_num,
                                                                             patient_hospital_num, patient_common_num)
    # 获取患者、医生用户基本信息
    patient_dict = get_user_dict(patient_pool_list)
    doctor_dict = get_user_dict(doctor_pool_list)

    # 生成多余的数据

    # 获取冗余处方量
    prescription_dict_list = gen_redundancy_prescription_by_month_v2(start_day, end_day, month_days,
                                                                     history_month_doctor_list, day_user_dict,
                                                                     patient_pool_list, doctor_dict,
                                                                     redundancy_prescription_num, yearmonth_datetime,
                                                                     all_active_doctor_dick)

    # 根据<patient_id,doctor_id,gmt_create>三元组组装处方详情数据

    # 添加连续活跃医生
    all_active_doctor_list = get_doctor_list_by_date()
    for user in all_active_doctor_list:
        doctor_dict[user['id']] = user

    redundancy_prescription_list = get_redundancy_prescription_list(prescription_dict_list, patient_dict, doctor_dict,
                                                                    yearmonth_datetime)

    # 写入文件
    if redundancy_prescription_list:
        logging.info('month:{ym},redundancy_prescription_list write sql start')
        iterate_elements_page(redundancy_prescription_list, write_pres_sql, DEFAULT_PAGE_SIZE, ym_date=start_day)
        logging.info('month:{ym},redundancy_prescription_list write end')
    a = 0
    for i in prescription_dict_list:
        if i['redundancy'] == 112:
            a = a + 1
        month_redundancy_dict[ym] = a


# 除去处方订单生成的处方量，计算剩余医生患者池
def get_patient_doctor_pool(yearmonth_datetime, order_hospital_patient_id_set, order_common_patient_id_set,
                            order_prescription_num, prescription_num, patient_hospital_num, patient_common_num):
    ym = get_ym(yearmonth_datetime)
    # 当月活跃医院患者
    hospital_user_list = get_active_user_data(str(ym), 2)
    hospital_user_list = filter_user(hospital_user_list, yearmonth_datetime)

    # 当月活跃非医院患者
    common_user_list = get_active_user_data(str(ym), 3)
    common_user_list = filter_user(common_user_list, yearmonth_datetime)

    # 剩余医院用户
    left_hospital_num = patient_hospital_num - len(order_hospital_patient_id_set)
    # 剩余非医院用户
    left_common_num = patient_common_num - len(order_common_patient_id_set)

    # 当月需要冗余处方量
    redundancy_prescription_num = prescription_num - order_prescription_num

    # 当月需要冗余的医院用户（排除订单生成的医院用户）
    if order_hospital_patient_id_set:
        redundancy_hospital_user_list = [p for p in hospital_user_list if
                                         p['id'] not in order_hospital_patient_id_set
                                         and p['referer'] is not None]
    else:
        redundancy_hospital_user_list = [p for p in hospital_user_list if
                                         p['referer'] is not None]

    redundancy_hospital_user_list = random.sample(redundancy_hospital_user_list, left_hospital_num)

    # 当月需要冗余大非医院用户
    if order_common_patient_id_set:
        redundancy_common_user_list = [p for p in common_user_list if p['id'] not in order_common_patient_id_set
                                       and p['referer'] is None]
    else:
        redundancy_common_user_list = [p for p in common_user_list if
                                       p['referer'] is None]

    redundancy_common_user_list = random.sample(redundancy_common_user_list, left_common_num)

    # 最终患者池
    patient_pool_list = redundancy_hospital_user_list + redundancy_common_user_list

    # 随机打散患者
    random.shuffle(patient_pool_list)

    return redundancy_prescription_num, patient_pool_list


# 读取Excel，按月纬度生成处方
def generate_prescription_from_excel(ym_range):
    for row in xls_reader(INPUT_DIR + 'prescription/处方数据7_11.xlsx', True, 0):
        # 读取Excel年月

        yearmonth_datetime = cell_to_datetime(row[0])

        ym = get_ym(yearmonth_datetime)
        # check
        if not (ym_range[0] <= ym <= ym_range[1]):
            # logging.info('skip ym {ym} not in ym_range {ym_range}')
            continue

        # print("readexcel is ready ...")

        # 当月活跃处方医生数量
        prescription_doctor_num = int(row[1])
        # 当月医院开方用户数
        patient_hospital_num = int(row[3])
        # 当月非医院开方用户数量
        patient_common_num = int(row[4])
        # 当月总计开方数量
        prescription_num = int(row[5])
        # if month_redundancy_dict:
        #     gen_history_prescription_by_month(yearmonth_datetime, prescription_doctor_num, patient_hospital_num,
        #                                       patient_common_num,
        #                                       prescription_num-month_redundancy_dict[ym])
        # # 当月历史处方数据
        # else:
        logging.info("时间:" + str(ym) + "当月活跃处方医生数量" + str(prescription_doctor_num) + "当月医院开方用户数" + str(
            patient_hospital_num) + "当月非医院开方用户数量" + str(patient_common_num) + "当月总计开方数量" + str(prescription_num))
        gen_history_prescription_by_month(yearmonth_datetime, prescription_doctor_num, patient_hospital_num,
                                          patient_common_num,
                                          prescription_num)


def get_user_dict(user_list):
    user_dict = {u['id']: u for u in user_list}
    return user_dict


def get_redundancy_prescription_list(prescription_dict_list, patient_dict, doctor_dict, ym):
    prescription_list = []
    for value in prescription_dict_list:
        prescription_dict = get_patient_doctor_dict(patient_dict, doctor_dict, value['patient_id'],
                                                    value['doctor_id'],
                                                    value['gmt_create'], ym)
        prescription_list.append(prescription_dict)
    return prescription_list


# 过滤掉月末注册患者/医生
def filter_user(user_list, yearmonth_datetime):
    list = []
    for u in user_list:
        register_time = u['gmt_create']
        month_days = calendar.monthrange(yearmonth_datetime.year, yearmonth_datetime.month)[1]
        if register_time is None:
            continue

        if register_time.year == yearmonth_datetime.year and register_time.month == yearmonth_datetime.month and register_time.day == month_days:
            continue
        else:
            list.append(u)
    return list


# 获取某月活跃用户信息
def get_active_user_data(ym, user_type):
    active_user_list = []
    active_uid_set = get_active_user(user_type)[str(ym)]
    if active_uid_set:
        active_user_list = get_user_list_by_ids(active_uid_set)
        return active_user_list
    return active_user_list


# 获取某个月，每天注册用户列表，返回dict
def get_month_day_user_register(user_list):
    day_user_dict = {}
    for u in user_list:
        register_time = u['gmt_create']
        register_time_date = register_time.date()  # datetime.date(2020, 9, 27)
        if register_time_date not in day_user_dict:
            day_user_dict[register_time_date] = []

        day_user_dict[register_time_date].append(u)

    return day_user_dict


# 将用户按日期分成2组,1组注册日期为当前月,一组注册日期为非当前月
def get_user_list_group_by_month(user_list, month_start_day):
    history_month_user_list = []
    current_month_user_list = []
    for d in user_list:
        if d['gmt_create'].date() < month_start_day:
            history_month_user_list.append(d)
        else:
            current_month_user_list.append(d)

    return history_month_user_list, current_month_user_list


# 根据医生池和患者池构造配对
def get_patient_doctor_list(patient_pool_list, doctor_pool_list, start_day, patient_doctor_id_dict,
                            doctor_dict, year_hour_probabilities):
    patient_doctor_dict_list = []
    # 遍历患者找医生，优先找具备绑定关系的医生
    doctor_pool_set = set(d['id'] for d in doctor_pool_list)
    for patient in patient_pool_list:
        patient_doctor_dict = {}
        # 先从绑定关系中取
        patient_id = patient['id']
        bind_doctor_id_set = patient_doctor_id_dict.get(patient_id, None)
        if bind_doctor_id_set:
            bind_doctor_id_list = list(bind_doctor_id_set)
            doctor_id = random.choice(bind_doctor_id_list)
            if doctor_id in doctor_pool_set:
                doctor = doctor_dict.get(doctor_id)
                if doctor is None:
                    doctor = random.choice(doctor_pool_list)
            else:
                doctor = random.choice(doctor_pool_list)
        else:
            doctor = random.choice(doctor_pool_list)

        # 根据概率曲线生成时间
        patient_register_time = patient['gmt_create']
        gmt_create = year_hour_probabilities.get_dt(start_day)

        if patient_register_time >= gmt_create:
            gmt_create = patient_register_time + datetime.timedelta(days=1)

        doctor_id = doctor['id']
        patient_doctor_dict['patient_id'] = patient_id
        patient_doctor_dict['doctor_id'] = doctor_id
        patient_doctor_dict['gmt_create'] = gmt_create
        patient_doctor_dict_list.append(patient_doctor_dict)

    return patient_doctor_dict_list


# 按月从处方订单中直接生成处方
def gen_order_prescription_by_month(start_day, end_day, history_month_doctor_list, day_user_dict,
                                    all_active_doctor_dick):
    hospital_patient_id_set = set()
    common_patient_id_set = set()
    order_prescription_num = 0

    first_day = start_day
    day_doctor_pool_list = history_month_doctor_list
    # datetime.datetime(2020, 10, 1, 0, 0)
    month_start_day_time = datetime.datetime.combine(start_day, datetime.datetime.min.time())
    month_last_day_time = datetime.datetime.combine(end_day, datetime.datetime.max.time())
    # start_day = datetime.datetime.strptime('2020-07-30', '%Y-%m-%d').date()
    # year, month, day = start_day[:3]
    # start_day = datetime.date(year, month, day)
    print(start_day)
    while start_day <= end_day:
        # 通过sql获取当日处方订单
        prescription_orderList = get_prescription_order7(start_day)
        if prescription_orderList:
            patient_id_list = [p['patient_id'] for p in prescription_orderList]
            patient_ids = ','.join([str(patient_id) for patient_id in patient_id_list])
            patient_doctor_id_dict = get_patient_doctor_relation(patient_ids)
        # 获取患者信息
            patient_list = get_user_list_by_ids(patient_id_list)
            patient_dict = get_user_dict(patient_list)
        if prescription_orderList:
            # 每天将当天注册医生放入医生池
            before_day = start_day - datetime.timedelta(days=1)
            if before_day >= first_day:
                if day_user_dict.get(before_day):
                    day_doctor_pool_list = day_doctor_pool_list + day_user_dict[before_day]

            # 为避免所有处方医生都活跃，每天取70-80%
            doctor_list = random.sample(day_doctor_pool_list,
                                        int(len(day_doctor_pool_list) * (random.uniform(70, 80) / 100)))
            # 取当天活跃的连续活跃医生
            active_doctor_list = all_active_doctor_dick[start_day]

            doctor_list += active_doctor_list
            doctor_dict = get_user_dict(doctor_list)

            day_prescription_list = []
            for pd in prescription_orderList:
                patient_id = pd['patient_id']
                order_no = pd['order_id']
                order_time = pd['order_time']
                sent_time =pd['sent_time']
                pay_time=pd['pay_time']
                order_prescription_num = order_prescription_num + 1
                if pd['referer'] is not None:
                    hospital_patient_id_set.add(patient_id)
                elif pd['referer'] is None:
                    common_patient_id_set.add(patient_id)
                if pd['order_type']  == 6:
                    gmt_create = get_gmt_create_before_order_time(order_time)
                    gmt_create = gmt_create - datetime.timedelta(seconds=random.randint(1, 60))
                    # 处方创建时间=订单时间-随机分钟数，若小于月初时间，则选择月初时间+随机分钟数
                    if gmt_create <= month_start_day_time:
                        gmt_create = month_start_day_time + datetime.timedelta(seconds=random.randint(1, 5))

                    # patient_register_time = pd['patient_register_time']
                    # 患者注册时间大于处方创建时间，则从下一天随机取个值
                    # if patient_register_time.date() >= gmt_create.date():
                    #     start_time = patient_register_time + datetime.timedelta(minutes=random.randint(5, 10))
                    #     next_day_time = patient_register_time + datetime.timedelta(days=1)
                    #     gmt_create = random_start_end_date(start_time, next_day_time)
                    #
                    #     if gmt_create >= month_last_day_time:
                    #         gmt_create = patient_register_time + datetime.timedelta(minutes=random.randint(1, 5))
                    #
                    #     if gmt_create >= month_last_day_time:
                    #         gmt_create = month_last_day_time
                    #
                    #     if gmt_create <= month_start_day_time:
                    #         gmt_create = month_start_day_time

                    if gmt_create > order_time:
                        gmt_create = order_time - datetime.timedelta(seconds=random.randint(20, 30))
                elif pd['order_type']  == 7:
                    #处方的时间在支付时间上加10分钟+加一个曲线
                    gmt_create=pay_time+ datetime.timedelta(minutes=random.randint(10, 20))+datetime.timedelta(seconds=random.randint(20, 30))
                    #如果处方创建时间大于发货时间
                    # if datetime.datetime.strptime(gmt_create, '%Y-%m-%d %H:%M:%S')>=datetime.datetime.strptime(sent_time, '%Y-%m-%d %H:%M:%S'):
                        #处方创建时间等于发货时间减去5分钟
                        # gmt_create=sent_time-datetime.timedelta(minutes=5)
                        #如果处方创建时间小于支付时间
                        # if datetime.datetime.strptime(gmt_create, '%Y-%m-%d %H:%M:%S')<=datetime.datetime.strptime(pay_time, '%Y-%m-%d %H:%M:%S'):
                        #     gmt_create=pay_time+datetime.timedelta(minutes=random.randint(1, 5))
                    if sent_time and gmt_create>sent_time:
                        gmt_create=sent_time-datetime.timedelta(minutes=random.randint(1, 2))
                    if gmt_create>month_last_day_time:
                        gmt_create = pay_time + datetime.timedelta(minutes=random.randint(1, 3))
                patient = patient_dict[patient_id]
                # 根据医生患者绑定关系获取医生信息
                doctor = get_doctor_by_patient(patient_id, doctor_list, patient_doctor_id_dict, doctor_dict)

                # 构造处方订单
                prescription_dict = build_order_prescription_data(patient, doctor, order_no, order_time, gmt_create)

                day_prescription_list.append(prescription_dict)

            if day_prescription_list:
                logging.info(
                    'date:{start_day}.order_prescription_num:{order_prescription_num},hospital_patient:{len(hospital_patient_id_set)},common_patient_num:{len(common_patient_id_set)}')

                iterate_elements_page(day_prescription_list, write_pres_sql, DEFAULT_PAGE_SIZE, ym_date=start_day)

        start_day = start_day + datetime.timedelta(days=1)

    return hospital_patient_id_set, common_patient_id_set, order_prescription_num


# 获取每日订单处方
def get_day_order_prescription(order_list, month_start_day_time, month_last_day_time,
                               order_prescription_num,
                               hospital_patient_id_set, common_patient_id_set):
    day_prescription_list = []
    if order_list:
        for pd in order_list:
            patient_id = pd['patient_id']

            order_prescription_num = order_prescription_num + 1
            if pd['referer'] is not None and (pd['patient_tag'] == '' or pd['patient_tag'] == 'NPC'):
                hospital_patient_id_set.add(patient_id)
            if pd['referer'] is None and (pd['patient_tag'] == '' or pd['patient_tag'] == 'NPC'):
                common_patient_id_set.add(patient_id)

            order_time = pd['order_time']
            gmt_create = get_gmt_create_before_order_time(order_time)

            if gmt_create <= month_start_day_time:
                gmt_create = month_start_day_time + datetime.timedelta(seconds=random.randint(1, 5))

            patient_register_time = pd['patient_register_time']
            if patient_register_time.date() >= gmt_create.date():
                # 从下一天随机取个值
                start_time = patient_register_time + datetime.timedelta(minutes=random.randint(5, 10))
                next_day_time = patient_register_time + datetime.timedelta(days=1)
                gmt_create = random_start_end_date(start_time, next_day_time)

                if gmt_create >= month_last_day_time:
                    gmt_create = patient_register_time + datetime.timedelta(minutes=random.randint(1, 5))

                if gmt_create >= month_last_day_time:
                    gmt_create = month_last_day_time

                if gmt_create <= month_start_day_time:
                    gmt_create = month_start_day_time

            if gmt_create > order_time:
                gmt_create = order_time - datetime.timedelta(seconds=random.randint(1, 5))

            pd['gmt_create'] = gmt_create

            day_prescription_list.append(pd)

        return day_prescription_list, hospital_patient_id_set, common_patient_id_set, order_prescription_num


def gen_redundancy_prescription_by_month_v2(start_day, end_day, month_days, history_month_user_list,
                                            day_user_dict,
                                            patient_pool_list,
                                            doctor_dict,
                                            redundancy_prescription_num, yearmonth_datetime, all_active_doctor_dick):
    patient_doctor_dict_list = []
    # 获取医患绑定关系
    patient_doctor_id_dict = get_patient_doctor_relation(','.join([str(p['id']) for p in patient_pool_list]))

    # 随机的患者池
    first_prescription_num = len(patient_pool_list)
    first_prescription_list = random_avg_split(first_prescription_num, month_days, 0.8)

    first_day = start_day
    index = 0
    # 历史医生的注册时间
    # TODO 出现了最后一天没有放进去
    day_doctor_pool_list = history_month_user_list
    day_patient_id_dict = {}
    # todo
    generator = RandomDatetimeGenerator(yearmonth_datetime.year, hour_minute_probability)
    while start_day <= end_day:
        # 每天将当天注册医生放入医生池
        before_day = start_day - datetime.timedelta(days=1)
        if before_day >= first_day:
            if day_user_dict.get(before_day):
                day_doctor_pool_list = day_doctor_pool_list + day_user_dict[before_day]

        doctor_list = random.sample(day_doctor_pool_list,
                                    int(len(day_doctor_pool_list) * (random.uniform(70, 80) / 100)))

        day_prescription_num = first_prescription_list[(start_day - first_day).days]
        day_time = datetime.datetime.combine(start_day, datetime.time.min)
        patient_list = patient_pool_list[index:index + day_prescription_num]

        # 随机打散医生患者
        random.shuffle(patient_list)
        # 取当天活跃的连续活跃医生
        active_doctor_list = all_active_doctor_dick[start_day]
        doctor_list += active_doctor_list
        random.shuffle(doctor_list)

        for patient in tqdm(patient_list):
            # print(len(patient_list))
            patient_doctor_dict = {}
            # 先从绑定关系中取
            patient_id = patient['id']
            doctor = get_doctor_by_patient(patient_id, doctor_list, patient_doctor_id_dict, doctor_dict)

            patient_register_time = patient['gmt_create']
            # 根据概率曲线生成时间
            # year_hour_probabilities = get_year_hour_probabilities_by_user_type(patient, day_time.year)
            # gmt_create = year_hour_probabilities.get_dt(start_day) # 转到下一行赋值

            # todo
            # print("HD line time1 ...")
            gmt_create = generator.get_datetime(datetime.datetime.combine(start_day, datetime.datetime.min.time()))
            # print("already get time1")
            # print("patient_register_time is", patient_register_time)
            # print("gmt_create is", gmt_create)

            # if patient_register_time >=datetime.datetime.combine(start_day, datetime.datetime.min.time()) and patient_register_time<=datetime.datetime.combine(end_day, datetime.datetime.min.time()):

            if patient_register_time.strftime('%Y-%m-%d') >= first_day.strftime(
                    '%Y-%m-%d') and patient_register_time.strftime('%Y-%m-%d') <= end_day.strftime('%Y-%m-%d'):
                gmt_create = patient_register_time + datetime.timedelta(days=random.randint(2, 8))
                gmt_create = generator.get_datetime(gmt_create)
            # else:
            # print("not current patient")
            # if patient_register_time >= gmt_create:
            #     print("patient_register_time >= gmt_create")
            #     # 从下一天随机取个值
            #     start_time = patient_register_time + datetime.timedelta(minutes=random.randint(5, 10))
            #     next_day_time = patient_register_time + datetime.timedelta(days=1)
            #     gmt_create = random_start_end_date(start_time, next_day_time)
            #     # TODO
            # else:
            #     print("patient_register_time < gmt_create")

            if start_day not in day_patient_id_dict:
                patient_id_set = set()
                patient_id_set.add(patient_id)
                day_patient_id_dict[start_day] = patient_id_set
            else:
                day_patient_id_dict[start_day].add(patient_id)

            doctor_id = doctor['id']
            patient_doctor_dict['patient_id'] = patient_id
            patient_doctor_dict['doctor_id'] = doctor_id
            patient_doctor_dict['gmt_create'] = gmt_create
            if gmt_create.strftime('%Y-%m-%d') > end_day.strftime('%Y-%m-%d'):
                patient_doctor_dict['redundancy'] = 112
            else:
                patient_doctor_dict['redundancy'] = 113
            patient_doctor_dict_list.append(patient_doctor_dict)

        index = index + day_prescription_num
        start_day = start_day + datetime.timedelta(days=1)

    second_prescription_num = 0
    second_patient_doctor_dict_list = []
    if redundancy_prescription_num > first_prescription_num:
        second_prescription_num = redundancy_prescription_num - first_prescription_num

    if second_prescription_num > 0:
        start_day = first_day
        second_patient_doctor_dict_list = get_patient_doctor_dict_list(patient_pool_list, doctor_dict,
                                                                       second_prescription_num,
                                                                       start_day, end_day, month_days,
                                                                       history_month_user_list,
                                                                       day_user_dict, patient_doctor_id_dict,
                                                                       day_patient_id_dict, yearmonth_datetime,
                                                                       all_active_doctor_dick)
    if second_patient_doctor_dict_list:
        patient_doctor_dict_list = patient_doctor_dict_list + second_patient_doctor_dict_list

    # print("ok return patient_doctor_dict_list")

    return patient_doctor_dict_list


# 根据患者类型获取小时曲线
def get_year_hour_probabilities_by_user_type(patient, year):
    if patient['referer'] is not None and (patient['tag'] == '' or patient['tag'] == 'NPC'):
        return HOSPITAL_DHDR_dict[year]

    if patient['referer'] is None and (patient['tag'] == '' or patient['tag'] == 'NPC'):
        return COMMON_DHDR_dict[year]

    return COMMON_DHDR_dict[year]


def get_patient_doctor_dict_list(patient_list, doctor_dict, prescription_num, start_day, end_day, month_days,
                                 history_month_user_list, day_user_dict, patient_doctor_id_dict, day_patient_id_dict,
                                 yearmonth_datetime, all_active_doctor_dick):
    patient_doctor_dict_list = []
    day_doctor_pool_list = history_month_user_list
    day_prescription_list = random_avg_split(prescription_num, month_days, 0.8)
    first_day = start_day

    generator = RandomDatetimeGenerator(yearmonth_datetime.year, hour_minute_probability)
    while start_day <= end_day:
        # 每天将当天注册医生放入医生池
        before_day = start_day - datetime.timedelta(days=1)
        if before_day >= first_day:
            if day_user_dict.get(before_day):
                day_doctor_pool_list = day_doctor_pool_list + day_user_dict[before_day]

        doctor_list = random.sample(day_doctor_pool_list,
                                    int(len(day_doctor_pool_list) * (random.uniform(70, 80) / 100)))
        # 取当天活跃的连续活跃医生
        active_doctor_list = all_active_doctor_dick[start_day]

        doctor_list += active_doctor_list

        # 每日处方量
        day_prescription_num = day_prescription_list[(start_day - first_day).days]
        day_time = datetime.datetime.combine(start_day, datetime.time.min)

        # 每次随机取一个患者,若同一天出现同一患者，再次随机
        count = 1
        # 循环1000次，仍无法找到满足条件的患者，则随机取
        loop = 1

        while count <= day_prescription_num:
            # print(count,day_prescription_num)
            patient = random.choice(patient_list)
            patient_id = patient['id']

            if loop < 10000:
                day_patient_id_set = day_patient_id_dict.get(start_day)
                if day_patient_id_set:
                    if patient_id in day_patient_id_set:
                        logging.warning(
                            'patient_id over limit:,patient_id{patient_id},start_day:{start_day}')
                        loop = loop + 1
                        continue
                    else:
                        day_patient_id_dict[start_day].add(patient_id)
                else:
                    day_patient_id_set = set()
                    day_patient_id_set.add(patient_id)
                    day_patient_id_dict[start_day] = day_patient_id_set
            else:
                loop = 1

            doctor = get_doctor_by_patient(patient_id, doctor_list, patient_doctor_id_dict, doctor_dict)
            count = count + 1

            patient_doctor_dict = {}
            patient_register_time = patient['gmt_create']

            # 根据概率曲线生成时间
            # year_hour_probabilities = get_year_hour_probabilities_by_user_type(patient, day_time.year)

            # todo
            # gmt_create = year_hour_probabilities.get_dt(start_day)
            # print("HD line time2 ...")
            gmt_create = generator.get_datetime(datetime.datetime.combine(start_day, datetime.datetime.min.time()))

            # print("already get time2")
            # if patient_register_time >= gmt_create:
            #     # 从下一天随机取个值
            #     start_time = patient_register_time + datetime.timedelta(minutes=random.randint(5, 10))
            #     next_day_time = patient_register_time + datetime.timedelta(days=1)
            #     gmt_create = random_start_end_date(start_time, next_day_time)
            if patient_register_time.strftime('%Y-%m-%d') >= first_day.strftime(
                    '%Y-%m-%d') and patient_register_time.strftime('%Y-%m-%d') <= end_day.strftime('%Y-%m-%d'):
                gmt_create = patient_register_time + datetime.timedelta(days=random.randint(2, 8))
                gmt_create = generator.get_datetime(gmt_create)
            # else:
            # print("not current patient")

            doctor_id = doctor['id']
            patient_doctor_dict['patient_id'] = patient_id
            patient_doctor_dict['doctor_id'] = doctor_id
            patient_doctor_dict['gmt_create'] = gmt_create
            if gmt_create.strftime('%Y-%m-%d') > end_day.strftime('%Y-%m-%d'):
                patient_doctor_dict['redundancy'] = 112
            else:
                patient_doctor_dict['redundancy'] = 113
            patient_doctor_dict_list.append(patient_doctor_dict)

        start_day = start_day + datetime.timedelta(days=1)
        # print("ok return patient_doctor_dict_list")

    return patient_doctor_dict_list


# 根据患者从医生池中取医生
def get_doctor_by_patient(patient_id, doctor_list, patient_doctor_id_dict, doctor_dict):
    doctor_id_set = set(d['id'] for d in doctor_list)
    # 先从绑定关系中取
    bind_doctor_id_set = patient_doctor_id_dict.get(patient_id, None)
    if bind_doctor_id_set:
        bind_doctor_id_list = list(bind_doctor_id_set)
        doctor_id = random.choice(bind_doctor_id_list)
        if doctor_id in doctor_id_set:
            doctor = doctor_dict.get(doctor_id)
            if doctor is None:
                doctor = random.choice(doctor_list)
        else:
            doctor = random.choice(doctor_list)
    else:
        doctor = random.choice(doctor_list)
    return doctor


def get_redundancy_patient_list(patient_list, prescription_num):
    pt_list = []
    num = 0
    day_patient_id_set = set()
    day_patient_id_num = {}
    while num < prescription_num:
        patient = random.choice(patient_list)
        if patient['id'] not in day_patient_id_set:
            pt_list.append(patient)
            num = num + 1
            day_patient_id_set.add(patient['id'])
            day_patient_id_num[patient['id']] = 1
        else:
            if day_patient_id_num.get(patient['id']) < 3:
                pt_list.append(patient)
                num = num + 1
                day_patient_id_num[patient['id']] = day_patient_id_num[patient['id']] + 1

    return pt_list


# 根据权重和订单时间获取处方生成时间
def get_gmt_create_before_order_time(order_time):
    # time_list = [[0, 0], [0, 2], [2, 8], [8, 13], [10, 60], [60, 120]]
    # time_list = [[30, 90], [60, 150], [120, 510], [480, 810], [600, 3660], [3600, 7500],[5000,86400]]
    time_list = [i for i in range(24 * 60)]
    # time_weight = [9, 5, 41, 38, 4, 3]
    # time_weight = [4, 4, 9, 41, 38,3,1]
    # time_weight = [7,9,12,17,24,31,39,48,57,67,76,84,93,100,108,115,121,127,132,137,141,145,149,152,156,158,161,163,165,167,169,170,171,173,173,174,175,175,176,176,176,176,176,176,175,175,175,174,173,172,171,169,168,166,165,163,161,159,156,154,151,149,146,143,140,137,133,130,126,123,119,115,111,108,104,100,96,92,88,85,81,77,73,70,66,63,59,56,53,50,47,44,41,39,36,34,31,29,27,25,23,21,20,18,17,15,14,13,12,11,10,9,9,8,7,7,7,6,2,3,1,2,1,2,1,2,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    time_weight = [70, 90, 120, 170, 240, 310, 390, 480, 570, 670, 760, 840, 930, 1000, 1080, 1150, 1210, 1270, 1320,
                   1370, 1410, 1450, 1490, 1520, 1560, 1580, 1610, 1630, 1650, 1670, 1690, 1700, 1710, 1730, 1730, 1740,
                   1750, 1750, 1760, 1760, 1760, 1760, 1760, 1760, 1750, 1750, 1750, 1740, 1730, 1720, 1710, 1690, 1680,
                   1660, 1650, 1630, 1610, 1590, 1560, 1540, 1510, 1490, 1460, 1430, 1400, 1370, 1330, 1300, 1260, 1230,
                   1190, 1150, 1110, 1080, 1040, 1000, 960, 920, 880, 850, 810, 770, 730, 700, 660, 630, 590, 560, 530,
                   500, 470, 440, 410, 390, 360, 340, 310, 290, 270, 250, 230, 210, 200, 180, 170, 150, 140, 130, 120,
                   110, 100, 90, 90, 80, 70, 70, 70, 59, 59, 58, 58, 57, 57, 55, 53, 54, 52, 51, 50, 49, 48, 47, 46, 45,
                   44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20,
                   19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0,
                   1, 1, 2, 0, 1, 1, 2, 1, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1,
                   1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 1, 0, 0, 1, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 0,
                   1, 1, 2, 0, 1, 0, 1, 1, 2, 0, 1, 1, 0, 1, 1, 2, 0, 1, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 0, 1, 1, 2, 1,
                   0, 1, 1, 2, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 0, 1,
                   1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1,
                   2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2,
                   1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 0, 1, 1, 2,
                   0, 1, 1, 2, 0, 1, 1, 2, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1,
                   0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0,
                   0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1,
                   2, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0,
                   0, 1, 1, 2, 1, 0, 0, 1, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0,
                   1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2,
                   1, 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 0, 1, 1, 2, 0,
                   1, 1, 2, 0, 1, 1, 2, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0,
                   0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0,
                   1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2,
                   1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1,
                   2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1,
                   0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0,
                   1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2,
                   1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1,
                   2, 1, 0, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1,
                   1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 1, 2, 1, 0, 0, 1, 0,
                   1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 0, 1, 1, 2,
                   1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1,
                   2, 1, 0, 0, 1, 1, 2, 1, 1, 0, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 1, 0, 1, 1, 2, 1, 0, 0,
                   1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1,
                   1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2,
                   1, 0, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 0, 0, 1,
                   1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 0, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 1, 0, 1, 1, 2,
                   1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0,
                   0, 1, 0, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 0, 1, 1, 2, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1,
                   1, 2, 1, 0, 0, 1, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 1, 2, 1, 0, 0, 1, 0,
                   1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 0, 1, 1, 2,
                   1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1, 2, 0, 0, 1, 1, 2, 1, 0, 0, 1, 1,
                   2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 2, 1, 0, 0, 1, 1, 2, 1, 1, 1, 2, 1, 0, 0, 1, 0, 1]
    start = get_element_by_random(time_list, time_weight)
    return order_time - datetime.timedelta(minutes=start)


# def get_gmt_create_before_order_time(order_time):
#
#     # time_list = [[0, 0], [0, 2], [2, 8], [8, 13], [10, 60], [60, 120]]
#     # time_list = [[30, 90], [60, 150], [120, 510], [480, 810], [600, 3660], [3600, 7500],[5000,86400]]
#     time_list = [i for i in range(24 * 60)]
#     # time_weight = [9, 5, 41, 38, 4, 3]
#     # time_weight = [4, 4, 9, 41, 38,3,1]
#     time_weight = [18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 24, 24, 24, 24, 24, 24, 24, 24, 24, 24, 25, 25, 25, 25, 25, 25, 25, 26, 26, 26, 26, 26, 26, 26, 27, 27, 27, 27, 27, 28, 28, 28, 28, 28, 28, 29, 29, 29, 29, 29, 30, 30, 30, 30, 30, 31, 31, 31, 31, 31, 32, 32, 32, 32, 32, 33, 33, 33, 33, 33, 34, 34, 34, 34, 34, 35, 35, 35, 35, 35, 36, 36, 36, 36, 36, 37, 37, 37, 37, 38, 38, 38, 38, 38, 39, 39, 39, 39, 40, 40, 40, 41, 41, 41, 41, 42, 42, 42, 43, 43, 43, 44, 44, 44, 45, 45, 46, 46, 47, 47, 47, 48, 48, 49, 49, 50, 50, 51, 51, 52, 52, 53, 54, 54, 55, 55, 56, 56, 57, 58, 58, 59, 59, 60, 61, 61, 62, 63, 63, 64, 64, 65, 66, 66, 67, 68, 68, 69, 69, 70, 71, 71, 72, 72, 73, 74, 74, 75, 75, 76, 76, 77, 77, 78, 79, 79, 79, 80, 80, 81, 81, 82, 82, 83, 83, 83, 84, 84, 84, 85, 85, 86, 86, 86, 87, 87, 87, 88, 88, 88, 88, 89, 89, 89, 90, 90, 90, 90, 91, 91, 91, 91, 92, 92, 92, 92, 92, 93, 93, 93, 93, 94, 94, 94, 94, 95, 95, 95, 95, 95, 96, 96, 96, 96, 96, 97, 97, 97, 97, 97, 98, 98, 98, 98, 98, 99, 99, 99, 99, 99, 99, 100, 100, 100, 100, 100, 100, 101, 101, 101, 101, 101, 101, 101, 102, 102, 102, 102, 102, 102, 102, 102, 103, 103, 103, 103, 103, 103, 103, 103, 103, 104, 104, 104, 104, 104, 104, 104, 104, 104, 105, 105, 105, 105, 105, 105, 105, 105, 105, 106, 106, 106, 106, 106, 106, 106, 106, 106, 107, 107, 107, 107, 107, 107, 107, 107, 108, 108, 108, 108, 108, 108, 108, 108, 108, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 111, 111, 111, 111, 111, 111, 110, 110, 110, 110, 110, 110, 109, 109, 109, 109, 108, 108, 108, 108, 108, 107, 107, 107, 107, 107, 106, 106, 106, 106, 106, 106, 106, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 105, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 113, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 112, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 106, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 107, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 108, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 109, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 110, 111, 111, 111, 111, 111, 111, 111, 111, 111, 111, 112, 112, 112, 112, 112, 112, 112, 112, 113, 113, 113, 113, 113, 113, 113, 114, 114, 114, 114, 114, 114, 115, 115, 115, 115, 115, 116, 116, 116, 116, 116, 117, 117, 117, 117, 117, 118, 118, 118, 118, 118, 119, 119, 119, 119, 119, 120, 120, 120, 120, 120, 121, 121, 121, 121, 121, 121, 121, 122, 122, 122, 122, 122, 122, 122, 122, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 123, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 124, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 127, 126, 126, 126, 126, 126, 126, 126, 126, 126, 126, 125, 125, 125, 125, 125, 125, 125, 124, 124, 124, 124, 124, 124, 124, 124, 123, 123, 123, 123, 123, 123, 123, 122, 122, 122, 122, 122, 122, 122, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 121, 120, 120, 120, 120, 120, 120, 120, 119, 119, 119, 119, 119, 118, 118, 118, 118, 117, 117, 117, 116, 116, 116, 115, 115, 115, 114, 114, 113, 113, 112, 112, 112, 111, 110, 110, 109, 109, 108, 108, 107, 106, 106, 105, 104, 104, 103, 102, 101, 100, 99, 97, 96, 95, 93, 91, 90, 88, 86, 84, 83, 81, 79, 77, 75, 73, 71, 69, 67, 65, 63, 61, 59, 58, 56, 54, 52, 50, 48, 46, 45, 43, 41, 39, 38, 36, 34, 33, 32, 30, 29, 28, 26, 25, 24, 23, 22, 21, 20, 20, 19, 19, 18, 18, 18]
#
#     start, end = get_element_by_random(time_list, time_weight)
#     if start == end:
#         return order_time
#     return order_time - datetime.timedelta(seconds=random.randint(start, end))

# 根据医生与患者构造处方信息
def get_patient_doctor_dict(patient_info_dict, doctor_info_dict, patient_id, doctor_id, gmt_create_time, ym):
    patient = patient_info_dict[patient_id]
    doctor = doctor_info_dict[doctor_id]
    prescription_dict = {}
    prescription_dict['type'] = 1
    prescription_dict['user_base_info_id'] = 0  # 老系统 0
    prescription_dict['patient_id'] = patient['id']
    # prescription_dict['name'] = add_quote(patient['name'])
    prescription_dict['name'] = add_quote(patient['name'])
    prescription_dict['age'] = 45
    if patient['birthday'] is not None:
        prescription_dict['age'] = datetime.datetime.now().year - patient['birthday'].year
    # prescription_dict['gender'] = patient.get('sex', 1)
    prescription_dict['gender'] = 1
    prescription_dict['symptom'] = MYSQL_NULL
    # 临床诊断
    prescription_dict['illness'] = quote_or_MYSQL_NULL(patient['disease_name'])

    prescription_dict['region'] = add_quote((patient.get('province', '') or '') + (patient.get('city', '') or ''))

    age = 45
    if patient['birthday'] is not None:
        age = datetime.datetime.now().year - patient['birthday'].year
    height, weight = get_height_weitht_by_age(age, patient.get('sex', 1))
    # 用户基础信息表
    prescription_dict['height'] = add_quote(str(height))
    prescription_dict['weight'] = add_quote(str(weight))
    prescription_dict['phone_number'] = quote_or_MYSQL_NULL(patient['mobile'])
    prescription_dict['remark'] = MYSQL_NULL

    prescription_dict['self_image_url'] = MYSQL_NULL
    prescription_dict['supply_image_url'] = MYSQL_NULL
    prescription_dict['prescription_remark'] = MYSQL_NULL

    prescription_dict['audit_type'] = 1
    prescription_dict['status'] = 2

    prescription_dict['patient_advisory_id'] = MYSQL_NULL
    prescription_dict['replace_prescription_id'] = MYSQL_NULL

    prescription_dict['doctor_id'] = doctor['id']
    prescription_dict['doctor_name'] = quote_or_MYSQL_NULL(doctor['name'])
    prescription_dict['doctor_title'] = quote_or_MYSQL_NULL(doctor['title'])
    prescription_dict['doctor_hospital_name'] = MYSQL_NULL
    prescription_dict['doctor_dept_name'] = MYSQL_NULL
    prescription_dict['dept'] = quote_or_MYSQL_NULL(doctor['dept'])

    # 订单审核人
    prescription_dict['auditor_id'] = -1
    prescription_dict['auditor_name'] = MYSQL_NULL
    # 医嘱下达
    # order_time = order_time
    gmt_create = gmt_create_time

    prescription_dict['order_time'] = MYSQL_NULL
    prescription_dict['t_order_id'] = MYSQL_NULL
    if gmt_create.strftime('%Y-%m') > ym.strftime('%Y-%m'):
        prescription_dict['redundancy'] = 112
    else:
        prescription_dict['redundancy'] = 113
    # prescription_dict['redundancy'] = 2

    prescription_dict['gmt_create'] = add_quote(gmt_create.strftime(all_format_str))

    # 线上是gmt_create + 1天
    prescription_dict['expired_time'] = add_quote(
        (gmt_create + datetime.timedelta(days=1)).strftime(all_format_str))

    prescription_audit_time = gmt_create + datetime.timedelta(seconds=10 * random.random())
    prescription_reaudit_time = prescription_audit_time + datetime.timedelta(seconds=10 * random.random())

    # 处方审核时间
    prescription_dict['prescription_audit_time'] = add_quote(prescription_audit_time.strftime(all_format_str))
    # 处方复审时间
    prescription_dict['prescription_reaudit_time'] = add_quote(
        prescription_reaudit_time.strftime(all_format_str))

    audit_time = prescription_reaudit_time + datetime.timedelta(seconds=2000 * random.random())
    gmt_modify = audit_time + datetime.timedelta(seconds=300 * random.random())

    # 线上空
    prescription_dict['audit_time'] = add_quote(gmt_modify.strftime(all_format_str))
    prescription_dict['gmt_modify'] = add_quote(gmt_modify.strftime(all_format_str))
    prescription_dict['mall_order_time'] = MYSQL_NULL

    PRESCRIPTION_AUDITOR = [
        {'id': 10000072, 'name': '马静', 'sign_url': '/userBaseInfo/5e7b8bc4-c611-4cdc-8ca5-4a519219d5b7.png'},
        {'id': 10000077, 'name': '李洪洋', 'sign_url': '/userBaseInfo/32011cef-119b-4179-965b-8d174bced71b.png'}]

    # 打乱
    random.shuffle(PRESCRIPTION_AUDITOR)

    prescription_dict['prescription_auditor_id'] = PRESCRIPTION_AUDITOR[0]['id']
    prescription_dict['prescription_auditor_name'] = add_quote(PRESCRIPTION_AUDITOR[0]['name'])
    prescription_dict['prescription_auditor_sign_url'] = add_quote(PRESCRIPTION_AUDITOR[0]['sign_url'])
    prescription_dict['prescription_reauditor_id'] = PRESCRIPTION_AUDITOR[1]['id']
    prescription_dict['prescription_reauditor_name'] = add_quote(PRESCRIPTION_AUDITOR[1]['name'])
    prescription_dict['prescription_reauditor_sign_url'] = add_quote(PRESCRIPTION_AUDITOR[1]['sign_url'])
    prescription_dict['prescription_audit_status'] = 2
    # 医生签名
    prescription_dict['doctor_sign_url'] = MYSQL_NULL
    return prescription_dict


# 获取处方订单数据
def get_order_prescription_data(patient_doctor_list):
    # print("获取处方订单数据")
    pdList = []
    if patient_doctor_list:
        for pd in patient_doctor_list:
            prescription_dict = {}
            prescription_dict['type'] = 1
            prescription_dict['user_base_info_id'] = 0  # 老系统 0
            prescription_dict['patient_id'] = pd['patient_id']
            prescription_dict['name'] = quote_or_MYSQL_NULL(pd['patient_name'])
            # prescription_dict['name'] = add_quote(pd['patient_name'])
            prescription_dict['age'] = datetime.datetime.now().year - pd['birthday'].year
            # prescription_dict['gender'] = pd.get('sex', 1)
            prescription_dict['gender'] = 1
            prescription_dict['symptom'] = MYSQL_NULL

            # 临床诊断
            prescription_dict['illness'] = quote_or_MYSQL_NULL(pd['disease_name'])

            prescription_dict['region'] = add_quote(pd.get('province', '') + pd.get('city', ''))

            height, weight = get_height_weitht_by_age(datetime.datetime.now().year - pd['birthday'].year,
                                                      pd.get('sex', 1))

            # 用户基础信息表
            prescription_dict['height'] = add_quote(str(height))
            prescription_dict['weight'] = add_quote(str(weight))
            prescription_dict['phone_number'] = quote_or_MYSQL_NULL(pd['mobile'])
            prescription_dict['remark'] = MYSQL_NULL

            prescription_dict['self_image_url'] = MYSQL_NULL
            prescription_dict['supply_image_url'] = MYSQL_NULL
            prescription_dict['prescription_remark'] = MYSQL_NULL

            prescription_dict['audit_type'] = 1
            prescription_dict['status'] = 2

            prescription_dict['patient_advisory_id'] = MYSQL_NULL
            prescription_dict['replace_prescription_id'] = MYSQL_NULL

            prescription_dict['doctor_id'] = pd['doctor_id']
            prescription_dict['doctor_name'] = quote_or_MYSQL_NULL(pd['doctor_name'])
            prescription_dict['doctor_title'] = quote_or_MYSQL_NULL(pd['title'])
            prescription_dict['doctor_hospital_name'] = MYSQL_NULL
            prescription_dict['doctor_dept_name'] = MYSQL_NULL
            prescription_dict['dept'] = quote_or_MYSQL_NULL(pd['dept'])

            # 订单审核人
            prescription_dict['auditor_id'] = -1
            prescription_dict['auditor_name'] = MYSQL_NULL

            # 医嘱下达
            order_time = pd['order_time']
            gmt_create = pd['gmt_create']

            prescription_dict['t_order_id'] = add_quote(pd['order_id'])
            prescription_dict['redundancy'] = 1

            prescription_dict['order_time'] = add_quote(order_time.strftime(all_format_str))
            prescription_dict['gmt_create'] = add_quote(gmt_create.strftime(all_format_str))

            # 线上是gmt_create + 1天
            prescription_dict['expired_time'] = add_quote(
                (gmt_create + datetime.timedelta(days=1)).strftime(all_format_str))

            prescription_audit_time = gmt_create + datetime.timedelta(seconds=10 * random.random())
            prescription_reaudit_time = prescription_audit_time + datetime.timedelta(seconds=10 * random.random())

            # 处方审核时间
            prescription_dict['prescription_audit_time'] = add_quote(prescription_audit_time.strftime(all_format_str))
            # 处方复审时间
            prescription_dict['prescription_reaudit_time'] = add_quote(
                prescription_reaudit_time.strftime(all_format_str))

            audit_time = prescription_reaudit_time + datetime.timedelta(seconds=2000 * random.random())
            gmt_modify = audit_time + datetime.timedelta(seconds=300 * random.random())

            # 线上空
            prescription_dict['audit_time'] = add_quote(gmt_modify.strftime(all_format_str))
            prescription_dict['gmt_modify'] = add_quote(gmt_modify.strftime(all_format_str))
            prescription_dict['mall_order_time'] = MYSQL_NULL

            PRESCRIPTION_AUDITOR = [
                {'id': 10000072, 'name': '马静', 'sign_url': '/userBaseInfo/5e7b8bc4-c611-4cdc-8ca5-4a519219d5b7.png'},
                {'id': 10000077, 'name': '李洪洋', 'sign_url': '/userBaseInfo/32011cef-119b-4179-965b-8d174bced71b.png'}]

            # 打乱
            random.shuffle(PRESCRIPTION_AUDITOR)

            prescription_dict['prescription_auditor_id'] = PRESCRIPTION_AUDITOR[0]['id']
            prescription_dict['prescription_auditor_name'] = add_quote(PRESCRIPTION_AUDITOR[0]['name'])
            prescription_dict['prescription_auditor_sign_url'] = add_quote(PRESCRIPTION_AUDITOR[0]['sign_url'])
            prescription_dict['prescription_reauditor_id'] = PRESCRIPTION_AUDITOR[1]['id']
            prescription_dict['prescription_reauditor_name'] = add_quote(PRESCRIPTION_AUDITOR[1]['name'])
            prescription_dict['prescription_reauditor_sign_url'] = add_quote(PRESCRIPTION_AUDITOR[1]['sign_url'])
            prescription_dict['prescription_audit_status'] = 2
            # 医生签名
            prescription_dict['doctor_sign_url'] = MYSQL_NULL
            pdList.append(prescription_dict)

    return pdList


# 按月生成sql，并写入文件
def write_pres_sql(pres_list: typing.List, arg_dict):
    pres_insert_sql = PRES_INSERT_SQL.replace('\n', '')

    pres_template_sql = PRES_TEMPLATE_SQL.replace('\n', '').replace(' ', '')

    out_dir = Path("{OUTPUT_DIR}/prescription_{ym_range[0]}")
    out_dir.mkdir(parents=True, exist_ok=True)

    sql_out = open(
        "{out_dir}/prescription_{arg_dict['ym_date'].year}_{arg_dict['ym_date'].month}.sql",
        'ab', buffering=33554432)
    sql_out.write(pres_insert_sql.encode('utf-8'))

    first = True

    for pres in pres_list:
        if first:
            first = False
        else:
            sql_out.write(b',')
        sql_out.write(pres_template_sql.format(**pres).encode('utf-8'))

    sql_out.write(b';\n')
    sql_out.flush()
    sql_out.close()


def build_order_prescription_data(patient, doctor, order_no, order_time, gmt_create):
    prescription_dict = {}
    prescription_dict['type'] = 1
    prescription_dict['user_base_info_id'] = 0  # 老系统 0
    prescription_dict['patient_id'] = patient['id']
    prescription_dict['name'] = quote_or_MYSQL_NULL(patient['name'])
    # prescription_dict['name'] = add_quote(patient['name'])
    prescription_dict['age'] = 45
    if patient['birthday'] is not None:
        prescription_dict['age'] = datetime.datetime.now().year - patient['birthday'].year
    # prescription_dict['gender'] = quote_or_MYSQL_NULL_v2(patient.get('sex', 1))
    prescription_dict['gender'] = 1
    prescription_dict['symptom'] = MYSQL_NULL

    # 临床诊断
    prescription_dict['illness'] = quote_or_MYSQL_NULL(patient['disease_name'])

    prescription_dict['region'] = add_quote((patient.get('province', '') or '') + (patient.get('city', '') or ''))

    age = 45
    if patient['birthday'] is not None:
        age = datetime.datetime.now().year - patient['birthday'].year
    height, weight = get_height_weitht_by_age(age, patient.get('sex', 1))

    # 用户基础信息表
    prescription_dict['height'] = add_quote(str(height))
    prescription_dict['weight'] = add_quote(str(weight))
    prescription_dict['phone_number'] = quote_or_MYSQL_NULL(patient['mobile'])
    prescription_dict['remark'] = MYSQL_NULL

    prescription_dict['self_image_url'] = MYSQL_NULL
    prescription_dict['supply_image_url'] = MYSQL_NULL
    prescription_dict['prescription_remark'] = MYSQL_NULL

    prescription_dict['audit_type'] = 1
    prescription_dict['status'] = 2

    prescription_dict['patient_advisory_id'] = MYSQL_NULL
    prescription_dict['replace_prescription_id'] = MYSQL_NULL

    prescription_dict['doctor_id'] = doctor['id']
    prescription_dict['doctor_name'] = quote_or_MYSQL_NULL(doctor['name'])
    prescription_dict['doctor_title'] = quote_or_MYSQL_NULL(doctor['title'])
    prescription_dict['doctor_hospital_name'] = MYSQL_NULL
    prescription_dict['doctor_dept_name'] = MYSQL_NULL
    prescription_dict['dept'] = quote_or_MYSQL_NULL(doctor['dept'])

    # 订单审核人
    prescription_dict['auditor_id'] = -1
    prescription_dict['auditor_name'] = MYSQL_NULL

    # 医嘱下达
    order_time = order_time
    gmt_create = gmt_create

    prescription_dict['t_order_id'] = add_quote(order_no)
    # 冗余字段，区分处方来源

    prescription_dict['redundancy'] = 1

    prescription_dict['order_time'] = add_quote(order_time.strftime(all_format_str))
    prescription_dict['gmt_create'] = add_quote(gmt_create.strftime(all_format_str))

    # 线上是gmt_create + 1天
    prescription_dict['expired_time'] = add_quote(
        (gmt_create + datetime.timedelta(days=1)).strftime(all_format_str))

    # prescription_audit_time = gmt_create + datetime.timedelta(seconds=10 * random.random())
    prescription_audit_time = gmt_create + datetime.timedelta(seconds=random.randint(5, 10))
    # gmt_create = patient_register_time + datetime.timedelta(days=random.randint(2, 8))
    # prescription_reaudit_time = prescription_audit_time + datetime.timedelta(seconds=10 * random.random())

    prescription_reaudit_time = prescription_audit_time + datetime.timedelta(seconds=random.randint(5, 10))

    # 处方审核时间
    prescription_dict['prescription_audit_time'] = add_quote(prescription_audit_time.strftime(all_format_str))
    # 处方复审时间
    prescription_dict['prescription_reaudit_time'] = add_quote(
        prescription_reaudit_time.strftime(all_format_str))

    audit_time = prescription_reaudit_time + datetime.timedelta(seconds=2000 * random.random())
    gmt_modify = audit_time + datetime.timedelta(seconds=300 * random.random())

    # 线上空
    prescription_dict['audit_time'] = add_quote(gmt_modify.strftime(all_format_str))
    prescription_dict['gmt_modify'] = add_quote(gmt_modify.strftime(all_format_str))
    prescription_dict['mall_order_time'] = MYSQL_NULL

    PRESCRIPTION_AUDITOR = [
        {'id': 10000072, 'name': '马静', 'sign_url': '/userBaseInfo/5e7b8bc4-c611-4cdc-8ca5-4a519219d5b7.png'},
        {'id': 10000077, 'name': '李洪洋', 'sign_url': '/userBaseInfo/32011cef-119b-4179-965b-8d174bced71b.png'}]

    # 打乱
    random.shuffle(PRESCRIPTION_AUDITOR)

    prescription_dict['prescription_auditor_id'] = PRESCRIPTION_AUDITOR[0]['id']
    prescription_dict['prescription_auditor_name'] = add_quote(PRESCRIPTION_AUDITOR[0]['name'])
    prescription_dict['prescription_auditor_sign_url'] = add_quote(PRESCRIPTION_AUDITOR[0]['sign_url'])
    prescription_dict['prescription_reauditor_id'] = PRESCRIPTION_AUDITOR[1]['id']
    prescription_dict['prescription_reauditor_name'] = add_quote(PRESCRIPTION_AUDITOR[1]['name'])
    prescription_dict['prescription_reauditor_sign_url'] = add_quote(PRESCRIPTION_AUDITOR[1]['sign_url'])
    prescription_dict['prescription_audit_status'] = 2
    # 医生签名
    prescription_dict['doctor_sign_url'] = MYSQL_NULL

    return prescription_dict


if __name__ == '__main__':
    ym_range = tuple(int(i) for i in sys.argv[1:3])
    if ym_range:
        generate_prescription_from_excel(ym_range)
    else:
        print("get me some args please!")
