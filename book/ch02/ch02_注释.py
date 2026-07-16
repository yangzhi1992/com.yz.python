#!/usr/bin/python3
import inspect

# 单行注释

'''
这是多行注释，用三个单引号
这是多行注释，用三个单引号
这是多行注释，用三个单引号
'''

"""
这是多行注释，用三个双引号
这是多行注释，用三个双引号
这是多行注释，用三个双引号
"""
print("Hello, Python!")


def add(a, b):
    """返回两数之和"""
    return a + b
# 使用 help() 函数
help(add)

def add(a, b):
    """返回两数之和"""
    return a + b
# 使用 inspect.getdoc() 获取文档
print(inspect.getdoc(add))  # 输出: 返回两数之和