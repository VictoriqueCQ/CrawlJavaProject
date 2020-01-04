import pyexcel

filename = "D:\\2017_Aug.xlsx"
records = pyexcel.iget_records(file_name=filename)
projects = []
for record in records:
    project = {}
    project['create_time'] = record['create_time']
    project['id'] = record['id']
    project['star'] = record['star']
    project['name'] = record['name']
    project['url'] = record['url']
    projects.append(project)

for p in projects:
    print(p)