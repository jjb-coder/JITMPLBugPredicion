from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import csv

# 打开文件
with open('name.txt', 'r') as file:
    # 逐行读取文件内容并存储为列表
    lines = file.readlines()

# 去除每行末尾的换行符，并存储为新的列表
cleaned_lines = [line.strip() for line in lines]

res_tol = []

for name in cleaned_lines:
    name = name.upper()
    path = "E:/info/" + name + "_prediction.csv"
    data = pd.read_csv(path, index_col=0)
    print(data)

    # # 划分特征和标签
    x = data.drop(['is_bug', 'is_many_language'], axis=1)
    y = data[['is_bug', 'is_many_language']]
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(x, y)
    feature_importances = rf_classifier.feature_importances_
    # 获取排序索引
    sorted_indices = np.argsort(feature_importances)[::-1]  # 使用[::-1]反转数组，使得顺序从大到小

    # 创建一个空字典，用于存储元素与排名的映射
    rank_dict = {}

    # 将排序索引的值映射到排名，保存在字典中
    for idx, rank in enumerate(sorted_indices):
        rank_dict[rank] = idx + 1  # 加1是因为排名从1开始

    # 将原数组的元素转化为排名列表
    ranked_list = [rank_dict[i] for i in range(len(feature_importances))]
    print(ranked_list)
    res_tol.append(ranked_list)

with open("index_importance.csv", 'w', newline='') as csvfile:
    # 创建CSV写入器
    csv_writer = csv.writer(csvfile)
    # 将数据写入CSV文件
    csv_writer.writerows(res_tol)



