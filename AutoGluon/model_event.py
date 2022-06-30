import pandas as pd
import numpy as np
import datetime
import time
import json
import pymysql
import os
from shutil import rmtree
from autogluon.tabular import TabularDataset, TabularPredictor


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


def dataset_split(data):
    data: pd.DataFrame = data.sample(frac=1.0)
    rows, cols = data.shape
    # train_set_cnt = int(rows * 0.8)
    split_point = int(rows * 0.2)
    data_test: pd.DataFrame = data.iloc[0: split_point, :].reset_index(drop=True)
    data_train: pd.DataFrame = data.iloc[split_point: rows, :].reset_index(drop=True)
    return data_train, data_test


def fit_data(user_name, train_file, generate_model_name, industry, prediction_field, task_type, model_desc=None, features_list=None):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str_before_finish = "insert into model(u_id,model_name,status,industry) values (\'{}\',\'{}\',0, \'{}\')".\
        format(user_name, generate_model_name, industry)
    sql_str_delete = "delete from model where u_id = \'{}\' and model_name = \'{}\'".format(user_name, generate_model_name)

    train_file_path = "/home/wmy/Desktop/Resource/{}/processplatform/{}.csv".format(user_name, train_file)
    save_path = "/home/wmy/Desktop/Resource/{}/model/{}".format(user_name, generate_model_name)
    dataset_name = "{}.csv".format(train_file)
    dataset_size = ""
    data_split_str = ""
    metric = ""
    predict_type = ""
    if os.path.exists(save_path):
        return "模型已存在，请重新输入模型名"
    else:
        try:
            cursor.execute(sql_str_before_finish)
            conn.commit()
        except:
            conn.rollback()
        print("模型生成中...")
        label = prediction_field
        data = TabularDataset(train_file_path)
        train_data, test_data = dataset_split(data)
        dataset_size = "共{}行{}列".format(data.shape[0], data.shape[1])
        data_split_str = "训练集共{}行, 测试集共{}行".format(train_data.shape[0], test_data.shape[0])
        eval_str = ""
        if task_type == "regression":
            metric = "r2"
        else:
            metric = "accuracy"
        if len(features_list) == 0:
            predictor = TabularPredictor(label=label, problem_type=task_type, path=save_path).fit(train_data)
            current_time = datetime.datetime.now()
            model_time = datetime.datetime.strftime(current_time, '%Y-%m-%d %H:%M:%S')
            y_test = test_data[label]
            y_pred = predictor.predict(test_data.drop(columns=[label]))
            perf = predictor.evaluate_predictions(y_true=y_test, y_pred=y_pred, auxiliary_metrics=True)
            fit_fields = ','.join(train_data.columns.tolist())
            if task_type == "regression":
                eval_str = "R2(决定系数) = " + f'{perf["r2"]}'
                predict_type = "回归"
                # print("R2:" + f'{perf["r2"]}')
            if (task_type == "binary") or (task_type == "multiclass"):
                eval_str = "Accuracy(准确率) = " + f'{perf["accuracy"]}'
                predict_type = "分类"
                # print("Accuracy:" + f'{perf["accuracy"]}')
        else:
            df = train_data[features_list]
            # print(df)
            predictor = TabularPredictor(label=label, problem_type=task_type, path=save_path).fit(df)
            current_time = datetime.datetime.now()
            model_time = datetime.datetime.strftime(current_time, '%Y-%m-%d %H:%M:%S')
            y_test = df[label]
            y_pred = predictor.predict(df.drop(columns=[label]))
            perf = predictor.evaluate_predictions(y_true=y_test, y_pred=y_pred, auxiliary_metrics=True)
            fit_fields = ','.join(df.columns.tolist())
            if task_type == "regression":
                eval_str = "R2(决定系数) = " + f'{perf["r2"]}'
                predict_type = "回归"
            if (task_type == "binary") or (task_type == "multiclass"):
                eval_str = "Accuracy(准确率) = " + f'{perf["accuracy"]}'
                predict_type = "分类"
        if os.path.exists(save_path):
            sql_str_finished = "update model set status = 1, dataset = \'{}\', dataset_size = \'{}\', dataset_split = \'{}\', model_desc = \'{}\', fields = \'{}\', \
                label = \'{}\', task = \'{}\', fit_time = \'{}\', eval_metric = \'{}\' where u_id = \'{}\' and \
                model_name = \'{}\'".format(dataset_name, dataset_size, data_split_str, model_desc, fit_fields, label, predict_type, model_time, \
                eval_str, user_name, generate_model_name)
            try:
                cursor.execute(sql_str_finished)
                conn.commit()
            except:
                conn.rollback()
            cursor.close()
            conn.close()
            print("模型已生成")
            return "模型已生成"
        else:
            try:
                cursor.execute(sql_str_delete)
                conn.commit()
            except:
                conn.rollback()
            cursor.close()
            conn.close()
            print("模型训练失败")
            return "模型训练失败"


def delete_model(user_name, delete_model_name):
    model_path = "/home/wmy/Desktop/Resource/{}/model/{}".format(user_name, delete_model_name)
    # print(delete_model_name)
    sql_str_delete = "delete from model where u_id = \'{}\' and model_name = \'{}\'".format(user_name,delete_model_name)
    if not os.path.exists(model_path):
        return "模型不存在"
    else:
        # os.removedirs(model_path)
        rmtree(model_path)
        if not os.path.exists(model_path):
            conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
            cursor = conn.cursor()
            try:
                cursor.execute(sql_str_delete)
                conn.commit()
            except:
                conn.rollback()
            cursor.close()
            conn.close()
            return "模型已删除"


def load_model_for_csv(user_name, load_model_name, test_file, save_flag, new_file_name=None):
    model_path = "/home/wmy/Desktop/Resource/{}/model/{}".format(user_name, load_model_name)
    test_file_path = "/home/wmy/Desktop/Resource/{}/processplatform/{}.csv".format(user_name, test_file)
    if not os.path.exists(model_path):
        return "模型不存在"
    if not os.path.exists(test_file_path):
        return "测试csv文件不存在"
    test_data = TabularDataset(test_file_path)
    print(test_data)
    predictor = TabularPredictor.load(model_path)
    pred = predictor.predict(test_data)
    # pred = predictor.predict(test_data.drop(columns=['Id', 'Name']))
    print(pred)

    # 保存到新文件
    if save_flag == "0":
        new_file_path = "/home/wmy/Desktop/Resource/{}/processplatform/{}.csv".format(user_name, new_file_name)
        if os.path.exists(new_file_path):
            return "文件名已存在"
        else:
            pred.to_csv(new_file_path, index=False)
            if os.path.exists(new_file_path):
                add_file_to_process_platform(user_name, new_file_name)
                return "保存成功"
    if save_flag == "1":
        # specified_file_path = "/home/wmy/Desktop/Resource/{}/processplatform/{}.csv".format(user_name, specified_file_name)
        df = pd.read_csv(test_file_path)
        df[f'{pred.name}(Prediction)'] = pred
        print(df)
        df.to_csv(test_file_path, index=False)
        return "保存成功"


def get_model_info(user_name, model):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select dataset,dataset_size,dataset_split,model_desc,fields,label,task,fit_time,eval_metric from model \
    where u_id = \'{}\' and model_name = \'{}\' and status = 1".format(user_name, model)
    cursor.execute(sql_str)
    res = cursor.fetchone()
    ans = {}
    ans['dataset'] = res[0]
    ans['dataset_size'] = res[1]
    ans['dataset_split'] = res[2]
    ans['model_desc'] = res[3]
    ans['fields'] = res[4]
    ans['label'] = res[5]
    ans['task'] = res[6]
    ans['fit_time'] = res[7]
    ans['eval_metric'] = res[8]
    # print(ans)
    return json.dumps(ans)


def model_list(user_name, industry):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select model_name from model where u_id = \'{}\' and status = 1 and industry = \'{}\'".\
        format(user_name, industry)
    cursor.execute(sql_str)
    res = cursor.fetchall()
    model_list = []
    for row in res:
        model_list.append(row[0])
    cursor.close()
    conn.close()
    # print(model_list)
    return json.dumps(model_list)


def model_list_fitting(user_name, industry):
    conn = pymysql.connect(host='localhost', user="root", passwd="root", db="data_anl")
    cursor = conn.cursor()
    sql_str = "select model_name from model where u_id = \'{}\' and status = 0 and industry = \'{}\'".\
        format(user_name, industry)
    cursor.execute(sql_str)
    res = cursor.fetchall()
    model_list = []
    for row in res:
        model_list.append(row[0])
    cursor.close()
    conn.close()
    # print(model_list)
    return json.dumps(model_list)


if __name__ == "__main__":
    name = "biter"
    train_file_name = "train"
    model_name = "model_regression_3"
    pre_field = "Credit"
    task = "regression"
    # task = "binary"
    # task = "multiclass"
    test_file_name = "test"
    model_desc = "model......"
    features = ["年份","上市股票数目(只)","A股股票数目(只)","B股股票数目(只)","A股发行股本(亿股)","B股发行股本(亿股)"]
    # ans = fit_data(name, train_file_name, model_name, pre_field, task, model_desc, features)
    # print(ans)
    # ans = load_model_for_csv(name, model_name, test_file_name, save_flag="1")
    # print(ans)


