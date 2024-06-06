'''
    获取文件夹路径
'''

import os

def get_file_path(path_name):
    # 获取当前文件所在的目录
    current_dir = os.path.dirname(__file__)

    # 获取项目根目录
    project_dir = os.path.dirname(current_dir)

    # 拼接文件夹路径
    file_folder_path = os.path.join(project_dir, path_name)

    # 如果文件夹不存在，则创建文件夹
    if not os.path.exists(file_folder_path):
        os.makedirs(file_folder_path)

    # 返回文件夹路径
    return file_folder_path