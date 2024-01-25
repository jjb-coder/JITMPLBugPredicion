from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import csv

# 打开文件
with open('output.txt', 'r') as file:
    # 使用 'r' 模式来打开文件，表示只读

    # 逐行读取文件内容并存储为列表
    lines = file.readlines()

# 去除每行末尾的换行符，并存储为新的列表
all_projections = [line.strip() for line in lines]

results = []

for name in all_projections:
    name = name.upper()
    data = pd.DataFrame()

    for merge_name in all_projections:
        merge_name = merge_name.upper()
        if merge_name != name:
            path = "E:/info/" + merge_name + "_prediction.csv"
            pro_data = pd.read_csv(path, index_col=0)
            data = pd.concat([data, pro_data], axis=0, ignore_index=True)

    x = data.drop(['is_bug', 'is_many_language'], axis=1)
    y = data[['is_bug', 'is_many_language']]


    path = "E:/info/" + name + "_prediction.csv"
    test_data = pd.read_csv(path, index_col=0)
    x_test = test_data.drop(['is_bug', 'is_many_language'], axis=1)
    y_test = test_data[['is_bug', 'is_many_language']]


    # 创建随机森林分类器
    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_classifier.fit(x, y)
    predictions = rf_classifier.predict(x_test)
    accuracy = accuracy_score(y_test, predictions)
    print(name)
    print("Accuracy: {:.2f}%".format(accuracy * 100))










