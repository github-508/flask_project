import re

from flask import Flask, request, session
from flask_cors import *
import os
import numpy as np
import json
import pandas as pd
import User.login as login
import User.register as register
import NewFolder.create_folder as create_folder
import FileEvent.file_event as file_event
import DataStat.data_stat as data_statistics
import AutoGluon.model_event as model_event
import DataVisual.data_visual as data_visual
import DataBaseConnection.database_connection as db_conn
import DataProcess.data_process as data_process
import Report.report_event as report_event


app = Flask(__name__)
CORS(app, supports_credentials=True)
# app.secret_key = "123654qwerty"


@app.route('/')
def hello():
    return "hello word!"


@app.route('/api/login', methods=['POST', 'GET'])
def login_check():
    if request.method == 'GET':
        # get
        user_name = request.args.get('name')
        user_password = request.args.get('password')
        # session['Name'] = "biter"

        # post
        # user_name = request.get_json()['name']
    # user_name = "bite"
    # user_password = "bite"
    res = login.login_check(user_name, user_password)
    return res


@app.route('/api/logout', methods=['POST', 'GET'])
def logout():
    if request.method == 'GET':
        # get
        user_name = request.args.get('name')
        # user_password = request.args.get('password')
        # session['Name'] = "biter"

        # post
        # user_name = request.get_json()['name']
    # user_name = "bite"
    # user_password = "bite"
    res = login.logout(user_name)
    return res


@app.route('/api/register', methods=['POST', 'GET'])
def user_register():
    if request.method == 'GET':
        user_name = request.args.get('name')
        user_password = request.args.get('password')
        user_mail = request.args.get('mail')
    res = register.register(user_name, user_password, user_mail)
    if res == "1":
        create_folder.user_dir(user_name)
    return res


# 上传xlsx,.csv文件
@app.route('/api/upload', methods=['POST', 'GET'])
def file_upload():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        user_name = request.form['name']
        # upload_path = "/home/wmy/Desktop/Resource/{}/datasrc/{}".format(user_name, files.filename)
        # files.save(upload_path)
        for f in files:
            upload_path = "/home/wmy/Desktop/Resource/{}/datasrc/{}".format(user_name, f.filename)
            if os.path.exists(upload_path):
                return "文件已存在"
            if not os.path.exists(upload_path):
                f.save(upload_path)
                if os.path.exists(upload_path):
                    file_event.xlsx_csv_db(user_name, f.filename)
    return "文件上传成功"


# 获取文件列表
@app.route('/api/getFileName', methods=['POST', 'GET'])
def get_file_name():
    if request.method == 'GET':
        user_name = request.args.get("name")
    res = file_event.xlsx_csv_file_name(user_name)
    return res


# 删除文件
@app.route('/api/delFile', methods=['POST', 'GET'])
def del_xlsx_csv_file():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("file_name")
    file_path = "/home/wmy/Desktop/Resource/{}/datasrc/{}".format(user_name, file_name)
    os.remove(file_path)
    if not os.path.exists(file_path):
        file_event.del_xlsx_csv_file(user_name, file_name)
    return "文件已删除"


@app.route('/api/delFromWorkSheet', methods=['POST', 'GET'])
def del_from_worksheet():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("file_name")
    file_path = "/home/wmy/Desktop/Resource/{}/worksheet/{}.csv".format(user_name, file_name)
    os.remove(file_path)
    if not os.path.exists(file_path):
        file_event.del_from_worksheet(user_name, file_name)
    return "文件已删除"


@app.route('/api/delFromProcessPlatform', methods=['POST', 'GET'])
def del_from_process_platform():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("file_name")
    file_path = "/home/wmy/Desktop/Resource/{}/processplatform/{}.csv".format(user_name, file_name)
    os.remove(file_path)
    if not os.path.exists(file_path):
        file_event.del_from_process_platform(user_name, file_name)
    return "文件已删除"


@app.route('/api/addToWorkSheet', methods=['POST', 'GET'])
def add_file_workspace():
    if request.method == 'POST':
        user_name = request.form['name']
        xlsx_list = request.form.getlist('xlsxList[]')
        ''' x_list = []
        print(user_name)
        for x in xlsx_list:
            print(x.split(".")[0])
        '''
        for f in xlsx_list:
            # print(user_name)
            # print("file " + f)
            if f[-1] == "v" or f[-1] == "s":
                # csv_file_name = f.split(".")[0]
                csv_file_name = f[:-4]
            else:
                csv_file_name = f[:-5]
            # print(csv_file_name)
            file_path_1 = "/home/wmy/Desktop/Resource/{}/datasrc/{}".format(user_name, f)
            file_path_2 = "/home/wmy/Desktop/Resource/{}/worksheet/{}.csv".format(user_name, csv_file_name)
            # print(csv_file_name)
            # print(file_path_2)
            if os.path.exists(file_path_2):
                return csv_file_name + "文件已存在"
            if os.path.exists(file_path_1):
                # print("file exit!")
                if f[-1] == "v":
                    # print("csv")
                    df = pd.read_csv(file_path_1, index_col=0)
                    df.to_csv(file_path_2)
                if (f[-1] == "x") or (f[-1] == "s"):
                    # print("xls")
                    df = pd.read_excel(file_path_1, index_col=0)
                    df.to_csv(file_path_2)
            if os.path.exists(file_path_2):
                # print("add success")
                file_event.add_file_to_worksheet(user_name, csv_file_name)
    return "已添加到工作表"


@app.route('/api/getConnectName', methods=['POST', 'GET'])
def get_connection_list():
    if request.method == 'GET':
        user_name = request.args.get("name")
    res = db_conn.get_connection_list(user_name)
    return res


@app.route('/api/createConnection', methods=['POST', 'GET'])
def create_connection():
    if request.method == 'POST':
        user_name = request.form['name']
        con_name = request.form['connName']
        host_name = request.form['hostName']
        port_num = request.form['portNumber']
        db_user = request.form['databaseUserName']
        db_password = request.form['databaseUserPassword']
        db_name = request.form['databaseName']
        db_type = request.form['databaseType']
        port_num = int(port_num)
    res = db_conn.create_connection(user_name, con_name, host_name, port_num, db_user, db_password, db_name, db_type)
    return res


@app.route('/api/delConnection', methods=['POST', 'GET'])
def delete_connection():
    if request.method == 'GET':
        user_name = request.args.get("name")
        con_name = request.args.get("con_name")
    res = db_conn.delete_connection(user_name, con_name)
    return res


@app.route('/api/getDatabaseTableList', methods=['POST', 'GET'])
def get_table_from_db():
    if request.method == 'GET':
        user_name = request.args.get("name")
        con_name = request.args.get("databaseConnection")
    res = db_conn.get_table_from_db(user_name, con_name)
    return res


@app.route('/api/getMeasurementsList', methods=['POST', 'GET'])
def get_measurements_from_db():
    if request.method == 'GET':
        user_name = request.args.get("name")
        con_name = request.args.get("databaseConnection")
    res = db_conn.get_measurements_from_db(user_name, con_name)
    return res


@app.route('/api/getTablesFields', methods=['POST', 'GET'])
def get_fields_from_tables():
    if request.method == 'POST':
        user_name = request.form['name']
        con_name = request.form['databaseConnection']
        table_list = request.form.getlist('tableList[]')
    res = db_conn.get_fields_from_tables(user_name, con_name, table_list)
    return res


@app.route('/api/getMeasurementsFields', methods=['POST', 'GET'])
def get_fields_from_measurements():
    if request.method == 'POST':
        user_name = request.form['name']
        con_name = request.form['databaseConnection']
        measurement_list = request.form.getlist('measurementList[]')
    res = db_conn.get_fields_from_measurements(user_name, con_name, measurement_list)
    # print(user_name)
    # print(con_name)
    # print(measurement_list)
    # print(res)
    return res


@app.route('/api/tablesToFile', methods=['POST', 'GET'])
def tables_to_file():
    if request.method == 'POST':
        user_name = request.form['name']
        con_name = request.form['databaseConnection']
        table_field = request.form['tables_fields']
        f_name = request.form['file_name']
        meth = request.form['method']
        table_field = json.loads(table_field)
        print(table_field)
    res = db_conn.tables_to_file(user_name, con_name, table_field, f_name, meth)
    return res


@app.route('/api/measurementsToFile', methods=['POST', 'GET'])
def measurements_to_file():
    if request.method == 'POST':
        user_name = request.form['name']
        con_name = request.form['databaseConnection']
        measurements_fields = request.form['measurements_fields']
        f_name = request.form['file_name']
        # meth = request.form['method']
        measurements_fields = json.loads(measurements_fields)
        record_cnt = request.form['record_cnt']
        record_cnt = int(record_cnt)
        # print(user_name)
        # print(con_name)
        # print(f_name)
        # print(measurements_fields)
    res = db_conn.measurements_to_file(user_name, con_name, measurements_fields, f_name, record_cnt)
    return res


@app.route('/api/getMeasurementRecordCnt', methods=['POST', 'GET'])
def get_measurement_record_cnt():
    if request.method == 'POST':
        user_name = request.form['name']
        con_name = request.form['databaseConnection']
        measurements_fields = request.form['measurements_fields']
        # f_name = request.form['file_name']
        # meth = request.form['method']
        measurements_fields = json.loads(measurements_fields)
        # print(user_name)
        # print(con_name)
        # print(f_name)
        # print(measurements_fields)
    res = db_conn.get_measurement_record_cnt(user_name, con_name, measurements_fields)
    return res


@app.route('/api/addToProcessPlatform', methods=['POST', 'GET'])
def add_file_process_platform():
    if request.method == 'POST':
        user_name = request.form['name']
        csv_list = request.form.getlist('csvList[]')
        ''' x_list = []
        print(user_name)
        for x in xlsx_list:
            print(x.split(".")[0])
        '''
        for f in csv_list:
            # print(user_name)
            # print("file " + f)
            # csv_file_name = f.split(".")[0]
            # print(f)
            file_path_1 = "/home/wmy/Desktop/Resource/{}/worksheet/{}.csv".format(user_name, f)
            file_path_2 = "/home/wmy/Desktop/Resource/{}/processplatform/{}.csv".format(user_name, f)
            # print(file_path_2)
            if os.path.exists(file_path_2):
                return f + "文件已存在"
            if os.path.exists(file_path_1):
                print("file exit!")
                df = pd.read_csv(file_path_1, index_col=0)
                df.to_csv(file_path_2)
            if os.path.exists(file_path_2):
                print("add success")
                file_event.add_file_to_process_platform(user_name, f)
    return "添加成功"


@app.route('/api/getCsvFileName', methods=['POST', 'GET'])
def get_csv_file_name():
    if request.method == 'GET':
        user_name = request.args.get("name")
    res = file_event.csv_file_name(user_name)
    return res


@app.route('/api/getProcessFileName', methods=['POST', 'GET'])
def get_file_name_process():
    if request.method == 'GET':
        user_name = request.args.get("name")
    res = file_event.get_file_name_process(user_name)
    return res


@app.route('/api/loadWorkSheetFile', methods=['POST', 'GET'])
def load_worksheet_file():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("file_name")
        res = file_event.load_worksheet_file(user_name, file_name)
        return res


@app.route('/api/loadProcessPlatformFile', methods=['POST', 'GET'])
def load_process_platform_file():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("file_name")
        res = file_event.load_process_platform_file(user_name, file_name)
        return res


@app.route('/api/tabularMerge', methods=['POST', 'GET'])
def data_merge():
    if request.method == 'POST':
        user_name = request.form['name']
        new_file_name = request.form['file_name']
        tabular_list = request.form.getlist('tabularList[]')
        meth = request.form['method']
    # print(user_name)
    # print(new_file_name)
    # print(tabular_list)
    # print(meth)
    res = data_process.data_merge(user_name, tabular_list, new_file_name, meth)
    return res


@app.route('/api/nanProcess', methods=['POST', 'GET'])
def nan_process():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        meth = request.form['process_meth']
        flag = request.form['process_flag']
        field_list = request.form.getlist('field_list[]')
        fill_value = ""
        if meth == "fill":
            if flag == "0" or flag == "6":
                fill_value = request.form['fill_value']
    res = data_process.nan_process(user_name, file_name, meth, flag, field_list, fill_value)
    return res


@app.route('/api/duplicateProcess', methods=['POST', 'GET'])
def duplicate_process():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        duplicate_axis = request.form['duplicate_axis']
        flag = request.form['process_flag']
        field_list = request.form.getlist('field_list[]')
    res = data_process.duplicate_process(user_name, file_name, duplicate_axis, flag, field_list)
    return res


@app.route('/api/minMaxScale', methods=['POST', 'GET'])
def min_max_scale():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        field_list = request.form.getlist('field_list[]')
    res = data_process.min_max_scale(user_name, file_name, field_list)
    return res


@app.route('/api/standardScale', methods=['POST', 'GET'])
def standard_scale():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        field_list = request.form.getlist('field_list[]')
    res = data_process.standard_scale(user_name, file_name, field_list)
    return res


@app.route('/api/decimalScale', methods=['POST', 'GET'])
def decimal_scale():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        field_list = request.form.getlist('field_list[]')
    res = data_process.decimal_scale(user_name, file_name, field_list)
    return res


@app.route('/api/dataCut', methods=['POST', 'GET'])
def data_cut():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        field_list = request.form.getlist('field_list[]')
        class_bins = request.form.getlist('class_bins[]')
        class_labels = request.form.getlist('class_labels[]')
        class_bins = [float(i) for i in class_bins]
        if class_labels[0] == '':
            class_labels = []
    res = data_process.data_cut(user_name, file_name, field_list, class_bins, class_labels)
    return res


@app.route('/api/dataQCut', methods=['POST', 'GET'])
def data_qcut():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        field_list = request.form.getlist('field_list[]')
        class_bins = request.form.getlist('class_bins[]')
        class_labels = request.form.getlist('class_labels[]')
        class_bins = [float(i) for i in class_bins]
        if class_labels[0] == '':
            class_labels = []
    res = data_process.data_qcut(user_name, file_name, field_list, class_bins,  class_labels)
    return res


@app.route('/api/predSave', methods=['POST', 'GET'])
def load_model_for_csv():
    if request.method == 'POST':
        user_name = request.form['name']
        model_name = request.form['model_name']
        file_name = request.form['file_name']
        save_flag = request.form['save_flag']
        new_file_name = ""
        if save_flag == "0":
            new_file_name = request.form['new_file_name']
    res = model_event.load_model_for_csv(user_name, model_name, file_name, save_flag, new_file_name)
    return res


@app.route('/api/getModelInfo', methods=['POST', 'GET'])
def get_model_info():
    if request.method == 'POST':
        user_name = request.form['name']
        model_name = request.form['model_name']
    res = model_event.get_model_info(user_name, model_name)
    return res


@app.route('/api/dropData', methods=['POST', 'GET'])
def drop_data():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        drop_flag = request.form['drop_flag']
        field_list = request.form.getlist('field_list[]')
    res = data_process.drop_data(user_name, file_name, drop_flag, field_list)
    return res


@app.route('/api/splitData', methods=['POST', 'GET'])
def split_data():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        new_file_name = request.form['new_file_name']
        field_list = request.form.getlist('field_list[]')
    res = data_process.data_split(user_name, file_name, new_file_name, field_list)
    return res


@app.route('/api/modifyData', methods=['POST', 'GET'])
def modify_data():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        modify_ans = []
        modify_ans = request.form.getlist('modify_data[]')
    res = data_process.modify_data(user_name, file_name, modify_ans)
    return res


@app.route('/api/loadFileForVisual', methods=['POST', 'GET'])
def load_file_visual():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("file_name")
        res = file_event.load_file_visual(user_name, file_name)
        return res


@app.route('/api/getVisualList', methods=['POST', 'GET'])
def get_visual_list():
    if request.method == 'GET':
        user_name = request.args.get("name")
        industry = request.args.get("industry")
        res = data_visual.get_visual_list(user_name, industry)
        return res


@app.route('/api/deleteVisualItem', methods=['POST', 'GET'])
def delete_visual_item():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("visual_file_name")
        res = data_visual.delete_visual_item(user_name, file_name)
        return res


@app.route('/api/saveVisual', methods=['POST', 'GET'])
def save_visual():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['visual_file_name']
        json_ans = request.form['visualAns']  # .getlist('visualAns')
        industry = request.form['industry']
        visual_ans = json.loads(json_ans)
        # print(user_name)
        # print(file_name)
        # print(type(json_ans))
        # print(type(visual_ans))
        # print(visual_ans)
        res = data_visual.save_visual(user_name, file_name, visual_ans, industry)
        return res
        # return "ok"


@app.route('/api/getVisualAns', methods=['POST', 'GET'])
def load_visual_ans():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("visual_file_name")
        res = data_visual.load_visual_ans(user_name, file_name)
        return res


@app.route('/api/loadStatFields', methods=['POST', 'GET'])
def load_stat_fields():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("file_name")
        res = file_event.load_stat_fields(user_name, file_name)
        return res


@app.route('/api/dataStat', methods=['POST', 'GET'])
def data_stat():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        var_list = request.form.getlist('varList[]')
        res = data_statistics.data_stat(user_name, file_name, var_list)
        return res


@app.route('/api/dataStatCar', methods=['POST', 'GET'])
def data_stat_car():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['file_name']
        # var_list = request.form.getlist('varList[]')
        res = data_statistics.data_stat_car()
        return res


@app.route('/api/getStatList', methods=['POST', 'GET'])
def get_stat_list():
    if request.method == 'GET':
        user_name = request.args.get("name")
        industry = request.args.get("industry")
        res = data_statistics.get_stat_list(user_name, industry)
        return res


@app.route('/api/deleteStatItem', methods=['POST', 'GET'])
def delete_stat_item():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("stat_file_name")
        res = data_statistics.delete_stat_item(user_name, file_name)
        return res


@app.route('/api/saveStat', methods=['POST', 'GET'])
def save_stat():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['stat_file_name']
        json_ans = request.form['statAns']  # .getlist('visualAns')
        industry = request.form['industry']
        stat_ans = json.loads(json_ans)
        # print(user_name)
        # print(file_name)
        # print(type(json_ans))
        # print(type(visual_ans))
        # print(visual_ans)
        res = data_statistics.save_stat(user_name, file_name, stat_ans, industry)
        return res
        # return "ok"


@app.route('/api/getStatAns', methods=['POST', 'GET'])
def load_stat_ans():
    if request.method == 'GET':
        user_name = request.args.get("name")
        file_name = request.args.get("stat_file_name")
        res = data_statistics.load_stat_ans(user_name, file_name)
        return res


@app.route('/api/getModelList', methods=['POST', 'GET'])
def model_list():
    if request.method == 'GET':
        user_name = request.args.get("name")
        industry = request.args.get("industry")
        res = model_event.model_list(user_name, industry)
        return res


@app.route('/api/getModelListFitting', methods=['POST', 'GET'])
def model_list_fitting():
    if request.method == 'GET':
        user_name = request.args.get("name")
        industry = request.args.get("industry")
        res = model_event.model_list_fitting(user_name, industry)
        return res


@app.route('/api/deleteModel', methods=['POST', 'GET'])
def delete_model():
    if request.method == 'GET':
        user_name = request.args.get("name")
        model_name = request.args.get("model_name")
        res = model_event.delete_model(user_name, model_name)
        return res


@app.route('/api/generateModel', methods=['POST', 'GET'])
def fit_data():
    if request.method == 'POST':
        user_name = request.form['name']
        train_file = request.form['file_name']
        generate_model_name = request.form['model_name']
        prediction_field = request.form['preField']
        task = request.form['task_type']
        fields = []
        model_desc = request.form['model_desc']
        fields = request.form.getlist('fieldsList[]')
        industry = request.form['industry']
        # print(fields)
        res = model_event.fit_data(user_name, train_file, generate_model_name, industry, prediction_field, \
                                   task, model_desc, fields)
        return res


@app.route('/api/getReportList', methods=['POST', 'GET'])
def get_report_list():
    if request.method == 'GET':
        user_name = request.args.get('name')
        res = report_event.get_report_list(user_name)
        return res


@app.route('/api/deleteReport', methods=['POST', 'GET'])
def delete_report():
    if request.method == 'GET':
        user_name = request.args.get("name")
        report_name = request.args.get("report_name")
        res = report_event.delete_report(user_name, report_name)
        return res


@app.route('/api/loadReport', methods=['POST', 'GET'])
def load_report():
    if request.method == 'GET':
        user_name = request.args.get("name")
        report_name = request.args.get("report_name")
        res = report_event.load_report(user_name, report_name)
        return res


@app.route('/api/saveReport', methods=['POST', 'GET'])
def save_report():
    if request.method == 'POST':
        user_name = request.form['name']
        file_name = request.form['report_name']
        json_ans = request.form['report_ans']  # .getlist('visualAns')
        report_ans = json.loads(json_ans)
        # print(user_name)
        # print(file_name)
        # print(type(json_ans))
        # print(type(visual_ans))
        # print(visual_ans)
        res = report_event.save_report(user_name, file_name, report_ans)
        print(res)
        return res
        # return "ok"


@app.route('/api/generateReport', methods=['POST', 'GET'])
def generate_report():
    if request.method == 'POST':
        user_name = request.form['name']
        visual_list = request.form.getlist('visual_list[]')
        stat_list = request.form.getlist('stat_list[]')
        res = report_event.generate_report(user_name, visual_list, stat_list)
        return res


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
