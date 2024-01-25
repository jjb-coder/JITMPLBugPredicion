# 标记是不是bug
import re
import pymysql
import csv
from pydriller import Repository, Git
from datetime import datetime

name = "ranger"
name = name.upper()

# 设置截止时间, 筛选commit
analyse_time = datetime(2022, 7, 30, 0, 0, 0)

db = pymysql.connect(host="localhost", user="root", password="XXXXXX", port=3306, database='jira', charset='utf8')
cursor = db.cursor()

# 选出bug
sql = f"""
    select issue.key from jira.issue where issue.key like '{name}%' and issue.issuetype = 'Bug'
"""

cursor.execute(sql)
results = cursor.fetchall()

print(results)  # 输出结果

# 关闭连接
cursor.close()
db.close()

sha_set = set() #初始化bug集合

repo_path = 'E:/info/repo/' + name
repo = Repository(repo_path)
gr = Git(repo_path)
for commit in repo.traverse_commits():
    commit_date = commit.committer_date
    if commit_date.replace(tzinfo=None) > analyse_time:
        break
    commit_message = commit.msg
    pattern = rf"^{name}-\d+"
    matches = re.findall(pattern, commit_message)
    if len(matches) != 0:
        # print(commit_message)
        str_matches = matches[0]
        for jira_bug in results:
            if jira_bug[0] == str_matches: # 当前commit是为了解决bug
                # print(str_matches, sha)
                try:
                    buggy_commits = gr.get_commits_last_modified_lines(commit)
                    for change_files_name, change_sha_list in buggy_commits.items():
                        # print(change_files_name)
                        # pattern = re.compile(r"\.(.+)")
                        # matches = re.findall(pattern, change_files_name)
                        for change_sha in change_sha_list:
                            sha_set.add(change_sha)
                except Exception as e:
                    print(e)

# 写入文档
bug_nums = 0
file_path = 'E:/info/' + name + '_commit_bug.txt'
with open(file_path, 'w') as file:
    for item in sha_set:
        file.write(item + '\n')
        bug_nums += 1

print(name, bug_nums)

