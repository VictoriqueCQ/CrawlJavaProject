# import os

class repository():
    def __init__(self, create_time, repo_id, repo_name, star, url):
        self.create_time = create_time
        self.repo_id = repo_id
        self.repo_name = repo_name
        self.star = star
        self.url = url

    def set_with_android(self, with_android):
        self.with_android = with_android

    def set_with_androidTest_file(self, with_androidTest_file):
        self.with_androidTest_file = with_androidTest_file

    def set_note(self, note):
        self.note = note


# path = 'D:/UStorage/projects/kylo_81384608_763/'
path = 'D:/UStorage/projects/'
# count = 0
# for fpathe, dirs, fs in os.walk(path):
#     print(fpathe)
#     for f in fs:
#         print(os.path.join(fpathe, f))
#         count += 1
# print("----------------------------")
# print("count:" + str(count))

# -*- coding: utf-8 -*-
import sys
from pathlib import Path


class DirectionTree(object):
    """生成目录树
    @ pathname: 目标目录
    @ filename: 要保存成文件的名称
    """

    def __init__(self, pathname='.', filename='tree.txt'):
        super(DirectionTree, self).__init__()
        self.pathname = Path(pathname)
        self.filename = filename
        self.tree = ''

    def set_path(self, pathname):
        self.pathname = Path(pathname)

    def set_filename(self, filename):
        self.filename = filename

    def generate_tree(self, n=0):
        if self.pathname.is_file():
            self.tree += '    |' * n + '-' * 4 + self.pathname.name + '\n'
        elif self.pathname.is_dir():
            self.tree += '    |' * n + '-' * 4 + \
                         str(self.pathname.relative_to(self.pathname.parent)) + '\\' + '\n'

            for cp in self.pathname.iterdir():
                self.pathname = Path(cp)
                self.generate_tree(n + 1)

    def save_file(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            f.write(self.tree)


if __name__ == '__main__':
    dirtree = DirectionTree()
    # 命令参数个数为1，生成当前目录的目录树
    # if len(sys.argv) == 1:
    #     dirtree.set_path(Path.cwd())
    #     # dirtree.set_path(path)
    #     dirtree.generate_tree()
    #     print(dirtree.tree)
    # # 命令参数个数为2并且目录存在存在
    # elif len(sys.argv) == 2 and Path(sys.argv[1]).exists():
    #     dirtree.set_path(sys.argv[1])
    #     # dirtree.set_path(path)
    #     dirtree.generate_tree()
    #     print(dirtree.tree)
    # # 命令参数个数为3并且目录存在存在
    # elif len(sys.argv) == 3 and Path(sys.argv[1]).exists():
    #     dirtree.set_path(sys.argv[1])
    #     # dirtree.set_path(path)
    #     dirtree.generate_tree()
    #     dirtree.set_filename(sys.argv[2])
    #     # dirtree.set_filename('tree.txt')
    #     dirtree.save_file()
    # else:  # 参数个数太多，无法解析
    #     print('命令行参数太多，请检查！')
    dirtree.set_path(path)
    dirtree.generate_tree()
    dirtree.set_filename('new_tree.txt')
    dirtree.save_file()
    print(dirtree.tree)
