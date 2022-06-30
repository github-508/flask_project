import pymysql
import json
import numpy as np
import pandas as pd
from flask import jsonify


def xlsx_csv_db(user_name, f_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "insert into datasrc(u_id,file_name) values (\'{}\',\'{}\')".format(user_name, f_name)
    try:
        cursor.execute(sql_str)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()
    conn.close()
    return 0


def xlsx_csv_file_name(user_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select file_name from datasrc where u_id = \'{}\'".format(user_name)
    cursor.execute(sql_str)
    res = cursor.fetchall()
    ans = []
    for row in res:
        ans.append(row[0])
    # print(ans)
    cursor.close()
    conn.close()
    return json.dumps(ans)


def csv_file_name(user_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select file_name from worksheet where u_id = \'{}\'".format(user_name)
    cursor.execute(sql_str)
    res = cursor.fetchall()
    ans = []
    for row in res:
        ans.append(row[0])
    # print(ans)
    cursor.close()
    conn.close()
    return json.dumps(ans)


def get_file_name_process(user_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select file_name from processplatform where u_id = \'{}\'".format(user_name)
    cursor.execute(sql_str)
    res = cursor.fetchall()
    ans = []
    for row in res:
        ans.append(row[0])
    # print(ans)
    cursor.close()
    conn.close()
    return json.dumps(ans)


def del_xlsx_csv_file(user_name, del_file_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "delete from datasrc where u_id = \'{}\' and file_name = \'{}\'".format(user_name, del_file_name)
    try:
        cursor.execute(sql_str)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()
    conn.close()
    return 0


def del_from_worksheet(user_name, del_file_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "delete from worksheet where u_id = \'{}\' and file_name = \'{}\'".format(user_name, del_file_name)
    try:
        cursor.execute(sql_str)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()
    conn.close()
    return 0


def del_from_process_platform(user_name, del_file_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "delete from processplatform where u_id = \'{}\' and file_name = \'{}\'".format(user_name, del_file_name)
    try:
        cursor.execute(sql_str)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()
    conn.close()
    return 0


def add_file_to_worksheet(user_name, add_file_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "insert into worksheet(u_id,file_name) values (\'{}\',\'{}\')".format(user_name, add_file_name)
    try:
        cursor.execute(sql_str)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()
    conn.close()
    return 0


def add_file_to_process_platform(user_name, add_file_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "insert into processplatform(u_id,file_name) values (\'{}\',\'{}\')".format(user_name, add_file_name)
    try:
        cursor.execute(sql_str)
        conn.commit()
    except:
        conn.rollback()
    cursor.close()
    conn.close()
    return 0


def load_worksheet_file(user_name, load_file_name):
    file_path = "../Resource/{}/worksheet/{}.csv".format(user_name, load_file_name)
    # df = pd.read_csv(file_path, nrows=2000)
    df = pd.read_csv(file_path)
    # print(df)
    # print(df.to_json(orient='index'))
    return df.to_json(orient='records')


def load_process_platform_file(user_name, load_file_name):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, load_file_name)
    # df = pd.read_csv(file_path,  nrows=2000)
    df = pd.read_csv(file_path)
    # print(df)
    # print(df.to_json(orient='index'))
    return df.to_json(orient='records')


def load_file_visual(user_name, load_file_name):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, load_file_name)
    df = pd.read_csv(file_path, nrows=2000)
    # print(df.to_json(orient='columns'))
    return df.to_json(orient='columns')


def load_stat_fields(user_name, load_file_name):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, load_file_name)
    df = pd.read_csv(file_path)
    ans = {}
    # print(df.columns.tolist())
    ans['columns'] = df.columns.tolist()
    # print(json.dumps(ans))
    # print(df.to_json(orient='split')["columns"])
    # return df.to_json(orient='columns')
    return json.dumps(ans)


if __name__ == "__main__":
    name = "biter"
    file_name = "股票数据(含缺失值)"
    ans = load_process_platform_file(name, file_name)
    print(ans)
