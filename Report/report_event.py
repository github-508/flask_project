import os
import pymysql
import numpy as np
import json
import pandas as pd


def generate_report(user_name, visual_list=None, stat_list=None):
    visual_ans_list = []
    stat_ans_list = []
    ans = {}
    for f in visual_list:
        visual_file_path = "../Resource/{}/visual/{}.json".format(user_name, f)
        with open(visual_file_path) as file:
            json_ans = json.load(file)
            visual_ans_list.append(json_ans)
    for f in stat_list:
        stat_file_path = "../Resource/{}/statistics/{}.json".format(user_name, f)
        with open(stat_file_path) as file:
            json_ans = json.load(file)
            stat_ans_list.append(json_ans)
    ans["visual"] = visual_ans_list;
    ans["stat"] = stat_ans_list
    # print(ans)
    return ans


def save_report(user_name, file_name, report_ans):
    file_path = "../Resource/{}/report/{}.json".format(user_name, file_name)
    if os.path.exists(file_path):
        return "该报告已存在，请重新输入名称"
    else:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(report_ans, indent=2, ensure_ascii=False))
        if os.path.exists(file_path):
            conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
            cursor = conn.cursor()
            sql_str_insert = "insert into report(u_id,report_name) values (\'{}\',\'{}\')".format(user_name, file_name)
            try:
                cursor.execute(sql_str_insert)
                conn.commit()
            except:
                conn.rollback()
                cursor.close()
                conn.close()
            else:
                cursor.close()
                conn.close()
                return "结果保存成功"
        else:
            return "结果保存失败"


def delete_report(user_name, file_name):
    file_path = "../Resource/{}/report/{}.json".format(user_name, file_name)
    if not os.path.exists(file_path):
        return "报告不存在"
    else:
        os.remove(file_path)
        if not os.path.exists(file_path):
            conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
            cursor = conn.cursor()
            sql_str_delete = "delete from report where u_id = \'{}\' and report_name = \'{}\'".format(user_name,file_name)
            try:
                cursor.execute(sql_str_delete)
                conn.commit()
            except:
                conn.rollback()
                cursor.close()
                conn.close()
            else:
                cursor.close()
                conn.close()
                return "报告已删除"
        else:
            return "报告删除失败"


def get_report_list(user_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select report_name from report where u_id = \'{}\'".format(user_name)
    cursor.execute(sql_str)
    res = cursor.fetchall()
    report_list = []
    for row in res:
        report_list.append(row[0])
    # print(report_list)
    cursor.close()
    conn.close()
    # print(report_list)
    return json.dumps(report_list)


def load_report(user_name, file_name):
    file_path = "../Resource/{}/report/{}.json".format(user_name, file_name)
    if not os.path.exists(file_path):
        return "报告不存在"
    else:
        with open(file_path) as file:
            json_ans = json.load(file)
            return json_ans


if __name__ == "__main__":
    name = "biter"
    visuals = ["成绩", "股票"]
    stats = ["成绩"]
    # generate_report(name, visuals, stats)
    get_report_list(name)
