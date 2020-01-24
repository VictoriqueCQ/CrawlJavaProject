import pyexcel
import os


class NewProject:
    def __init__(self, project_name, repository_name, repository_id, testing_framework, junit_version):
        self.project_name = project_name
        self.repsoitory_name = repository_name
        self.repository_id = repository_id
        self.testing_framework = testing_framework
        self.junit_version = junit_version

    def toString(self):
        return '''==============================\nproject_name:%s\nrepository_name:%s\nrepository_id:%s\ntesting_framework:%s\njunit_version:%s\n==============================\n''' % (
            str(self.project_name), str(self.repsoitory_name), str(self.repository_id), str(self.testing_framework),
            str(self.junit_version))


filename = "D:\\2017_Aug_second_filter.xlsx"
records = pyexcel.iget_records(file_name=filename)
records = list(records)
third_filter_project_list = list()
for record in records:
    project = NewProject(project_name=str(record['project_name']),
                         repository_name=(str(record['project_name']).split('/')[-1]).split('\\')[0],
                         repository_id=str(record['repository_id']),
                         testing_framework='',
                         junit_version='')
    path = record['project_name'] + "src"
    file_path_list = list()
    for fpathe, dirs, fs in os.walk(path):
        for f in fs:
            file_path = os.path.join(fpathe, f)
            file_name = str(file_path.split('\\')[-1])
            if ('test' in file_name or 'Test' in file_name) and '.java' in file_name:
                file_path_list.append(file_path)
    project_testing_framework_and_junit_version_set = set()
    for file in file_path_list:
        try:
            testing_framework = 0
            junit_version = 0
            f = open(file, 'rb')
            content = f.read()
            if 'org.junit.' in str(content) and 'org.junit.jupiter.' not in str(content):
                testing_framework = 1
                junit_version = 4
            elif 'org.junit.jupiter.' in str(content):
                testing_framework = 1
                junit_version = 5
            elif 'extends TestCase' in str(content):
                testing_framework = 1
                junit_version = 3
            elif 'org.testing.' in str(content):
                testing_framework = 2
                junit_version = 0
            if (testing_framework, junit_version) != (0, 0):
                project_testing_framework_and_junit_version_set.add((testing_framework, junit_version))
        except EOFError:
            print("no file")
    if len(project_testing_framework_and_junit_version_set) == 1:
        project.testing_framework = list(project_testing_framework_and_junit_version_set)[0][0]
        project.junit_version = project_testing_framework_and_junit_version_set.pop()[1]
        third_filter_project_list.append(project)
    elif len(project_testing_framework_and_junit_version_set) > 1:
        tf = set()
        jv = set()
        for i in project_testing_framework_and_junit_version_set:
            tf.add(str(i[0]))
            jv.add(str(i[1]))
        tf = int(''.join(tf))
        jv = int(''.join(jv))
        project.testing_framework = tf
        project.junit_version = jv
        third_filter_project_list.append(project)

third_filter_result = list()
for project in third_filter_project_list:
    third_filter_result_dict = dict()
    third_filter_result_dict['project_name'] = project.project_name
    third_filter_result_dict['repository_name'] = project.repsoitory_name
    third_filter_result_dict['repository_id'] = project.repository_id
    third_filter_result_dict['testing_framework'] = project.testing_framework
    third_filter_result_dict['junit_version'] = project.junit_version
    third_filter_result.append(third_filter_result_dict)

pyexcel.save_as(records=third_filter_result, dest_file_name="D:\\2017_Aug_third_filter.xlsx")