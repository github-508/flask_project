import os, sys


def user_dir(user_name):
    dir_path_datasrc = "/home/wmy/Desktop/Resource/{}/datasrc".format(user_name)
    dir_path_worhsheet = "/home/wmy/Desktop/Resource/{}/worksheet".format(user_name)
    dir_path_processplatform = "/home/wmy/Desktop/Resource/{}/processplatform".format(user_name)
    dir_path_visual = "/home/wmy/Desktop/Resource/{}/visual".format(user_name)
    dir_path_statistics = "/home/wmy/Desktop/Resource/{}/statistics".format(user_name)
    dir_path_model = "/home/wmy/Desktop/Resource/{}/model".format(user_name)
    dir_path_report = "/home/wmy/Desktop/Resource/{}/report".format(user_name)

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

