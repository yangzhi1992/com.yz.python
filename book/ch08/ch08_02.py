# coding=utf-8
#  代码文件

def sum(*numbers):
    total = 0.0
    for number in numbers:
        total += number
    return total


print(sum(100.0, 20.0, 30.0))
print(sum(30.0, 80.0))
