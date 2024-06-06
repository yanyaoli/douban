'''
    线性回归分析
    1. 读取数据
    2. 划分训练集和测试集
    3. 使用线性回归模型进行分析
    4. 在测试集上进行预测
    5. 计算均方误差和R^2
    6. 绘制预测结果
    7. 返回均方误差和R^2
'''

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from utils.getPath import get_file_path

def plot_results(X_test, y_test, y_pred, xlabel, ylabel):   # 定义 plot_results 函数，接收四个参数：测试集特征，测试集标签，预测值，横坐标标签，纵坐标标签
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']   # 设置中文字体

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))     # 创建画布

    # 绘制散点图和预测线
    axes[0].scatter(X_test, y_test, color='black')  # 绘制散点图
    axes[0].plot(X_test, y_pred, color='blue', linewidth=3) # 绘制预测线
    axes[0].set_xlabel(xlabel)
    axes[0].set_ylabel(ylabel)
    axes[0].set_title('预测结果')
    axes[0].grid(True)

    # 绘制残差图
    residuals = y_test - y_pred # 计算残差
    axes[1].scatter(y_pred, residuals, color='red') # 绘制残差图
    axes[1].axhline(y=0, color='black', linestyle='--', linewidth=2)    # 绘制参考线
    axes[1].set_xlabel('预测值')
    axes[1].set_ylabel('残差')
    axes[1].set_title('残差图')
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()

def linear_regression_analysis(X, y, xlabel, ylabel):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)   # 划分训练集和测试集

    model = LinearRegression()  # 创建线性回归模型
    model.fit(X_train, y_train) # 在训练集上训练模型

    y_pred = model.predict(X_test)  # 在测试集上进行预测

    mse = mean_squared_error(y_test, y_pred)    # 计算均方误差
    r2 = r2_score(y_test, y_pred)   # 计算R^2
    print(f'均方误差为: {mse}')
    print(f'R^2 分数为: {r2}')

    plot_results(X_test, y_test, y_pred, xlabel, ylabel)    # 绘制预测结果

    return mse, r2

def linear_regression():
    # 读取数据
    data_file_path = get_file_path('data') + '/details_info.csv'  # 获取文件路径
    data = pd.read_csv(data_file_path)

    data['五星比例'] = data['五星比例'].str.rstrip('%').astype(float)   # 处理含有百分号的数据列

    # 特征1：评分与五星比例
    X1 = data[['评分']]
    y1 = data['五星比例']
    mse1, r2_1 = linear_regression_analysis(X1, y1, '评分', '五星比例')
    print(f'特征1（评分与五星比例）的均方误差为: {mse1}, R^2分数为: {r2_1}')

    # 特征2：评分与评分人数
    X2 = data[['评分']]
    y2 = data['评分人数']
    mse2, r2_2 = linear_regression_analysis(X2, y2, '评分', '评分人数')
    print(f'特征2（评分与评分人数）的均方误差为: {mse2}, R^2分数为: {r2_2}')
    return mse1, r2_1, mse2, r2_2