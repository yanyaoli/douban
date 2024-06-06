'''
    代理池
    1. 从代理池获取代理
    2. 随机代理
'''

import json
import random
import requests
from utils.getPath import get_file_path

# 获取代理池
def get_proxy():
    url = "https://fastly.jsdelivr.net/gh/parserpp/ip_ports@main/proxyinfo.json"    # 代理池地址
    response = requests.get(url)

    proxies = []    # 定义一个空代理列表用于存放代理信息

    # 遍历代理信息
    for line in response.iter_lines(decode_unicode=True):
        if line:
            proxy_data = json.loads(line)
            proxies.append({
                "host": proxy_data["host"],
                "port": proxy_data["port"],
                "type": proxy_data["type"]
            })
            print(f"{proxy_data['host']}:{proxy_data['port']}")

    proxy_file = get_file_path("data") + '/proxyinfo.json'  # 拼接代理池文件路径

    with open(proxy_file, "w") as json_file:
        json.dump(proxies, json_file)

    print(f"代理池更新成功，共计{len(proxies)}个代理！\n")

    return proxies

# 随机代理
def random_proxy(proxies_list):
    return random.choice(proxies_list)  # 随机返回一个代理