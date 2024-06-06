'''
    用于将爬取到的电影信息保存至 CSV 文件中
'''
import os
import csv
from utils.getPath import get_file_path

def save_to_csv(csv_headers, movie_data, file_name): # 定义 save_to_csv 函数，接收三个参数：文件头，电影信息列表，文件名

    # 按照排名对电影信息列表进行排序
    sorted_movie_info_list = sorted(movie_data, key=lambda x: x['排名'])

    # 获取文件夹路径
    folder_path = get_file_path('data')

    # 如果文件夹不存在，则创建文件夹
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 拼接文件路径
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=csv_headers)
        writer.writeheader()
        for data in sorted_movie_info_list:
            writer.writerow(data)

    print(f"结果已保存至 {file_path}\n")
    return file_path
