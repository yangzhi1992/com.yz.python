# coding=utf-8

i = input('请输入数字：')
n = 8888

try:
    result = n / int(i)
    print(result)
    print('{0}除以{1}等于2'.format(n, i, result))
except:
    print("1、不能除以0，异常：{}".format(e))

try:
    result = n / int(i)
    print(result)
    print('{0}除以{1}等于2'.format(n, i, result))
except ZeroDivisionError as e:
    print("2、不能除以0，异常：{}".format(e))
except ValueError as e:
    print("3、输入的是无效数字，异常：{}".format(e))

try:
    result = n / int(i)
    print(result)
    print('{0}除以{1}等于2'.format(n, i, result))
except (ZeroDivisionError, ValueError) as e:
    print("4、不能除以0，异常：{}".format(e))

try:
    i2 = int(i)
    try:
        result = n / i2
        print('{0}除以{1}等于{2}'.format(n, i2, result))
    except ZeroDivisionError as e1:
        print("5、不能除以0，异常：{}".format(e1))
except ValueError as e2:
    print("6、输入的是无效数字，异常：{}".format(e2))
finally:
    print('释放资源。。。')
