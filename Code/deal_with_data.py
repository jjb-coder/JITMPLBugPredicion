import pandas as pd
import re
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from pydriller import Git, Repository
import scipy.stats as stats

name = "zookeeper"
name = name.upper()

# 读取CSV文件
data = pd.read_csv("E:/info/" + name + ".csv")
data = data.dropna()  # 去除空行

change_data = pd.read_csv("E:/info/" + name + "_change.csv")
change_data = change_data.dropna()

repo = 'E:/info/repo/' + name.lower()
analyse_time = datetime(2022, 7, 30, 0, 0, 0)

gr = Git(repo)

# 处理数据
new_part_data_list = []

for index, row in data.iterrows():
    mylist = []
    mysha = row['sha']
    author_name = row["committer_name"]
    mylist.append(mysha)
    filter_change_data = change_data[change_data["sha"] == mysha]
    complexity = 0
    max_complexity = 0
    before_methods = 0
    max_before_methods = 0
    changed_methods = 0
    max_changed_methods = 0
    token_count = 0
    max_token_count = 0
    language_deletions = 0
    language_add = 0
    same_file_percent = 0
    file_nums_entropy = {}

    file_type = set()
    try :
        # 判断上次修改这些文件是不是他本人
        commits = Repository(path_to_repo=repo, single=mysha).traverse_commits()
        change_files_num = 0 # 修改的文件数量
        change_same_files_num = 0 # 修改相同文件的数量
        for commit in commits:
            buggy_commits = gr.get_commits_last_modified_lines(commit)
            # print(commit)
            for change_files_name, change_sha_list in buggy_commits.items():
                for last_change_sha in change_sha_list:
                    last_change_row = data[data['sha'] == last_change_sha]
                    if last_change_row.empty == 0:
                        change_files_num += 1
                        if list(last_change_row["committer_name"])[0] == author_name:
                            change_same_files_num += 1
        if change_files_num:
            same_file_percent = change_same_files_num / change_files_num

    except Exception as e:
        print(e)

    for myindex, myrow in filter_change_data.iterrows():
        file_name = myrow["file_name"]
        match = re.search(r'\.([a-zA-Z0-9]+)$', file_name)
        if match:
            file_extension = match.group(1)
            if file_extension in file_nums_entropy:
                file_nums_entropy[file_extension] += 1
            else:
                file_nums_entropy[file_extension] = 1

        complexity += myrow["file_complexity"]
        max_complexity = max(max_complexity, myrow["file_complexity"])
        before_methods += myrow["methods_before"]
        max_before_methods = max(myrow["methods_before"], before_methods)
        changed_methods += myrow["changed_methods"]
        max_changed_methods = max(myrow["changed_methods"], max_changed_methods)
        token_count += myrow["token_count"]
        max_token_count = max(myrow["token_count"], token_count)
        pattern = r'\.(.*?)($|\s)'  # 匹配点号后的整个字符串，直到行尾或空格
        result = re.search(pattern, myrow["file_name"])
        file_type.add(result.group(1))
        language_deletions += myrow["deleted_lines"]
        language_add += myrow["added_lines"]

    is_main_language = 0
    is_many_language = 0
    many_language_files = len(file_type)

    if "java" in file_type:
        is_main_language = 1

    if len(file_type) > 1:
       is_many_language = 1

    row_nums = filter_change_data.shape[0]
    if row_nums == 0:
        continue
    complexity /= row_nums
    before_methods /= row_nums
    changed_methods /= row_nums
    token_count /= row_nums
    mylist.append(complexity)
    mylist.append(max_complexity)
    mylist.append(before_methods)
    mylist.append(max_before_methods)
    mylist.append(changed_methods)
    mylist.append(max_changed_methods)
    mylist.append(token_count)
    mylist.append(max_token_count)
    mylist.append(is_main_language)
    mylist.append(is_many_language)
    mylist.append(many_language_files)
    mylist.append(language_deletions)
    mylist.append(language_add)
    mylist.append(same_file_percent)

    values_list = list(file_nums_entropy.values())
    list_sum = sum(values_list)
    result_list = [num / list_sum for num in values_list]
    entropy_value = stats.entropy(result_list, base=2)
    mylist.append(entropy_value)
    new_part_data_list.append(mylist)

# 将列表转换为DataFrame
new_part_data = pd.DataFrame(new_part_data_list, columns=['sha', 'complexity', 'max_complexity', 'before_methods', 'max_before_methods', 'changed_methods', 'max_changed_methods', 'token_count', 'max_token_count', 'is_main_language', 'is_many_language','many_language_files', "language_deletions", "language_add", "same_file_percent", "entropy_value"])

merge_info = pd.merge(data, new_part_data, on='sha', how='inner')

# 删除列
del merge_info['sha']
del merge_info['committer_name']
del merge_info['commit_time']
del merge_info['parents']

merge_info.to_csv("E:/info/" + name + "_prediction.csv", index=True)

# # 划分特征和标签
x = merge_info.drop(['is_bug', 'is_many_language'], axis=1)
y = merge_info[['is_bug', 'is_many_language']]

# 随机森林
# 将数据集分为训练集和测试集
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

# 创建随机森林分类器
rf_classifier = RandomForestClassifier(n_estimators=1000, random_state=42)

# 训练分类器
rf_classifier.fit(x_train, y_train)

# 使用训练好的模型进行预测
y_pred = rf_classifier.predict(x_test)

# 计算模型的准确性
accuracy = accuracy_score(y_test, y_pred)
print(f"模型的准确性: {accuracy * 100:.2f}%")





