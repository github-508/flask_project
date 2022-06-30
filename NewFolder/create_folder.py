import os, sys


def user_dir(user_name):
    dir_path_datasrc = "../Resource/{}/datasrc".format(user_name)
    dir_path_worhsheet = "../Resource/{}/worksheet".format(user_name)
    dir_path_processplatform = "../Resource/{}/processplatform".format(user_name)
    dir_path_visual = "../Resource/{}/visual".format(user_name)
    dir_path_statistics = "../Resource/{}/statistics".format(user_name)
    dir_path_model = "../Resource/{}/model".format(user_name)
    dir_path_report = "../Resource/{}/report".format(user_name)

    # os.mkdir(dir_path);
    os.makedirs(dir_path_datasrc)
    os.makedirs(dir_path_worhsheet)
    os.makedirs(dir_path_processplatform)
    os.makedirs(dir_path_visual)
    os.makedirs(dir_path_statistics)
    os.makedirs(dir_path_model)
    os.makedirs(dir_path_report)


if __name__ == '__main__':
    name = "biter"
    user_dir(name)

