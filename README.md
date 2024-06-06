# 豆瓣电影排行榜爬虫

数据分析作业代码，豆瓣电影排行榜数据爬取（排名页面+详情页面），进行简单数据分析。

## 使用说明

### 克隆项目

```bash
git clone https://github.com/yanyaoli/douban.git
```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行项目

```bash
python run.py
```
未使用多线程，可能会有些卡顿。

## 功能说明

- 基本信息爬虫：只爬取排行榜显示的相关信息
- 详情信息爬虫：爬取每个电影详情页信息，建议填写Cookie，避免反爬限制
- 简单数据分析：词云图、热度排名统计、聚类分析、线性回归


<div class="image-container">
<img class="image-item" src='./files/词云图/主演词云图.png'>
<img class="image-item" src='./files/词云图/导演词云图.png'>
<img class="image-item" src='./files/词云图/编剧词云图.png'>
<img class="image-item" src='./files/词云图/制片国家或地区词云图.png'>
<img class="image-item" src='./files/词云图/类型词云图.png'>
<img class="image-item" src='./files/词云图/语言词云图.png'>
</div>

<div class="image-container">
<img class="image-item" src='./files/分析图/热榜.png'>
<img class="image-item" src='./files/分析图/排行榜.png'>
<img class="image-item" src='./files/分析图/二维聚类分析.png'>
<img class="image-item" src='./files/分析图/三维聚类分析.png'>
<img class="image-item" src='./files/分析图/线性回归_评分与五星比例.png'>
<img class="image-item" src='./files/分析图/线性回归_评分与评分人数.png'>
<img class="image-item" src='./files/分析图/线性回归分析.png'>
</div>

<style>
.image-container {
    display: flex;
    flex-wrap: wrap;
}
.image-item {
    flex: 1 0 33%;
    max-width: 33%;
}
</style>

## 文件树

```
douban
├─ gui.py （程序GUI界面）
├─ README.md （说明文件）
├─ run.py （程序入口文件）
├─ utils （存放一些依赖文件）
│  ├─ font.ttf （字体文件）
│  ├─ getPath.py （文件路径获取）
│  ├─ headers.py （请求头获取）
│  ├─ proxy.py （代理池获取）
│  ├─ saveData.py （数据保存）
│  └─ __init__.py
├─ files （存放生成的分析文件）
├─ data （存放爬取的文件）
│  ├─ basic_datacccc.csv （电影详情信息文件）
│  ├─ details_info.csv （电影基本信息文件）
│  ├─ proxyinfo.json （代理池文件）
│  └─ __init__.py
└─ core
   ├─ basic_spider.py （基本信息爬虫）
   ├─ cluster.py （聚类分析）
   ├─ detail_spider.py （详情信息爬虫）
   ├─ linear.py （线性回归分析）
   ├─ stat.py （基本信息统计）
   ├─ word_cloud.py （词云）
   └─ __init__.py
```

