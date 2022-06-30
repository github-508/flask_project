import pymysql
from flask import jsonify
import json


def login_check(name, password):
    conn = pymysql.connect(host='localhost',user = "root",passwd = "root",db = "data_anl")
    cursor=conn.cursor()
    sql_str_check = "select * from user where user_id = \'{}\'".format(name)
    sql_str_login = "select * from user where user_id = \'{}\' and user_password = \'{}\'".format(name,password)
    cursor.execute(sql_str_check)
    res = cursor.fetchone()
    # 用户不存在
    if res is None:
        return json.dumps(-1)
    else:
        cursor.execute(sql_str_login)
        res = cursor.fetchone()
        if res is None:
            # 密码错误
            return json.dumps(0)
        else:
            cursor.execute("update user set user_status = 1 where user_id = \'{}\'".format(name))
            conn.commit()
    cursor.close()
    conn.close()
    return json.dumps(res)
    # return jsonify(ans3)


def logout(name):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    # sql_str_change = "update user set user_status = 0 where user_id = \'{}\'".format(name)
    cursor.execute("update user set user_status = 0 where user_id = \'{}\'".format(name))
    conn.commit()
    cursor.close()
    conn.close()
    return json.dumps("logout")


if __name__ == "__main__":
    user_name = "biter"
    user_password = "biter"
    # ret = login_check(user_name, user_password)
    ret = logout(user_name)
    print(ret)
