import sys
import os
import os.path

# 查找文件

def file_name(file_dir, type):
    k = os.walk(file_dir)
    for root, dirs, files in k:
        # print("root是  %s" % root)  # 当前目录路径
        # print("11111111  %s" % dirs)  # 当前路径下所有子目录
        # print("333333  %s" % files)  # 当前路径下所有非目录子文件
        for file in files:
            if os.path.splitext(file)[1] == type:
                print("找到一个类型一样的%s" % os.path.abspath(file))


def myFind(path, type):
    print("")
    for file in os.listdir(path):
        filePath = os.path.join(path, file)
        if os.path.isfile(filePath) and os.path.splitext(filePath)[1] == type:
            print("找到一个 ----------  %s" % filePath)
        elif os.path.isdir(filePath):
            myFind(filePath, type)

# myFind("C:\\Users\\spc\\Desktop\\设计图", ".png")
