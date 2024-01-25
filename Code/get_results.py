from sklearn.model_selection import cross_val_predict
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.metrics import confusion_matrix

path = "E:/info/" + "Thrift" + "_prediction.csv"
data = pd.read_csv(path, index_col=0)

# # 划分特征和标签
x = data.drop(['is_bug', 'is_many_language'], axis=1)
x = x[["many_language_files","entropy_value","all_lines","file_nums"]]
print(x)
y = data[['is_bug', 'is_many_language']]

# 创建随机森林分类器
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
y_pred = cross_val_predict(rf_classifier, x, y, cv=5)

# 计算准确度、精确度、召回率和F1分数的微平均
accuracy = accuracy_score(y, y_pred)
precision, recall, f1, _ = precision_recall_fscore_support(y, y_pred, average='micro')

# 输出结果
print(f"Micro-average Accuracy:{accuracy * 100:.2f}")
print(f"Micro-average Precision:{precision* 100:.2f}")
print(f"Micro-average Recall:{recall*100:.2f}")
print(f"Micro-average F1-Score:{f1*100:.2f}")