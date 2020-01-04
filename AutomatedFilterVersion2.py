import os

# path = 'D:/UStorage/projects/kylo_81384608_763/'
path = 'D:/UStorage/projects/'
count = 0
for fpathe, dirs, fs in os.walk(path):
    print(fpathe)
    for f in fs:
        print(os.path.join(fpathe, f))
        count += 1
# print("----------------------------")
# print("count:" + str(count))