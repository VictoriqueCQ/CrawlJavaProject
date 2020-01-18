import pyexcel
import os


class OriginalRepository:
    def __init__(self, create_time, id, star, name, url):
        self.create_time = create_time
        self.id = id
        self.star = star
        self.name = name
        self.url = url

    def toString(self):
        return '''==============================\ncreate_time:%s\nid:%s\nstar:%s\nname:%s\nurl:%s\n==============================\n''' % (
            str(self.create_time), str(self.id), str(self.star), str(self.name), str(self.url))


class Repository(OriginalRepository):
    def __init__(self, with_android, with_androidTest_folder, note, create_time, id, star, name, url, src_num, src_set):
        super().__init__(create_time, id, star, name, url)
        self.with_android = with_android
        self.with_androidTest_folder = with_androidTest_folder
        self.note = note
        self.src_num = src_num
        self.src_set = src_set

    def toString(self):
        return '''==============================\ncreate_time:%s\nid:%s\nstar:%s\nname:%s\nurl:%s\nwith_android:%s\nwith_androidTest_folder:%s\nnote:%s\nsrc_num:%s\nsrc_set:%s\n==============================\n''' % (
            str(self.create_time), str(self.id), str(self.star), str(self.name), str(self.url), str(self.with_android),
            str(self.with_androidTest_folder), str(self.note), str(self.src_num), str(self.src_set))


class Project:
    def __init__(self, project_name, repository_id, url, note):
        self.project_name = project_name
        self.repository_id = repository_id
        self.url = url
        self.note = note

    def toString(self):
        return '''==============================\nproject_name:%s\nrepository_id:%s\nurl:%s\nnote:%s\n==============================\n''' % (
            str(self.project_name), str(self.repository_id), str(self.url), str(self.note))


# 从磁盘中获取实际爬下来的项目信息
path = 'D:/javaProjectsFromGithub/2017/Aug'
repository_list = os.listdir(path)
for repository in repository_list:
    if os.path.isfile(os.path.join(path, repository)):
        repository_list.remove(repository)
repository_list.sort()

# 从excel中获取与在磁盘中存在的项目的完整信息。excel中项目数量大于等于磁盘中实际存在的项目数量
filename = "D:\\2017_Aug.xlsx"
records = pyexcel.iget_records(file_name=filename)
repositories = []
for record in records:
    repo = OriginalRepository(record['create_time'], record['id'], record['star'], record['name'], record['url'])
    repo_dir_name = repo.name + "_" + str(repo.id) + "_" + str(repo.star)
    if repo_dir_name in repository_list:
        repositories.append(repo)
print(len(repositories))

# 第一轮过滤，过滤掉不存在测试的仓库
first_filter_repo_list = list()
for repo in repositories:
    repo_path = path + "/" + str(repo.name) + "_" + str(repo.id) + "_" + str(repo.star)
    file_path_list = list()
    repository = Repository(with_android=0, with_androidTest_folder=0, note=0, create_time=repo.create_time,
                            id=repo.id, star=repo.star, name=repo.name, url=repo.url, src_num=0, src_set=None)
    for fpathe, dirs, fs in os.walk(repo_path):
        for f in fs:
            file_path = os.path.join(fpathe, f)
            file_path_list.append(file_path)
    src_set = set()
    for file_path in file_path_list:
        # print(file_path)
        if "\\test" in file_path and "src\\junit" not in file_path:
            # print(file_path)
            # print(repo_path)
            # print("=======================")
            repository.note = 1
        elif "\\test" not in file_path and "src\\junit" in file_path:
            repository.note = 2

        if "AndroidManifest.xml" in file_path:
            repository.with_android = 1

        if "androidTest" in file_path:
            repository.with_androidTest_folder = 1

        if "\\src\\" in file_path:
            dir_path = file_path.split('src')[0]
            src_set.add(dir_path)
            # print(dir_path)
            # print(repo_path)
            # print("==================================")
    #         src_num += 1
    repository.src_num = len(src_set)
    repository.src_set = src_set
    # for i in src_set:
    #     print(i)
    # print("-----------------------------")
    first_filter_repo_list.append(repository)

# for i in first_filter_repo_list:
#     print(i.toString())
# 第二轮过滤步骤1，过滤掉安卓项目
first_filter_result = list()
for repo in first_filter_repo_list:
    first_filter_result_dict = dict()
    first_filter_result_dict['create_time'] = repo.create_time
    first_filter_result_dict['id'] = repo.id
    first_filter_result_dict['star'] = repo.star
    first_filter_result_dict['name'] = repo.name
    first_filter_result_dict['url'] = repo.url
    first_filter_result_dict['with_android'] = repo.with_android
    first_filter_result_dict['with_androidTest_folder'] = repo.with_androidTest_folder
    first_filter_result_dict['note'] = repo.note
    first_filter_result_dict['src_num'] = repo.src_num
    first_filter_result.append(first_filter_result_dict)

pyexcel.save_as(records=first_filter_result, dest_file_name="D:\\2017_Aug_first_filter.xlsx")

new_first_filter_repo_list = list()
for repo in first_filter_repo_list:
    if repo.with_android == 0 and repo.with_androidTest_folder == 0:
        new_first_filter_repo_list.append(repo)
print(len(new_first_filter_repo_list))
# for i in new_first_filter_repo_list:
#     print(i.toString())


# 第二轮过滤步骤2，根据src筛选出项目
second_filter_project_list = list()
second_filter_repo_set = set()
for repo in new_first_filter_repo_list:
    project_path_list = list(repo.src_set)
    for project_path in project_path_list:
        project = Project(project_name=project_path, repository_id=repo.id, url=repo.url, note=0)
        project_file_path_list = list()
        for fpathe, dirs, fs in os.walk(project_path):
            for f in fs:
                file_path = os.path.join(fpathe, f)
                project_file_path_list.append(file_path)
        for project_file_path in project_file_path_list:
            if "\\test" in project_file_path and "src\\junit" not in file_path:
                # print(file_path)
                # print(repo_path)
                # print("=======================")
                project.note = 1
            elif "\\test" not in file_path and "src\\junit" in file_path:
                project.note = 2
        if project.note == 1:
            second_filter_repo_set.add(repo)
            second_filter_project_list.append(project)

print("repository number:")
print(len(second_filter_repo_set))
print("project number:")
print(len(second_filter_project_list))
# for i in second_filter_project_list:
#     print(i.toString())
second_filter_result = list()
for project in second_filter_project_list:
    second_filter_result_dict = dict()
    second_filter_result_dict['project_name'] = project.project_name
    second_filter_result_dict['repository_id'] = project.repository_id
    second_filter_result_dict['url'] = project.url
    second_filter_result_dict['note'] = project.note
    second_filter_result.append(second_filter_result_dict)
pyexcel.save_as(records=second_filter_result, dest_file_name="D:\\2017_Aug_second_filter.xlsx")
