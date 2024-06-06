'''
    电影详情数据爬取模块
    1. 从基本信息中获取电影链接
    2. 解析电影详情信息
    3. 保存电影详情信息到CSV文件
    4. 返回总用时和文件路径
    *使用代理池进行爬取
    *使用多线程进行爬取容易被封IP
'''

import json
import re
import time
import requests
from bs4 import BeautifulSoup
from core.basic_spider import get_basic_info
from utils.saveData import save_to_csv
from utils.getPath import get_file_path

# 获取电影详情信息
def get_details(Cookie=None):
    movie_data = []     #空列表用于存放电影详情信息

    # 读取代理信息
    proxy_file = get_file_path("data") + '/proxyinfo.json'
    with open(proxy_file, "r") as json_file:
        proxies_list = json.load(json_file)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
        "Referer": "https://movie.douban.com/",
        "Host": "movie.douban.com",
    }

    # 添加Cookie
    if Cookie:
        headers["Cookie"] = Cookie

    session = requests.Session() # 创建会话对象
    start_time = time.time() # 开始时间

    links_list = get_basic_info()[0] # 获取电影基本信息
    get_details_worker(headers, session, proxies_list, movie_data, links_list) # 获取电影详情信息

    # 保存电影详情信息到CSV文件
    file_name = 'details_info.csv'
    csv_headers = "排名 电影名 导演 编剧 主演 类型 制片国家或地区 语言 年份 上映日期 片长 又名 IMDb 评分 评分人数 五星比例 四星比例 三星比例 二星比例 一星比例 简介 海报 链接".split(" ")
    file_path = save_to_csv(csv_headers, movie_data, file_name)

    end_time = time.time() # 结束时间
    total_time = end_time - start_time # 总用时
    print(f"电影详情信息已爬取完毕，用时：{total_time:0.2f} 秒\n")
    return total_time, file_path

# 获取电影详情信息工作函数
def get_details_worker(headers, session, proxies_list, movie_data, links_list):

    current_proxy_index = 0 # 当前代理索引

    # 遍历电影链接
    while True:
        proxy = proxies_list[current_proxy_index] # 获取当前代理
        if proxy["type"].lower() == "http":
            proxies = {"http": f"http://{proxy['host']}:{proxy['port']}"}
        else:
            proxies = {"https": f"https://{proxy['host']}:{proxy['port']}"}

        try:
            for link in links_list:
                try:
                    response = session.get(link, headers=headers, proxies=proxies, timeout=3)
                    if response.url.startswith("https://sec.douban.com"):  # 检查是否被重定向到sec.douban.com
                        print("被重定向到sec.douban.com，跳过当前代理")
                        current_proxy_index += 1
                        time.sleep(2)
                        continue
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "lxml")

                        top250_no_span = soup.find('span', class_='top250-no')
                        rank = top250_no_span.text.strip()[3:] if top250_no_span else "无"
                        if rank != '0': print(f"正在解构第{int(rank)}部电影的数据")

                        title = soup.find('span', property='v:itemreviewed').text.strip() if soup.find('span', property='v:itemreviewed') else "无"  # 电影名
                        year = soup.find('span', class_='year').text.strip('()') if soup.find('span', class_='year') else "无"  # 年份
                        directors = ', '.join([director.string for director in soup.find_all(attrs={"rel": "v:directedBy"})]) if soup.find_all(attrs={"rel": "v:directedBy"}) else "无"  # 导演
                        writer_span = soup.find('span', string='编剧')  # 编剧标签
                        writers = ', '.join([a.text for a in writer_span.find_next_sibling('span').find_all('a')]) if writer_span else "无" # 编剧
                        actors = ', '.join([actor.string for actor in soup.find_all(attrs={"rel": "v:starring"})]) if soup.find_all(attrs={"rel": "v:starring"}) else "无"  # 主演
                        genres = ', '.join([genre.string for genre in soup.find_all('span', property='v:genre')]) if soup.find_all('span', property='v:genre') else "无"    # 类型
                        palce = soup.find('span', string=re.compile('制片国家/地区:')).next_sibling.strip() if soup.find('span', string=re.compile('制片国家/地区:')) else "无" # 制片国家或地区
                        language = soup.find('span', string=re.compile('语言:')).next_sibling.strip() if soup.find('span', string=re.compile('语言:')) else "无"    # 语言
                        release_date = ', '.join([date.string for date in soup.find_all('span', property='v:initialReleaseDate')]) if soup.find_all('span', property='v:initialReleaseDate') else "无"  # 上映日期
                        runtime = re.search(r'\d+', soup.find('span', property='v:runtime').text.strip()).group() if soup.find('span', property='v:runtime') else "无"
                        IMDb_tag = soup.find("span", string=re.compile("IMDb:"))    # IMDb标签
                        IMDb = IMDb_tag.next_sibling.strip() if IMDb_tag else "无"  # IMDb

                        rating = soup.find('strong', property='v:average').text.strip() if soup.find('strong', property='v:average') else "无"  # 评分
                        rating_count = soup.find('span', property='v:votes').text.strip() if soup.find('span', property='v:votes') else "无"    # 评分人数
                        star_ratios = soup.find_all('span', class_='rating_per')    # 评分比例
                        five_star_ratio = star_ratios[0].text.strip() if star_ratios else "无"  # 五星比例
                        four_star_ratio = star_ratios[1].text.strip() if len(star_ratios) > 1 else "无" # 四星比例
                        three_star_ratio = star_ratios[2].text.strip() if len(star_ratios) > 2 else "无"    # 三星比例
                        two_star_ratio = star_ratios[3].text.strip() if len(star_ratios) > 3 else "无"  # 二星比例
                        one_star_ratio = star_ratios[4].text.strip() if len(star_ratios) > 4 else "无"  # 一星比例

                        summary = soup.find('span', property='v:summary').text.split('<br>', 1)[0].strip() if soup.find('span', property='v:summary') else "无" # 简介
                        poster = soup.find('img', rel='v:image').get('src') if soup.find('img', rel='v:image') else "无"    # 海报
                        another_name_tag = soup.find('span', string=re.compile('又名:'))    # 又名标签
                        another_name = another_name_tag.next_sibling.strip() if another_name_tag else "无"  # 又名

                        movie_data.append({
                            "排名": int(rank),
                            "电影名": title,
                            "导演": directors,
                            "编剧": writers,
                            "主演": actors,
                            "类型": genres,
                            "制片国家或地区": palce,
                            "语言": language,
                            "年份": year,
                            "上映日期": release_date,
                            "片长": runtime,
                            "又名": another_name,
                            "IMDb": IMDb,
                            "评分": rating,
                            "评分人数": rating_count,
                            "五星比例": five_star_ratio,
                            "四星比例": four_star_ratio,
                            "三星比例": three_star_ratio,
                            "二星比例": two_star_ratio,
                            "一星比例": one_star_ratio,
                            "简介": summary,
                            "海报": poster,
                            "链接": link
                        })
                        time.sleep(2)
                        continue
                except Exception as e:
                    print(f"Error occurred while processing link {link}: {e}")
                    time.sleep(2)
                    current_proxy_index += 1
                    continue
            break
        except requests.exceptions.RequestException:
            print("请求失败，正在尝试下一个代理...\n")
            current_proxy_index += 1
            time.sleep(2)
            continue