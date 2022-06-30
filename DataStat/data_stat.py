# -*- coding : utf-8-*-
import json
import numpy as np
import pandas as pd
import pymysql
import os
import base64
from flask import jsonify
import re
import ast


def data_stat(user_name, load_file_name, field_list):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, load_file_name)
    columns = field_list
    df = pd.read_csv(file_path)
    ans = {}
    for field in columns:
        # 平均值
        field_mean = df[field].mean()
        field_mean = round(field_mean, 2)
        # 最大值
        field_max = df[field].max()
        field_max = round(field_max, 2)
        # 最小值
        field_min = df[field].min()
        field_min = round(field_min, 2)
        # 中位数
        field_median = df[field].median()
        field_median = round(field_median, 2)
        # 偏度
        field_skew = df[field].skew()
        field_skew = round(field_skew, 2)
        # 峰度
        field_kurt = df[field].kurt()
        field_kurt = round(field_kurt, 2)
        ans[field] = {'name': field, 'mean': str(field_mean), 'max': str(field_max), 'min': str(field_min),
                      'median': str(field_median), 'skew': str(field_skew), 'kurt': str(field_kurt)}
    corr_ans = df[columns].corr().to_json(orient='split')


    ans['corr'] = ast.literal_eval(corr_ans)
    return ans


def save_stat(user_name, file_name, stat_ans, industry):
    file_path = "../Resource/{}/statistics/{}.json".format(user_name, file_name)
    if os.path.exists(file_path):
        return "该统计分析文件已存在，请重新输入名称"
    else:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(stat_ans, indent=2, ensure_ascii=False))
        if os.path.exists(file_path):
            conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
            cursor = conn.cursor()
            sql_str_insert = "insert into stat(u_id,stat_file_name,industry) values (\'{}\',\'{}\',\'{}\')".\
                format(user_name, file_name, industry)
            try:
                cursor.execute(sql_str_insert)
                conn.commit()
            except:
                conn.rollback()
            cursor.close()
            conn.close()
            return "结果保存成功"
        else:
            return "结果保存失败"


def delete_stat_item(user_name, file_name):
    file_path = "../Resource/{}/statistics/{}.json".format(user_name, file_name)
    if not os.path.exists(file_path):
        return "统计分析文件不存在"
    else:
        os.remove(file_path)
        if not os.path.exists(file_path):
            conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
            cursor = conn.cursor()
            sql_str_delete = "delete from stat where u_id = \'{}\' and stat_file_name = \'{}\'".format(user_name, file_name)
            try:
                cursor.execute(sql_str_delete)
                conn.commit()
            except:
                conn.rollback()
            cursor.close()
            conn.close()
            return "统计分析文件已删除"
        else:
            return "删除失败"


def get_stat_list(user_name, industry):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select stat_file_name from stat where u_id = \'{}\' and industry = \'{}\'".format(user_name, industry)
    cursor.execute(sql_str)
    res = cursor.fetchall()
    stat_list = []
    for row in res:
        stat_list.append(row[0])
    # print(stat_list)
    cursor.close()
    conn.close()
    return json.dumps(stat_list)


def load_stat_ans(user_name, file_name):
    file_path = "../Resource/{}/statistics/{}.json".format(user_name, file_name)
    if not os.path.exists(file_path):
        return "统计分析文件不存在"
    else:
        with open(file_path) as file:
            json_ans = json.load(file)
            return json_ans


def data_stat_car():
    dir_path = "/home/wmy/Desktop/test_data/BSX_01_99AZD_20180118154338/form3/Regularity_1/"
    ans = {}
    ans['csv'] = []
    ans['img'] = []
    file_list = []
    file_list = os.listdir(dir_path)
    cnt = 0
    for item in file_list:
        if re.findall('.csv$', item):
            # print("csv")
            data = pd.read_csv(os.path.join(dir_path, item), encoding='gbk')
            csv_json = data.to_json(orient='split')
            ans['csv'].append(ast.literal_eval(csv_json))
        if re.findall('.jpg$', item):
            img_stream = ''
            with open(os.path.join(dir_path, item), 'rb') as img_f:
                img_stream = base64.b64encode(img_f.read())
            # if cnt == 0:
            ans['img'].append(img_stream.decode())
    return json.dumps(ans)
    # print(item)


if __name__ == "__main__":
    name = "biter"
    f_name = "demo1"
    var_list = ["Gaoshu", "Dawu", "Daying"]
    # xlsx_csv_db(name, _name)
    # xlsx_csv_file_name(name)
    # del_xlsx_csv_file(name, _name)
    # stat_corr, stat_json = data_stat(name, f_name, var_list)
    # data_stat(name, f_name, var_list)
    # stat_json['corr'] = stat_corr
    # print(stat_corr)
    # print(stat_json)
    data_stat_car()
