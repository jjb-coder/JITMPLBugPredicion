import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

with open('output.txt', 'r') as file:
    # 逐行读取文件内容并存储为列表
    lines = file.readlines()

# 去除每行末尾的换行符，并存储为新的列表
name = [line.strip() for line in lines]

results = []
for train_name in name:
    path = "E:/info/" + train_name + "_prediction.csv"
    data = pd.read_csv(path, index_col=0)

    x = data.drop(['is_bug', 'is_many_language'], axis=1)
    y = data[['is_bug', 'is_many_language']]
    yy = []
    for index, row in y.iterrows():
        if row['is_bug'] == 0 and row['is_many_language'] == 0:
            yy.append(1)
        elif row['is_bug'] == 0 and row['is_many_language'] == 1:
            yy.append(2)
        elif row['is_bug'] == 1 and row['is_many_language'] == 0:
            yy.append(3)
        else:
             yy.append(4)
    # 将数据集划分为训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, yy, test_size=0.3, random_state=42)
    # 创建SVM分类器
    clf = LogisticRegression(multi_class='ovr', solver='liblinear', max_iter=1000)
    # 训练模型
    clf.fit(x_train, y_train)
    # 在测试集上进行预测
    y_pred = clf.predict(x_test)

    # 计算准确率
    accuracy = accuracy_score(y_test, y_pred)

    print(f"{accuracy * 100:.2f}")

