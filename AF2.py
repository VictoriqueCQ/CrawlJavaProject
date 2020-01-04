# 规则1：有test文件夹
# 规则2：有junit文件夹
# 规则3：有tests文件夹
# 规则0：没有以上三种规则
f = open('new_tree.txt', 'rb')
line = f.readlines()
max_line = len(line)
projects = []
for i in range(len(line)):
    s = line[i][4:9].strip()
    match = '|----'
    if '|----' in str(s):
        start_index = i
        project_name = (str(line[i]).split('|----')[1]).split('\\')[0]
        projects.append([[start_index], project_name])
for i in range(len(projects) - 1):
    end = projects[i + 1][0][0] - 1
    projects[i][0].append(end)
projects[-1][0].append(max_line)

# for p in projects:
#     print(p)
#     print(p[0][0])

for project in projects:
    for i in range(project[0][0] - 1, project[0][1]):
        if str('----test') in str(line[i]):
            project.append('note:1')
            break
        elif str('----junit') in str(line[i]):
            project.append('note:2')
            break
        elif str('----tests') in str(line[i]):
            project.append('note:3')
            break
    if str('note:') not in project[-1]:
        project.append('note:0')
    for i in range(project[0][0] - 1, project[0][1]):
        if str('AndroidManifest.xml') in str(line[i]):
            project.append('with_android:1')
            break
    if str('android') not in project[-1]:
        project.append('with_android:0')
    for i in range(project[0][0] - 1, project[0][1]):
        if str('----androidTest') in str(line[i]):
            project.append('with_androidTest_folder:1')
            break
    if str('androidTest') not in project[-1]:
        project.append('with_androidTest_folder:0')

for p in projects:
    print(p)
