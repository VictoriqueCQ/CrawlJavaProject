import pyexcel
import os

filename = "D:\\2017_Aug_second_filter.xlsx"
records=pyexcel.iget_records(file_name=filename)
for record in records:
    print(record['project_name'])