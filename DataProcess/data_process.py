import os
import pymysql
import numpy as np
import json
import pandas as pd
import ast


# 定义求取特征是否完全相同的矩阵的函数
def feature_equals(df):
    df_equals = pd.DataFrame([], columns=df.columns, index=df.columns)
    for i in df.columns:
        for j in df.columns:
            df_equals.loc[i, j]=df.loc[:, i].equals(df.loc[:, j])
    return df_equals


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


def data_merge(user_name, file_list, new_file_name, meth):
    new_file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, new_file_name)
    if os.path.exists(new_file_path):
        return "file_name exists"
    else:
        df_list = list()
        for f in file_list:
            file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, f)
            df = pd.read_csv(file_path)
            df_list.append(df)
        # for df_temp in df_list:
            # print(df_temp)
        if meth == "merge":
            ans = pd.merge(df_list[0], df_list[1])
            # print(ans)
            list_l = len(df_list) - 2
            for i in range(list_l):
                # print(i)
                # print(df_list[i])
                ans = pd.merge(ans, df_list[i + 2])
            ans.to_csv(new_file_path, index=False)
            if os.path.exists(new_file_path):
                add_file_to_process_platform(user_name, new_file_name)
            return "主键合并完成"
        if meth == "concat_0":
            ans = pd.concat(df_list, join='outer', ignore_index=True)
            ans.to_csv(new_file_path, index=False)
            if os.path.exists(new_file_path):
                add_file_to_process_platform(user_name, new_file_name)
            return "纵向堆叠完成"
        if meth == "concat_1":
            ans = pd.concat(df_list, axis=1, join='outer', ignore_index=False)
            ans.to_csv(new_file_path, index=False)
            if os.path.exists(new_file_path):
                add_file_to_process_platform(user_name, new_file_name)
            return "横向堆叠完成"
        # ans = pd.merge(df_list)
        # print(ans)


def nan_process(user_name, file_name, process_meth, process_flag, field_list=None, fill_value=None):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    data = pd.read_csv(file_path)
    # print(data)
    if process_meth == "drop":
        if process_flag == "0":
            data.dropna(inplace=True)
            # print(data)
            data.to_csv(file_path, index=False)
            return "已删除存在空值的记录"
        if process_flag == "1":
            data.dropna(how='all', inplace=True)
            # print(data)
            data.to_csv(file_path, index=False)
            return "已删除整行为空值的记录"
        if process_flag == "2":
            data.dropna(subset=field_list, inplace=True)
            # print(data)
            data.to_csv(file_path, index=False)
            return "已删除所选判断特征为空值的记录"
    if process_meth == "fill":
        if process_flag == "0":
            # 整表缺失值替换
            data.fillna(fill_value, inplace=True)
            # print(data)
            data.to_csv(file_path, index=False)
            return "整表缺失值替换已完成"
        if process_flag == "1":
            # 前置填充
            data.fillna(method="ffill", inplace=True)
            # print(data)
            data.to_csv(file_path, index=False)
            return "前置填充已完成"
        if process_flag == "2":
            # 后置填充
            data.fillna(method="bfill", inplace=True)
            # print(data)
            data.to_csv(file_path, index=False)
            return "后置填充已完成"
        if process_flag == "3":
            # 均值填充特征缺失值
            field_dict = {}
            for item in field_list:
                field_dict[item] = data[item].mean()
            data[field_list] = data[field_list].fillna(field_dict)
            # print(data)
            data.to_csv(file_path, index=False)
            return "均值填充特征缺失值"
        if process_flag == "4":
            # 中位数填充特征缺失值
            field_dict = {}
            for item in field_list:
                field_dict[item] = data[item].median()
            data[field_list] = data[field_list].fillna(field_dict)
            # print(data)
            data.to_csv(file_path, index=False)
            return "中位数填充特征缺失值"
        if process_flag == "5":
            # 众数填充特征缺失值
            field_dict = {}
            for item in field_list:
                field_dict[item] = data[item].mode()
            data[field_list] = data[field_list].fillna(field_dict)
            # print(data)
            data.to_csv(file_path, index=False)
            return "众数填充特征缺失值"
        if process_flag == "6":
            # 自定义填充特征缺失值
            field_dict = {}
            for item in field_list:
                field_dict[item] = fill_value
            data[field_list] = data[field_list].fillna(field_dict)
            # print(data)
            data.to_csv(file_path, index=False)
            return "自定义填充特征缺失值已完成"
    if process_meth == "inter":
        if process_flag == "0":
            # 线性插值
            # print(field_list)
            data[field_list] = data[field_list].interpolate(method="linear", limit_direction="forward")
            # print(data)
            data.to_csv(file_path, index=False)
            return "线性插值已完成"
        if process_flag == "1":
            # 二次多项式插值
            data[field_list] = data[field_list].interpolate(method="polynomial", order=2)
            # print(data)
            data.to_csv(file_path, index=False)
            return "二次多项式插值已完成"
        if process_flag == "2":
            # 三次样条插值
            data[field_list] = data[field_list].interpolate(method="spline", order=3)
            # print(data)
            data.to_csv(file_path, index=False)
            return "三次样条插值已完成"


def duplicate_process(user_name, file_name, duplicate_axis, process_flag, field_list=None):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    data = pd.read_csv(file_path)
    # print(data)
    if duplicate_axis == "row":
        if process_flag == "0":
            data.drop_duplicates(inplace=True)
            data = data.reset_index(drop=True)
            # print(data)
            data.to_csv(file_path, index=False)
            return "已删除重复行"
        if process_flag == "1":
            data.drop_duplicates(subset=field_list, inplace=True)
            data = data.reset_index(drop=True)
            # print(data)
            data.to_csv(file_path, index=False)
            return "已删除重复行"
    if duplicate_axis == "col":
        # if process_flag == "0":
        df_equals = feature_equals(data)
        dup_col = []
        for i in range(df_equals.shape[0]):
            for j in range(i+1, df_equals.shape[0]):
                if df_equals.iloc[i, j] & (df_equals.columns[j] not in dup_col):
                    dup_col.append(df_equals.columns[j])
        data.drop(dup_col, axis=1, inplace=True)
        # print(data)
        data.to_csv(file_path, index=False)
        return "已删除重复列"


# 离差标准化
def min_max_scale(user_name, file_name, field_list):
    print("离差标准化")
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    data = pd.read_csv(file_path)
    # print(data)
    data[field_list] = (data[field_list] - data[field_list].min()) / (data[field_list].max() - data[field_list].min())
    print("离差标准化 ok")
    # print(data)
    data.to_csv(file_path, index=False)
    # data.to_csv("/home/wmy/Desktop/Resource/biter/processplatform/1.csv", index=False)
    return "离差标准化已完成"


# 标准差标准化
def standard_scale(user_name, file_name, field_list):
    print("标准差标准化")
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    data = pd.read_csv(file_path)
    # print(data)
    data[field_list] = (data[field_list] - data[field_list].min()) / data[field_list].std()
    print("标准差标准化 ok")
    # print(data)
    data.to_csv(file_path, index=False)
    return "标准差标准化已完成"


# 小数定标标准化
def decimal_scale(user_name, file_name, field_list):
    print("小数定标标准化")
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    data = pd.read_csv(file_path)
    # print(data)
    data[field_list] = data[field_list]/10**np.ceil(np.log10(data[field_list].abs().max()))
    print("小数定标标准化 ok")
    # print(data)
    data.to_csv(file_path, index=False)
    return "小数定标标准化已完成"


# 等宽离散
def data_cut(user_name, file_name, field_list, class_bins, class_label=None):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    data = pd.read_csv(file_path)
    # print(data)
    print("等宽离散")
    # bins = [0, 10, 18, 30, 60, 100]  # 自定义区间
    new_labels = []
    for item in field_list:
        if (class_label is None) or (len(class_label) == 0):
            if len(class_bins) == 1:
                data[item] = pd.cut(data[item], int(class_bins[0]), labels=range(int(class_bins[0])))
            else:
                data[item] = pd.cut(data[item], class_bins, labels=range(len(class_bins)-1))
        else:
            if len(class_bins) == 1:
                data[item] = pd.cut(data[item], int(class_bins[0]), labels=class_label)
            else:
                data[item] = pd.cut(data[item], class_bins, labels=class_label)
    # print(data)
    data.to_csv(file_path, index=False)
    return "等宽离散已完成"


# 等频离散
def data_qcut(user_name, file_name, field_list, class_bins, class_label=None):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    data = pd.read_csv(file_path)
    # print(data)
    print("等频离散")
    # print(class_label)
    # bins = [0, 10, 18, 30, 60, 100]  # 自定义区间
    new_labels = []
    for item in field_list:
        if (class_label is None) or (len(class_label) == 0):
            if len(class_bins) == 1:
                data[item] = pd.qcut(data[item], int(class_bins[0]), labels=range(int(class_bins[0])))
            else:
                data[item] = pd.qcut(data[item], class_bins, labels=range(len(class_bins) - 1))
        else:
            if len(class_bins) == 1:
                data[item] = pd.qcut(data[item], int(class_bins[0]), labels=class_label)
            else:
                data[item] = pd.qcut(data[item], class_bins, labels=class_label)
    # print(data)
    data.to_csv(file_path, index=False)
    return "等频离散已完成"


def drop_data(user_name, file_name, drop_flag, fields_list=None):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    data = pd.read_csv(file_path)
    # print(data)
    if drop_flag == "1":
        print(fields_list)
        data.drop(fields_list, axis=1, inplace=True)
        # print(data)
        data.to_csv(file_path, index=False)
        return "已删除所选列"
    else:
        pass


def data_split(user_name, file_name, new_file_name, field_list):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    new_file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, new_file_name)
    data = pd.read_csv(file_path)
    # print(data)
    if os.path.exists(new_file_path):
        return "文件名已存在"
    else:
        data[field_list].to_csv(new_file_path, index=False)
        if os.path.exists(new_file_path):
            add_file_to_process_platform(user_name, new_file_name)
            return "文件保存成功"


def modify_data(user_name, file_name, modify_ans):
    file_path = "../Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    i = 0
    ans = []
    # print(type(modify_ans))
    while i < len(modify_ans):
        item = json.loads(modify_ans[i])
        ans.append(item)
        i += 1
    data = pd.DataFrame(ans)
    data.to_csv(file_path, index=False)
    # print(data)
    return "保存成功"


if __name__ == "__main__":
    name = "biter"
    f_list = ["demo1", "demo2", "train"]
    f_name = "股票数据(含缺失值)"
    method = "col"
    flag = "1"
    fields = ["上市股票数目(只)", "A股股票数目(只)"]
    d_flag = "1"
    fill_v = 2
    bins = [3]
    # labels = ["l1", "l2", "l3", "l4"]
    labels = []
    data_qcut(name, f_name, fields, bins, labels)
    # print(ans)
