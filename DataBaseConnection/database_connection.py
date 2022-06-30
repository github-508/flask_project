import json
import numpy as np
import pandas as pd
import pymysql
from influxdb import InfluxDBClient, DataFrameClient
import os


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


def get_connection_list(user_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str_1 = "select conn_name from connection where u_id = \'{}\' and db_type = 'mysql'".format(user_name)
    sql_str_2 = "select conn_name from connection where u_id = \'{}\' and db_type = 'influxdb'".format(user_name)

    cursor.execute(sql_str_1)
    res_1 = cursor.fetchall()
    cursor.execute(sql_str_2)
    res_2 = cursor.fetchall()
    ans = {}
    ans_1 = []
    ans_2 = []
    for row in res_1:
        ans_1.append(row[0])
    for row in res_2:
        ans_2.append(row[0])
    # print(ans)
    cursor.close()
    conn.close()
    ans['mysql'] = ans_1
    ans['influxdb'] = ans_2
    # print(ans)
    return json.dumps(ans)


def create_connection(user_name, con_name, host_name, port_num, db_user, db_password, db_name, db_type):
    if db_type == "mysql":
        try:
            con = pymysql.connect(host=host_name, port=port_num, user=db_user, passwd=db_password, db=db_name, charset="utf8")
        except BaseException as e:
            return "连接创建失败，请检查输入的参数是否有错误"
        else:
            conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
            cursor = conn.cursor()
            sql_str_insert = "insert into connection(u_id,conn_name,host,port,db_user,db_password, db_name, db_type) \
                values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".\
                format(user_name, con_name, host_name, port_num, db_user, db_password, db_name, db_type)
            try:
                cursor.execute(sql_str_insert)
                conn.commit()
            except BaseException as e:
                conn.rollback()
                cursor.close()
                conn.close()
                return "连接保存失败"
            else:
                # print("连接实例创建成功")
                cursor.close()
                conn.close()
                return "连接实例创建成功"
    if db_type == "influxdb":
        try:
            client = InfluxDBClient(host=host_name, port=port_num, username=db_user, password=db_password, database=db_name)
            client.query('show measurements;')
        except BaseException as e:
            print(e)
            return "Influxdb连接创建失败，请检查输入的参数是否有错误"
        else:
            conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
            cursor = conn.cursor()
            sql_str_insert = "insert into connection(u_id,conn_name,host,port,db_user,db_password, db_name, db_type) \
                values (\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".\
                format(user_name, con_name, host_name, port_num, db_user, db_password, db_name, db_type)
            try:
                cursor.execute(sql_str_insert)
                conn.commit()
            except BaseException as e:
                conn.rollback()
                # print("Exception:")
                # print(e)
                # print("连接保存失败")
                cursor.close()
                conn.close()
                return "influxdb 连接保存失败"
            else:
                # print("连接实例创建成功")
                cursor.close()
                conn.close()
                return "influxdb 连接实例创建成功"


def delete_connection(user_name, con_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str_delete = "delete from connection where u_id = \'{}\' and conn_name = \'{}\'".format(user_name, con_name)
    try:
        cursor.execute(sql_str_delete)
        conn.commit()
    except:
        conn.rollback()
        cursor.close()
        conn.close()
        return "删除失败"
    else:
        cursor.close()
        conn.close()
        return "数据库连接实例已删除"


def get_table_from_db(user_name, con_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select host,port,db_user,db_password,db_name from connection where u_id = \'{}\' and conn_name = \'{}\' and db_type \
        = 'mysql'".format(user_name, con_name)
    cursor.execute(sql_str)
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    try:
        conn_search = pymysql.connect(host=res[0], port=res[1], user=res[2], passwd=res[3], db=res[4], charset="utf8")
    except:
        conn_search.close()
        print("连接失败，该连接可能已失效，请检查原数据库")
        return "连接失败，该连接可能已失效，请检查原数据库"
    else:
        cursor_search = conn_search.cursor()
        cursor_search.execute("show tables")
        ans_list = [tuple[0] for tuple in cursor_search.fetchall()]
        cursor_search.close()
        conn_search.close()
        # print(json.dumps(ans_list))
        return json.dumps(ans_list)


def get_measurements_from_db(user_name, con_name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select host,port,db_user,db_password,db_name from connection where u_id = \'{}\' and conn_name = \'{}\' and db_type \
        = 'influxdb'".format(user_name, con_name)
    cursor.execute(sql_str)
    res = cursor.fetchone()
    cursor.close()
    conn.close()
    try:
        client = InfluxDBClient(host=res[0], port=res[1], username=res[2], password=res[3], database=res[4])
    except BaseException as e:
        print(e)
        return "Error!"
    else:
        result = client.query('show measurements;')
        ans_list = []
        for item in result:
            for it in item:
                ans_list.append(it['name'])
        return json.dumps(ans_list)


def get_fields_from_tables(user_name, con_name, table_list):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select host,port,db_user,db_password,db_name from connection where u_id = \'{}\' and conn_name = \'{}\' and db_type \
        = 'mysql'".format(user_name, con_name)
    cursor.execute(sql_str)
    cursor.close()
    conn.close()
    res = cursor.fetchone()
    ans_json = {}
    try:
        conn_search = pymysql.connect(host=res[0], port=res[1], user=res[2], passwd=res[3], db=res[4], charset="utf8")
    except:
        conn_search.close()
        print("连接失败，该连接可能已失效，请检查原数据库")
        # return "连接失败，该连接可能已失效，请检查原数据库"
    else:
        cursor_search = conn_search.cursor()
        for item in table_list:
            cursor_search.execute("select * from %s" % item)
            ans_json[item] = [tuple[0] for tuple in cursor_search.description]
            # ans_json[item] = [tuple for tuple in cursor_search.description]
        cursor_search.close()
        conn_search.close()
        # print(json.dumps(ans_json))
        return json.dumps(ans_json)


def get_fields_from_measurements(user_name, con_name, table_list):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select host,port,db_user,db_password,db_name from connection where u_id = \'{}\' and conn_name = \'{}\' and db_type \
        = 'influxdb'".format(user_name, con_name)
    cursor.execute(sql_str)
    cursor.close()
    conn.close()
    res = cursor.fetchone()
    ans_json = {}
    try:
        client = InfluxDBClient(host=res[0], port=res[1], username=res[2], password=res[3], database=res[4])
    except BaseException as e:
        print(e)
        return "error"
    else:
        for item in table_list:
            result_fields = client.query("show field keys from %s" % item)
            result_tags = client.query("show tag keys from %s" % item)
            ans_json[item] = []
            for res in result_fields:
                for it in res:
                    ans_json[item].append(f'\"{it["fieldKey"]}\"::field')
            for res in result_tags:
                for it in res:
                    ans_json[item].append(f'\"{it["tagKey"]}\"::tag')
        # print(ans_json)
        return json.dumps(ans_json)
            # print(result2)
        ans_list = []
        #for item in result:
          #  for it in item:
          #      ans_list.append(it['name'])
        #return json.dumps(ans_list)


def tables_to_file(user_name, con_name, tables_fields, file_name, meth):
    file_path = "/home/wmy/Desktop/Resource/{}/worksheet/{}.csv".format(user_name, file_name)
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select host,port,db_user,db_password,db_name from connection where u_id = \'{}\' and conn_name = \'{}\' and db_type \
        = 'mysql'".format(user_name, con_name)
    cursor.execute(sql_str)
    cursor.close()
    conn.close()
    res = cursor.fetchone()
    try:
        conn_extract = pymysql.connect(host=res[0], port=res[1], user=res[2], passwd=res[3], db=res[4], charset="utf8")
    except:
        conn_extract.close()
        print("连接失败，该连接可能已失效，请检查原数据库")
    else:
        first_table = ""
        label_index = ""
        sql_extract = ""
        # cursor_extract = conn_extract.cursor()
        if meth == "UNION":
            cnt = 0
            for key in tables_fields:
                if cnt == 0:
                    label_index = key
                    first_table = key
                cnt += 1
                sql_extract += "select " + ','.join(tables_fields[key]) + " from " + key
                if cnt < len(tables_fields):
                    sql_extract += " UNION "
            print(sql_extract)
        if meth == "INNER JOIN":
            cnt = 0
            join_str = ""
            sql_extract = "select "
            for key in tables_fields:
                sql_extract += f'{key}.'
                if cnt == 0:
                    label_index = key
                    first_table = key
                cnt += 1
                sql_extract += f',{key}.'.join(tables_fields[key])
                join_str += key
                if cnt < len(tables_fields):
                    sql_extract += ","
                    join_str += " INNER JOIN "
            sql_extract += " from " + join_str
            print(sql_extract)
        if meth == "LEFT JOIN":
            cnt = 0
            join_str = ""
            on_str = " on "
            sql_extract = "select "
            for key in tables_fields:
                on_str += f'{key}.{tables_fields[key][0]}'
                sql_extract += f'{key}.'
                if cnt == 0:
                    label_index = key
                    first_table = key
                cnt += 1
                sql_extract += f',{key}.'.join(tables_fields[key])
                join_str += key
                if cnt < len(tables_fields):
                    sql_extract += ","
                    join_str += " LEFT JOIN "
                    on_str += " = "
            sql_extract += " from " + join_str
            sql_extract += on_str
            print(sql_extract)
        if meth == "RIGHT JOIN":
            cnt = 0
            join_str = ""
            sql_extract = "select "
            for key in tables_fields:
                sql_extract += f'{key}.'
                if cnt == 0:
                    label_index = key
                    first_table = key
                cnt += 1
                sql_extract += f',{key}.'.join(tables_fields[key])
                join_str += key
                if cnt < len(tables_fields):
                    sql_extract += ","
                    join_str += " RIGHT JOIN "
            sql_extract += " from " + join_str
            print(sql_extract)
        # cursor_extract.execute(sql_extract)
        # extract_ans = cursor_extract.fetchall()
        # cursor_extract.close()
        if tables_fields[label_index][0] == "*":
            list_tables = list()
            list_tables.append(first_table)
            fields = get_fields_from_tables(user_name, con_name, list_tables)
            fields = json.loads(fields)
            # print(fields)
            # print(type(fields))
            first_field = fields[first_table][0]
            extract_ans = pd.read_sql_query(sql_extract, conn_extract, index_col=first_field)
        else:
            extract_ans = pd.read_sql_query(sql_extract, conn_extract, index_col=tables_fields[label_index][0])
        conn_extract.close()
        df = pd.DataFrame(extract_ans)
        # print(df)
        # print(extract_ans)
    if os.path.exists(file_path):
        print("文件名已存在，请更名")
        return "文件名已存在，请更名"
    else:
        # print("ok!")
        df.to_csv(file_path)


        if os.path.exists(file_path):
            conn_add_file = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
            cursor_add_file = conn_add_file.cursor()
            sql_str = "insert into worksheet(u_id,file_name) values (\'{}\',\'{}\')".format(user_name, file_name)
            try:
                cursor_add_file.execute(sql_str)
                conn_add_file.commit()
            except:
                conn_add_file.rollback()
                cursor_add_file.close()
                conn_add_file.close()
                return "文件添加失败"
            else:
                cursor_add_file.close()
                conn_add_file.close()
                return "文件添加成功"


def measurements_to_file(user_name, con_name, measurements_fields, file_name, record_cnt=1500):
    file_path = "/home/wmy/Desktop/Resource/{}/worksheet/{}.csv".format(user_name, file_name)
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select host,port,db_user,db_password,db_name from connection where u_id = \'{}\' and conn_name = \'{}\' and db_type \
        = 'influxdb'".format(user_name, con_name)
    cursor.execute(sql_str)
    cursor.close()
    conn.close()
    res = cursor.fetchone()
    try:
        client = DataFrameClient(host=res[0], port=res[1], username=res[2], password=res[3], database=res[4])
    except BaseException as e:
        print(e)
        return "error"
    else:
        sql_extract = "select "
        measure_list = []
        # print(measurements_fields)
        cnt = 0
        for item in measurements_fields:
            if cnt > 0:
                sql_extract += ','
            cnt += 1
            sql_extract += ','.join(measurements_fields[item])
            measure_list.append(item)
        sql_extract += " from "
        sql_extract += ','.join(measure_list)
        sql_extract += f' limit {record_cnt}'
        print(sql_extract)
        result = client.query(sql_extract)
        measure_name = ""
        for item in result:
            measure_name = item
        data = pd.DataFrame(result[measure_name])
        # col_list = ["time"]
        # data.columns = col_list
        # data.rename(columns={'': 'time'}, inplace=True)
        data.to_csv(file_path)
        if os.path.exists(file_path):
            add_file_to_worksheet(user_name, file_name)
            return "文件添加成功"
        # print(data)
        return "文件添加失败"


def get_measurement_record_cnt(user_name, con_name, measurements_fields):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select host,port,db_user,db_password,db_name from connection where u_id = \'{}\' and conn_name = \'{}\' and db_type \
        = 'influxdb'".format(user_name, con_name)
    cursor.execute(sql_str)
    cursor.close()
    conn.close()
    res = cursor.fetchone()
    try:
        client = DataFrameClient(host=res[0], port=res[1], username=res[2], password=res[3], database=res[4])
    except BaseException as e:
        print(e)
        return "error"
    else:
        sql_extract = "select count(*) from (select "
        measure_list = []
        # print(measurements_fields)
        cnt = 0
        for item in measurements_fields:
            if cnt > 0:
                sql_extract += ','
            cnt += 1
            sql_extract += ','.join(measurements_fields[item])
            measure_list.append(item)
        sql_extract += " from "
        sql_extract += ','.join(measure_list)
        # cnt = 4000
        # sql_extract += f' limit {cnt}'
        sql_extract += " )"
        print(sql_extract)
        result = client.query(sql_extract)
        record_cnt = 0
        for item in result:
            record_cnt = result[item].iloc[0, 0]
        return json.dumps(str(record_cnt))


if __name__ == "__main__":
    name = "biter"
    con_demo = "NOAA_DEMO"
    host_ip = "127.0.0.1"
    # port = 3306
    port = 8086
    database_user = "root"
    database_password = "root"
    database_name = "NOAA_water_database"
    database_type = "influxdb"
    method = "INNER JOIN"
    f_name = "sqlFile"
    # ans = get_connection_list(name)
    # print(ans)
    list_demo = ["average_temperature", "h2o_feet", "h2o_pH", "h2o_quality", "h2o_temperature"]
    file_js = {'h2o_feet': ['"level description"::field', '"water_level"::field', '"location"::tag']}
    # measurements_to_file(name, con_demo, file_js, "4567")
    ans = get_measurement_record_cnt(name, con_demo, file_js)
    print(ans)

