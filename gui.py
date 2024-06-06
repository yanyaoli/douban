'''
    GUI界面
    主要功能：
    1. 更新代理池
    2. 爬取基本信息
    3. 爬取详情信息
    4. 词云图
    5. 聚类分析
    6. 线性回归
    7. 基础统计
'''

import tkinter as tk
from tkinter import Label, Button, Text, Frame, simpledialog
from tkinter import *

root = tk.Tk()
root.title("豆瓣电影爬虫")
root.configure(bg='#f0f0f0')

label = Label(root, text="豆瓣电影爬虫", font=("System", 20), bg='#f0f0f0')
label.grid(row=0, column=0)


# 更新代理池
def updateProxy():
    from utils.proxy import get_proxy

    proxies = get_proxy()
    info_text.delete('1.0','end')
    info_text.insert(END, "代理池更新完毕\n代理数量：" + str(len(proxies)) + "\n")
    info_text.see("end")

# 获取基本信息
def getBasicData():
    from core.basic_spider import get_basic_info

    _, total_time, file_path = get_basic_info()
    info_text.delete('1.0','end')
    info_text.insert(END, f"电影基本信息已爬取完毕，用时：{total_time:0.2f} 秒\n结果已保存至{file_path}\n")
    info_text.see("end")

# 获取详情信息
def getDetails():
    from core.detail_spider import get_details

    global Cookie
    Cookie = simpledialog.askstring("Cookie", "请输入Cookie，置空可能会影响爬取效果")
    info_text.delete('1.0','end')
    info_text.insert(END, "请等待...\n")
    root.update()
    total_time, file_path = get_details(Cookie)

    info_text.delete('1.0','end')
    info_text.insert(END, f"电影详情信息已爬取完毕，用时：{total_time:0.2f} 秒\n结果已保存至{file_path}\n")
    info_text.see("end")

# 词云图
def getWordCloud():
    from core.word_cloud import generate_wordcloud_from_column

    window = Toplevel(root)
    window.title("词云图选择")

    wc_btn_frame = Frame(window)
    wc_btn_frame.pack(pady=10)

    def display_wordcloud(column_name, title):
        generate_wordcloud_from_column(column_name, title)

    # 添加按钮来选择显示哪个词云图
    Button(wc_btn_frame, text="导演", command=lambda: display_wordcloud('导演', '导演词云图'), font=("System", 15), bg='skyblue').grid(row=0, column=0, padx=10)
    Button(wc_btn_frame, text="编剧", command=lambda: display_wordcloud('编剧', '编剧词云图'), font=("System", 15), bg='skyblue').grid(row=0, column=1, padx=10)
    Button(wc_btn_frame, text="主演", command=lambda: display_wordcloud('主演', '主演词云图'), font=("System", 15), bg='skyblue').grid(row=0, column=2, padx=10)
    Button(wc_btn_frame, text="类型", command=lambda: display_wordcloud('类型', '类型词云图'), font=("System", 15), bg='skyblue').grid(row=1, column=0, padx=10)
    Button(wc_btn_frame, text="制片国家或地区", command=lambda: display_wordcloud('制片国家或地区', '制片国家或地区词云图'), font=("System", 15), bg='skyblue').grid(row=1, column=1, padx=10)
    Button(wc_btn_frame, text="语言", command=lambda: display_wordcloud('语言', '语言词云图'), font=("System", 15), bg='skyblue').grid(row=1, column=2, padx=10)

# 聚类分析
def clusterAnalysis():
    from core.cluster import cluster_analysis

    result = cluster_analysis()
    info_text.delete('1.0','end')
    info_text.insert(END, "聚类分析完毕\n")
    for item in result:
        info_text.insert(END, f"聚类簇 {item['聚类簇']} 中心：\n评分: {item['评分']}\n评分人数: {item['评分人数']}\n\n")
    info_text.see("end")

# 线性回归
def linearRegression():
    from core.linear import linear_regression

    mse1, r2_1, mse2, r2_2 = linear_regression()
    info_text.delete('1.0','end')
    info_text.insert(END, f"特征1（评分与五星比例）\n均方误差为: {mse1}\nR^2分数为: {r2_1}\n\n")
    info_text.insert(END, f"特征2（评分与评分人数）\n均方误差为: {mse2}\n R^2分数为: {r2_2}\n\n")
    info_text.see("end")

# 基础统计
def basicStat():
    from core.stat import get_hot_list, get_ranking_list

    window = Toplevel(root)
    window.title("统计图选择")

    wc_btn_frame = Frame(window)
    wc_btn_frame.pack(pady=10)

    Button(wc_btn_frame, text="热榜统计图", command=get_hot_list, font=("System", 15), bg='skyblue').grid(row=0, column=1, padx=10)
    Button(wc_btn_frame, text="排名统计图", command=get_ranking_list, font=("System", 15), bg='skyblue').grid(row=0, column=2, padx=10)

# 第一排按钮
first_btn_frame = Frame(root)
first_btn_frame.grid(row=1, column=0, pady=10)

# 更新代理池按钮
update_proxy_btn = Button(first_btn_frame, text="更新代理池", command=updateProxy, font=("System", 15), bg='skyblue')
update_proxy_btn.grid(row=1, column=0, padx=10)

# 爬取基本信息按钮
run_btn_basic = Button(first_btn_frame, text="爬取基本信息", command=getBasicData, font=("System", 15), bg='skyblue')
run_btn_basic.grid(row=1, column=1, padx=10)

# 爬取详情信息按钮
run_btn_details = Button(first_btn_frame, text="爬取详情信息", command=getDetails, font=("System", 15), bg='skyblue')
run_btn_details.grid(row=1, column=2, padx=10)

#第二排按钮
second_btn_frame = Frame(root)
second_btn_frame.grid(row=2, column=0, pady=10)

# 词云图按钮
word_cloud_btn = Button(second_btn_frame, text="词云图", command=getWordCloud, font=("System", 15), bg='skyblue')
word_cloud_btn.grid(row=2, column=0, padx=5)

# 聚类分析
cluster_btn = Button(second_btn_frame, text="聚类分析",command=clusterAnalysis, font=("System", 15), bg='skyblue')
cluster_btn.grid(row=2, column=1, padx=5)

# 线性回归
linear_btn = Button(second_btn_frame, text="线性回归",command=linearRegression, font=("System", 15), bg='skyblue')
linear_btn.grid(row=2, column=2, padx=5)

# 基础统计
stat_btn = Button(second_btn_frame, text="基础统计", command=basicStat,font=("System", 15), bg='skyblue')
stat_btn.grid(row=2, column=3, padx=5)

# 信息显示框
box_frame = Frame(root)
box_frame.grid(row=3, column=0, padx=10)

info_text = Text(box_frame, width=40, height=10, font=("微软雅黑", 15), bg='white')
info_text.grid(row=3, column=0)

info_text.insert(END, "欢迎使用豆瓣电影爬虫\n未使用多线程处理任务，速度较慢，请耐心等待\n")

about_me = Label(box_frame, text="@yanyaoli", font=("微软雅黑", 10), fg="orange")
about_me.grid(row=4, column=0)

root.mainloop()
