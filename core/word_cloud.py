'''
    词云图生成
'''

import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
from utils.getPath import get_file_path

# 数据处理
def generate_wordcloud_from_column(column_name, title): # 定义 generate_wordcloud_from_column 函数，接收两个参数：列名，标题
    column_data = df[column_name] # 获取指定列的数据
    if column_name in ['制片国家或地区', '语言']: # 判断列名是否为制片国家或地区或类型
        text_data = ' / '.join(column_data.dropna().astype(str).values) # 将数据以' / '切片，并合并成一个字符串
    else:
        text_data = ', '.join(column_data.dropna().astype(str).values) # 将数据以逗号切片，并合并成一个字符串
    generate_wordcloud(column_name, text_data, title, font_path) # 调用 generate_wordcloud 函数生成词云图

# 生成词云图
def generate_wordcloud(column_name, text_data, title, font_path):
    if column_name in ['制片国家或地区', '语言']:
        counter = Counter(text_data.split(' / ')) # 使用 Counter 计算每个词的出现次数
    else:
        counter = Counter(text_data.split(', ')) # 使用 Counter 计算每个词的出现次数
    wordcloud = WordCloud(scale=10, font_path=font_path, background_color='white').generate_from_frequencies(counter) # 生成词云

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 设置中文字体

    plt.figure(num='词云', figsize=(15, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')

    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.show()

# 获取文件路径
data_file_path = get_file_path('data') + '/details_info.csv'

# 读取 CSV 文件
df = pd.read_csv(data_file_path, encoding='utf-8')

# 指定字体文件路径
font_path = get_file_path('utils') + '/font.ttf'
