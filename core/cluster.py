'''
    聚类分析
    1. 读取数据
    2. 数据预处理
    3. 数据标准化
    4. 聚类模型训练
    5. 将聚类结果添加到原始数据中
    6. 分析每个聚类簇中的样本特征
    7. 可视化聚类结果
    8. 返回聚类结果
'''

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from utils.getPath import get_file_path

def cluster_analysis():
    # 读取数据
    data_path = get_file_path('data') + '/details_info.csv'
    data = pd.read_csv(data_path)

    # 处理含有百分号的数据列
    data['五星比例'] = data['五星比例'].str.rstrip('%').astype(float)

    # 选择需要用于聚类的特征：评分、评分人数和五星比例
    X = data[['评分', '五星比例', '评分人数']]

    # 数据标准化
    scaler = StandardScaler()   # 创建标准化对象
    X_scaled = scaler.fit_transform(X)  # 标准化数据

    # 聚类模型训练
    kmeans = KMeans(n_clusters=5, random_state=42)  # 创建 KMeans 聚类模型
    kmeans.fit(X_scaled)    # 在标准化后的数据上训练模型

    # 将聚类结果添加到原始数据中
    data['cluster'] = kmeans.labels_

    # 分析每个聚类簇中的样本特征
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    result = []
    for i, center in enumerate(cluster_centers):
        print(f'聚类簇 {i+1} 中心: 评分={center[0]:.4f}, 五星比例={center[1]:.4f}, 评分人数={center[2]:.4f}')
        result.append({'聚类簇': i+1, '评分': round(center[0], 4), '五星比例': round(center[1], 4), '评分人数': round(center[2], 4)})

    # 设置字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    # 可视化聚类结果
    fig = plt.figure(num='聚类分析', figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d') # 创建3D坐标系

    for i in range(5):  # 遍历每个聚类簇
        cluster_data = data[data['cluster'] == i]
        scatter = ax.scatter(cluster_data['评分'], cluster_data['五星比例'], cluster_data['评分人数'], c=cluster_data['cluster'], cmap='viridis', label=f'聚类簇 {i+1}') # 绘制散点图

    # 添加聚类中心点折线图
    for i, center in enumerate(cluster_centers):
        ax.plot([center[0]], [center[1]], [center[2]], marker='o', markersize=8, color='red')

    ax.set_xlabel('评分') # 设置 x 轴标签
    ax.set_ylabel('五星比例') # 设置 y 轴标签
    ax.set_zlabel('评分人数') # 设置 z 轴标签
    ax.set_title('聚类结果') # 设置标题
    ax.legend(loc='upper left') # 将图例放在左上角
    plt.grid(True) # 添加网格线
    plt.colorbar(scatter, label='聚类簇') # 添加颜色条
    plt.show() # 显示图形

    return result