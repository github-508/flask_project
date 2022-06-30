import json
import pymysql
import os


def save_visual(user_name, file_name, visual_ans, industry):
    file_path = "/home/wmy/Desktop/Resource/{}/visual/{}.json".format(user_name, file_name)
    if os.path.exists(file_path):
        return "该可视化文件已存在，请重新输入名称"
    else:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(visual_ans, indent=2, ensure_ascii=False))
        if os.path.exists(file_path):
            conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
            cursor = conn.cursor()
            sql_str_insert = "insert into visual(u_id,visual_file_name,industry) values (\'{}\',\'{}\',\'{}\')".\
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


def delete_visual_item(user_name, file_name):
    file_path = "/home/wmy/Desktop/Resource/{}/visual/{}.json".format(user_name, file_name)
    if not os.path.exists(file_path):
        return "可视化文件不存在"
    else:
        os.remove(file_path)
        if not  os.path.exists(file_path):
            conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
            cursor = conn.cursor()
            sql_str_delete = "delete from visual where u_id = \'{}\' and visual_file_name = \'{}\'".format(user_name,file_name)
            try:
                cursor.execute(sql_str_delete)
                conn.commit()
            except:
                conn.rollback()
            cursor.close()
            conn.close()
            return "可视化图表已删除"
        else:
            return "删除失败"


def get_visual_list(user_name, industry):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select visual_file_name from visual where u_id = \'{}\' and industry = \'{}\'".format(user_name, industry)
    cursor.execute(sql_str)
    res = cursor.fetchall()
    visual_list = []
    for row in res:
        visual_list.append(row[0])
    # print(visual_list)
    cursor.close()
    conn.close()
    return json.dumps(visual_list)


def load_visual_ans(user_name, file_name):
    file_path = "/home/wmy/Desktop/Resource/{}/visual/{}.json".format(user_name, file_name)
    if not os.path.exists(file_path):
        return "可视化文件不存在"
    else:
        with open(file_path) as file:
            json_ans = json.load(file)
            return json_ans


if __name__ == "__main__":
    name = "biter"
    f_name = "test2"
    indst = "智能数据分析"
    test_js = {'l': [1, 2, 3, 4, 5], 'f': {'a': "hhh", 'b': 3, 'd': [1, 2, 3, 4]}}
    # ans = save_visual(name, f_name, test_js)
    # print(ans)
    # ans = delete_visual_item(name,f_name)
    # print(ans)
    ans = get_visual_list(name, indst)
    # print(ans)
    # ans = load_visual_ans(name, f_name)
    print(ans)

