import pymysql
from flask import jsonify
import json


def register(name, password, mail):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select * from user where user_id = \'{}\'".format(name)
    sql_str_register = "insert into user(user_id,user_password,user_mail,user_status) values (\'{}\',\'{}\',\'{}\',0)" \
                        .format(name, password, mail)
    # 检查用户是否存在
    cursor.execute(sql_str)
    res = cursor.fetchone()
    flag = 1
    # 用户不存在则允许注册
    if res is None:
        try:
            cursor.execute(sql_str_register)
            conn.commit()
            # res = cursor.fetchone()
        except:
            conn.rollback()
            flag = 0
    else:
        flag = -1
    cursor.close()
    conn.close()
    return json.dumps(flag)


if __name__ == "__main__":
    user_name = "user"
    user_password = "user"
    user_mail = "1120180298@qq.com"

    '''
    ret == -1,user_name has exits
    ret == 0  register fail
    ret == 1 register success
    '''

    ret = register(user_name, user_password, user_mail)
    if ret == -1:
        print(ret)
        print("该用户名已被使用")
    elif ret == 0:
        print(ret)
        print("注册失败")
    else:
        print(ret)
        print("%s 注册成功" %(user_name))

