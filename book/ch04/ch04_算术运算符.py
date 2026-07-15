print(1 + 1)
print(1 - 1)
print(1 * 1)
print(1 / 1)
print(1 % 1)
print(1 ** 2)
print(5 // 2)
print("================================")
a = 1
b = 0


def f1():
    print('--进入函数f1--')
    return True


print((a > b) or f1())
print("==")
print((a < b) or f1())
print("==")
print((a < b) and f1())
print("==")
print((a > b) and f1())
