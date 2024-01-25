import csv
from pydriller import Git, Repository
from datetime import datetime
# 时间筛选标准, 2022-07-30

name = "avro"
name = name.upper()

repo_path = 'E:/info/repo/' + name
file_path = 'E:/info/' + name + '_commit_bug.txt'


with open(file_path, "r") as f:
    commits_bug_sha = f.read()
commits_bug_sha = commits_bug_sha.split("\n")

analyse_time = datetime(2022, 7, 30, 0, 0, 0)
all_commits = Repository(path_to_repo=repo_path, to=analyse_time).traverse_commits() # 得到commit

# 设立三个表， 项目基本信息表， commits基本信息表， 项目修改信息表
commit_info_list = []
commit_change_info_list = []
all_lines = 0
file_nums = 0

i = 0

for commit in all_commits:
    i = i + 1
    print(i)
    is_bug = 0
    for commit_bug_sha in commits_bug_sha:
        if commit.hash == commit_bug_sha:
            is_bug = 1

    commit_info = []
    try:
        commit_info.append(commit.hash)
        commit_info.append(is_bug)
        # 基本commit信息
        committer = commit.committer
        commit_info.append(committer.name)
        commit_date = commit.committer_date
        commit_info.append(commit_date)
        parents = commit.parents
        commit_info.append(parents)
        all_del = commit.deletions
        commit_info.append(all_del)
        all_add = commit.insertions
        commit_info.append(all_add)
        all_change_lines = commit.lines
        all_lines += all_change_lines
        commit_info.append(all_change_lines)

        commit_info.append(all_lines)
        files_change_nums = commit.files
        commit_info.append(files_change_nums)
        dmm_unit_size = commit.dmm_unit_size
        commit_info.append(dmm_unit_size)
        dmm_unit_complexity = commit.dmm_unit_complexity
        commit_info.append(dmm_unit_complexity)
        dmm_unit_interface = commit.dmm_unit_interfacing
        commit_info.append(dmm_unit_interface)


        # 修改文件信息
        modify_files = commit.modified_files
        commit_add_file_nums = 0
        for modify_file in modify_files:
            commit_change_info = []
            commit_change_info.append(commit.hash)
            file_name = modify_file.filename
            commit_change_info.append(file_name)
            added_lines = modify_file.added_lines
            commit_change_info.append(added_lines)
            deleted_lines = modify_file.deleted_lines
            commit_change_info.append(deleted_lines)
            nloc = modify_file.nloc
            commit_change_info.append(nloc)
            file_complexity = modify_file.complexity
            commit_change_info.append(file_complexity)
            methods_before = modify_file.methods_before
            methods_before_nums = len(methods_before)
            commit_change_info.append(methods_before_nums)
            changed_methods = modify_file.changed_methods
            changed_methods_nums = len(changed_methods)
            commit_change_info.append(changed_methods_nums)
            # print(str(modify_file.change_type))
            if str(modify_file.change_type) == "ModificationType.ADD":
                commit_add_file_nums += 1

            token_count = modify_file.token_count
            commit_change_info.append(token_count)
            commit_change_info_list.append(commit_change_info)

        file_nums += commit_add_file_nums
        commit_info.append(file_nums)
        commit_info_list.append(commit_info)

    except Exception as e:
        print(e)

with open("E:/info/" + name + ".csv", 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(commit_info_list)

with open("E:/info/" + name + "_CHANGE.csv", 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(commit_change_info_list)
