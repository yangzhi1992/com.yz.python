# coding=utf-8
#  代码文件

# 定义加法函数
def f1(x):
    return x > 50


def f11(x):
    return lambda x: (x > 50)


dataFilter = [66, 15, 91, 28, 98, 50, 7, 80, 99]
filtered = filter(f1, dataFilter)
dataFilter = list(filtered)
print(filtered)

filtered1 = filter(lambda x: (x > 50), dataFilter)
dataFilter = list(filtered1)
print(dataFilter)


def f2(x):
    return x * 2


def f22(x):
    return lambda x: (x * 2)


dataMap = [66, 15, 91, 28, 98, 50, 7, 80, 99]
maped = map(f2, dataMap)
dataMap = list(maped)
print(dataMap)

maped = map(lambda x: (x * 2), dataMap)
dataMap = list(maped)
print(dataMap)
