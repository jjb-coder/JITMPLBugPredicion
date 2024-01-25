import pandas as pd
import csv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np

# 指定CSV文件路径
csv_file_path = 'index_importance.csv'
data = np.loadtxt(csv_file_path, delimiter=',')
labels = ['C{}'.format(i) for i in range(1, 24)]

print(data)
plt.figure(dpi=150)
plt.boxplot(data, labels=labels)
plt.xlabel("Metric")
plt.ylabel("Metric ranking")
# 显示箱线图的各种数据

plt.show()

