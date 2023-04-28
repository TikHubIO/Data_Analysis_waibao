# -*- encoding: utf-8 -*-
# @Author: https://github.com/TikHubIO
# @Time: 2023/04/20
# @Update: 2023/04/20
# @Version: 1.0
# @Function:
# 将接口数据从JSON转成CSV形式，并且可以进行数据选取
# @Change:

import json
import csv
import io
import sys
import os
from collections import OrderedDict


# to_string 用来将数据转换成字符串
def to_string(s):
    try:
        return str(s)
    except:
        return s.encode('utf-8')


# reduce_item 使用递归的方式将JSON文件的dict和list进行简化
def reduce_item(key, value, reduced_item):
    if type(value) is list:
        i = 0
        for sub_item in value:
            reduce_item(key + '_' + to_string(i), sub_item, reduced_item)
            i = i + 1

    elif type(value) is dict:
        sub_keys = value.keys()
        for sub_key in sub_keys:
            reduce_item(key + '_' + to_string(sub_key), value[sub_key], reduced_item)

    else:
        reduced_item[to_string(key)] = to_string(value)


# convert_json_to_csv 是用于将JSON文件转换成CSV文件的函数
def convert_json_to_csv(json_file_path, csv_file_path):
    with io.open(json_file_path, 'r', encoding='utf-8-sig') as fp:  # 读取JSON文件
        json_value = fp.read()
        raw_data = json.loads(json_value)

    processed_data = []  # 用于存储处理后的数据
    header = OrderedDict()
    for key, value in raw_data.items():
        if type(value) != dict and type(value) != list:  # 如果数据不是dict和list类型，直接将数据存储到header中
            reduced_item = {key: value}
            header.update(reduced_item)
            processed_data.append(reduced_item)
        elif type(value) == dict or type(value) == list:  # 如果数据是dict或者list类型，需要进行递归处理
            try:
                data_to_be_processed = raw_data[key]
            except:
                data_to_be_processed = raw_data
            for item in data_to_be_processed:
                reduced_item = OrderedDict()
                reduce_item(key, item, reduced_item)
                header.update(reduced_item)
                processed_data.append(reduced_item)

    header = list(header.keys())

    with open(csv_file_path, 'w+') as f:  # 将数据写入CSV文件
        writer = csv.DictWriter(f, header, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in processed_data:
            writer.writerow(row)

    path_parts = csv_file_path.strip().split(os.path.sep)
    last_file_name = path_parts[-1]

    print("Just completed writing " + str(last_file_name) + " with %d columns" % len(header))


# process_json_to_csv 是用于批量将JSON文件转换成CSV文件的函数
def process_folder_to_csv(input_folder) -> str:
    output_folder = input_folder + "_csv"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):  # 遍历文件夹中的所有文件
        if filename.endswith(".json"):
            json_file_path = os.path.join(input_folder, filename)
            csv_file_path = os.path.join(output_folder, filename.replace(".json", ".csv"))
            convert_json_to_csv(json_file_path, csv_file_path)  # 调用convert_json_to_csv函数进行转换
    return output_folder


'''
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("\nUsage: python json_to_csv.py <input_folder>\n")
    else: 
        input_folder = sys.argv[1]
        process_folder_to_csv(input_folder)
        #执行命令 python json_to_csv.py path/to/input_folder
        # path/to/input_folder 这里换成json文件夹路径就好啦
'''
