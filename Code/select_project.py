import csv
import time
from datetime import datetime
from github import Github

# 认证你的GitHub账户。在此之前请确保你已经生成了一个Access Token
g = Github("XXXXXX")
# 获取apache组织对象
org = g.get_organization("apache")
repos = org.get_repos()
print(repos.totalCount)
project_list_info = []
i = 0
tol_name = ""

for repo in repos:
    i = i + 1
    print(i)
    if (i == 1500):
        time.sleep(3600)
    language_count = {}
    per_language_rate = {}
    mylist = []
    try:
        # 获取repository的语言信息
        languages = repo.get_languages()
        name = repo.name
        star = repo.stargazers_count
        commits_num = repo.get_commits().totalCount
        if commits_num < 1000:  # 用commits进行筛选
            continue
        contributors = repo.get_contributors().totalCount
        created_time = repo.created_at
        # 获取存储库的最近一次 commit
        commits = repo.get_commits()
        last_commit = commits[0]
        # 获取最近一次 commit 的提交时间
        last_commit_time = last_commit.commit.author.date
        # 最近提交时间筛选
        if last_commit_time < datetime(2022, 6, 1, 0, 0):
            continue
        time_delta = last_commit_time - created_time

        # 统计每个repository使用的语言
        legal_language_nums = 0
        for language, bytes_of_code in languages.items():
            if language in language_count:
                language_count[language] += bytes_of_code
            else:
                language_count[language] = bytes_of_code
        is_select = 1
        total_bytes_of_code = sum(language_count.values())

        for language, bytes_of_code in language_count.items():
            percentage = bytes_of_code / total_bytes_of_code * 100
            per_language_rate[language] = percentage
            if percentage > 5:
                legal_language_nums += 1

        if legal_language_nums < 2:
            continue

        per_language_rate = str(per_language_rate)
        mylist.append(name)
        mylist.append(star)
        mylist.append(commits_num)
        mylist.append(contributors)
        mylist.append(time_delta)
        mylist.append(per_language_rate)
        project_list_info.append(mylist)

    except Exception as e:
        print(e)


with open("E:/info/projection_info.csv", 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(project_list_info)
