# coding=utf-8
#  代码文件

# 定义加法函数
def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def calc(opr):
    if opr == '+':
        return add
    else:
        return sub


def calc2(opr):
    if opr == '+':
        return lambda a, b: (a + b)
    else:
        return lambda a, b: (a - b)


f1 = calc('+')
f2 = calc('-')
f3 = calc('-')

print("10 + 5 = {0}".format(f1(10, 5)))
print("10 - 5 = {0}".format(f2(10, 5)))
print("10 - 5 = {0}".format(f3(10, 5)))
