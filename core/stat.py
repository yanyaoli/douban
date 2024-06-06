'''
    基础统计分析模块
    1. 热榜信息分析
    2. 排行榜信息分析
    3. 可视化热榜信息
    4. 可视化排行榜信息
'''

import pandas as pd
import matplotlib.pyplot as plt
from utils.getPath import get_file_path

# 热榜信息分析
def get_hot_list_info():
    data_file = get_file_path('data') + '/details_info.csv' # 获取详情信息文件路径
    df = pd.read_csv(data_file, encoding='utf-8')

    directors_count = {} # 定义导演计数字典
    writers_count = {} # 定义编剧计数字典
    actors_count = {} # 定义主演计数字典
    genres_count = {} # 定义类型计数字典
    place_count = {} # 定义地区计数字典
    languages_count = {} # 定义语言计数字典
    years_count = {} # 定义年份计数字典
    rating_count = {} # 定义评分计数字典

    for row in df.itertuples(): # 遍历数据
        directors = row.导演.split(', ') # 以逗号切片导演数据
        writers = row.编剧.split(', ') # 以逗号切片编剧数据
        actors = row.主演.split(', ') # 以逗号切片主演数据
        genres = row.类型.split(', ') # 以逗号切片类型数据
        places = row.制片国家或地区.split(' / ') # 以' / '切片地区数据
        languages = row.语言.split(' / ') # 以' / '切片语言数据
        year = str(row.年份) # 获取年份数据
        rating = str(row.评分) # 获取评分数据

        for director in directors: # 遍历导演数据
            directors_count[director] = directors_count.get(director, 0) + 1 # 统计导演出现次数

        for writer in writers: # 遍历编剧数据
            writers_count[writer] = writers_count.get(writer, 0) + 1 # 统计编剧出现次数

        for actor in actors: # 遍历主演数据
            actors_count[actor] = actors_count.get(actor, 0) + 1 # 统计主演出现次数

        for genre in genres: # 遍历类型数据
            genres_count[genre] = genres_count.get(genre, 0) + 1 # 统计类型出现次数

        for place in places: # 遍历地区数据
            place_count[place] = place_count.get(place, 0) + 1 # 统计地区出现次数

        for language in languages: # 遍历语言数据
            languages_count[language] = languages_count.get(language, 0) + 1 # 统计语言出现次数

        years_count[year] = years_count.get(year, 0) + 1 # 统计年份出现次数

        rating_count[rating] = rating_count.get(rating, 0) + 1 # 统计评分出现次数


    # 获取前十名导演、编剧、主演、类型、地区、语言、年份和评分
    top_directors = dict(sorted(directors_count.items(), key=lambda item: item[1], reverse=True)[:10]) # 获取前十名导演
    top_writers = dict(sorted(writers_count.items(), key=lambda item: item[1], reverse=True)[:10]) # 获取前十名编剧
    top_actors = dict(sorted(actors_count.items(), key=lambda item: item[1], reverse=True)[:10]) # 获取前十名主演
    top_genres = dict(sorted(genres_count.items(), key=lambda item: item[1], reverse=True)[:10]) # 获取前十名类型
    top_places = dict(sorted(place_count.items(), key=lambda item: item[1], reverse=True)[:10]) # 获取前十名地区
    top_languages = dict(sorted(languages_count.items(), key=lambda item: item[1], reverse=True)[:10]) # 获取前十名语言
    top_years = dict(sorted(years_count.items(), key=lambda item: item[1], reverse=True)[:10]) # 获取前十名年份
    top_ratings = dict(sorted(rating_count.items(), key=lambda item: item[1], reverse=True)[:10]) # 获取前十名评分

    return {
        '导演': top_directors,
        '编剧': top_writers,
        '主演': top_actors,
        '类型': top_genres,
        '地区': top_places,
        '语言': top_languages,
        '年份': top_years,
        '评分': top_ratings
    }

# 热榜可视化
def gui_hot_list(categories):
    plt.figure(num='热榜',figsize=(15, 10)) # 设置标题和图形大小

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 设置中文显示

    for i, (category, items) in enumerate(categories.items(), start=1): # 遍历热榜信息
        names = list(items.keys())[::-1] # 获取名称列表
        counts = list(items.values())[::-1] # 获取计数列表

        plt.subplot(2, 4, i) # 设置子图
        plt.barh(names, counts, color='skyblue') # 绘制水平条形图
        plt.xlabel('出现次数') # 设置 x 轴标签
        plt.title(f'{category}热榜前十名') # 设置标题

        for j, count in enumerate(counts): # 遍历计数列表
            plt.text(count, j, f' {count}', va='center') # 添加标签文本

    mng = plt.get_current_fig_manager() # 获取当前图形管理器
    mng.window.state('zoomed') # 最大化显示图形
    plt.subplots_adjust(wspace=0.3, hspace=0.3) # 调整子图间距
    plt.show() # 显示图形

# 热榜入口
def get_hot_list():
    categories = get_hot_list_info()
    for key, value in categories.items():
        print(f"{key}：")
        for k, v in value.items():
            print(f"{k}: {v}")
    gui_hot_list(categories)
    return categories


# 排行榜可视化
def visualize_ranking_list(top_10_by_rating, top_10_by_rating_count, top_10_by_year, top_10_by_five_star_ratio):
    plt.figure(num='排行榜', figsize=(15, 10))

    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    # 绘制按评分排序的前十名电影
    plt.subplot(2, 2, 1)
    movie_names = [name.split(' ')[0] for name in top_10_by_rating['电影名']]
    plt.barh(movie_names[::-1], top_10_by_rating['评分'][::-1], color='skyblue')
    plt.xlabel('评分')
    plt.title('按评分排序的前十名电影')
    for i, score in enumerate(top_10_by_rating['评分'][::-1]):
        plt.text(score, i, f'{score}', va='center')

    # 绘制按评分人数排序的前十名电影
    plt.subplot(2, 2, 2)
    movie_names = [name.split(' ')[0] for name in top_10_by_rating_count['电影名']]
    plt.barh(movie_names[::-1], top_10_by_rating_count['评分人数'][::-1], color='salmon')
    plt.xlabel('评分人数')
    plt.title('按评分人数排序的前十名电影')
    for i, count in enumerate(top_10_by_rating_count['评分人数'][::-1]):
        plt.text(count, i, f'{count}', va='center')

    # 绘制按上映年份排序的前十名电影
    plt.subplot(2, 2, 3)
    movie_names = [name.split(' ')[0] for name in top_10_by_year['电影名']]
    plt.barh(movie_names[::-1], top_10_by_year['年份'][::-1], color='lightgreen')
    plt.xlabel('年份')
    plt.title('按上映年份排序的前十名电影')
    for i, year in enumerate(top_10_by_year['年份'][::-1]):
        plt.text(year, i, f'{year}', va='center')

    # 绘制按五星比例排序的前十名电影
    plt.subplot(2, 2, 4)
    movie_names = [name.split(' ')[0] for name in top_10_by_five_star_ratio['电影名']]
    plt.barh(movie_names[::-1], top_10_by_five_star_ratio['五星比例'][::-1], color='lightgreen')
    plt.xlabel('五星比例')
    plt.title('按五星比例排序的前十名电影')
    for i, ratio in enumerate(top_10_by_five_star_ratio['五星比例'][::-1]):
        plt.text(ratio, i, f'{ratio}', va='center')

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.subplots_adjust(wspace=0.3, hspace=0.3)
    plt.show()

# 排行榜入口
def get_ranking_list():
    data_file = get_file_path('data') + '/details_info.csv'
    df = pd.read_csv(data_file, encoding='utf-8')

    top_10_by_rating = df.sort_values(by='评分', ascending=False).head(10) # 按评分进行排序，取前十名
    top_10_by_rating.index = range(1, 11)  # 调整索引从1开始

    top_10_by_rating_count = df.sort_values(by='评分人数', ascending=False).head(10) # 按评分人数进行排序，取前十名
    top_10_by_rating_count.index = range(1, 11)  # 调整索引从1开始

    top_10_by_year = df.sort_values(by='年份', ascending=False).head(10) # 按上映年份进行排序，取前十名
    top_10_by_year.index = range(1, 11)  # 调整索引从1开始

    top_10_by_five_star_ratio = df.sort_values(by='五星比例', ascending=False).head(10) # 按五星比例进行排序，取前十名
    top_10_by_five_star_ratio.index = range(1,11) # 调整索引从1开始

    print("\n按评分排序的前十名电影详情：")
    for i, row in top_10_by_rating.iterrows():
        print(f"{i}. {row['电影名']}（{row['评分']}）")

    print("\n按评分人数排序的前十名电影详情：")
    for i, row in top_10_by_rating_count.iterrows():
        print(f"{i}. {row['电影名']}（{row['评分人数']}）")

    print("\n按上映年份排序的前十名电影详情：")
    for i, row in top_10_by_year.iterrows():
        print(f"{i}. {row['电影名']}（{row['年份']}）")

    print("\n按五星比例排序的前十名电影详情：")
    for i, row in top_10_by_five_star_ratio.iterrows():
        print(f"{i}. {row['电影名']}（{row['五星比例']}）")
    visualize_ranking_list(top_10_by_rating, top_10_by_rating_count, top_10_by_year, top_10_by_five_star_ratio) # 可视化排行榜
