'''
    爬取豆瓣电影Top250的基本信息
    *使用多线程进行爬取
'''

import time
import requests
import threading
from bs4 import BeautifulSoup
from utils.headers import random_user_agent
from utils.saveData import save_to_csv

lock = threading.Lock()

def get_movie_item(item):
    bd_div = item.find("div", class_="bd")  # 获取电影信息的div
    info = bd_div.find("p").text.strip().split("\n")    # 获取电影信息的文本并按换行符切片
    director_actors = info[0].strip().split("\xa0\xa0\xa0") # 导演和主演的信息标签
    year_type_place = info[1].strip().split("\xa0/\xa0")    # 上映日期、制片国家或地区、类型的信息标签

    return {
        "排名": int(item.find("em").text),
        "电影名": item.find("span", class_="title").text,
        "评分": item.find("span", class_="rating_num").text,
        "评分人数": item.find("div", class_="star").find_all("span")[-1].text[:-3],
        "评语": item.find("span", class_="inq").text if item.find("span", class_="inq") else "",
        "导演": director_actors[0].replace("导演: ", "").strip(),
        "主演": director_actors[1].replace("主演: ", "").strip() if len(director_actors) > 1 else "",
        "上映日期": year_type_place[0].strip()[:4],
        "制片国家或地区": year_type_place[1].strip(),
        "类型": year_type_place[2].strip(),
        "海报": item.find("img").get("src"),
        "链接": item.find("a").get("href"),
    }

def get_movie_info_worker(start, headers, session, movie_info_list, links_list):
    url = f"https://movie.douban.com/top250?start={start}&filter="
    response = session.get(url, headers=headers, timeout=2)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        movie_items = soup.find_all("div", class_="item")
        for item in movie_items:
            movie_info = get_movie_item(item)
            with lock:
                movie_info_list.append(movie_info)
                links_list.append(movie_info["链接"])
        print(f"已获取第{start//25 + 1}页的基本信息\n")

def get_basic_info():
    movie_info_list = []    # 空列表用于存放电影信息
    links_list = [] # 空列表用于存放电影链接
    start_time = time.time()    # 开始时间

    headers = {"User-Agent": random_user_agent()}   # 随机User-Agent

    session = requests.Session()    # 创建会话对象
    threads = []    # 空列表用于存放线程

    # 创建线程
    for start in range(0, 25, 25):
        t = threading.Thread(target=get_movie_info_worker, args=(start, headers, session, movie_info_list, links_list))   # 创建线程
        t.start()   # 启动线程
        threads.append(t)   # 添加线程到列表
        time.sleep(1)   # 休眠1秒

    for t in threads:   # 遍历线程列表
        t.join()    # 等待线程结束

    movie_data = sorted(movie_info_list, key=lambda x: x['排名'])   # 按照排名对电影信息列表进行排序

    end_time = time.time()  # 结束时间
    total_time = end_time - start_time  # 总用时
    print(f"电影基本信息爬取完毕，用时：{total_time:0.2f} 秒\n")

    file_name = 'basic_data.csv'
    csv_headers = ['排名', '电影名', '评分', '评分人数', '评语', '导演', '主演', '上映日期', '制片国家或地区', '类型', '海报', '链接']
    file_path = save_to_csv(csv_headers, movie_data, file_name)

    return links_list, total_time, file_path