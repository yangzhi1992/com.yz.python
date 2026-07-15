i = 32
s = 'i * i = ' + str(i * i)
print(s)

# 默认占位符
s = 'i * i = {}'.format(i * i)
print(s)

# 参数占位符
s = '{0} * {0} = {1}'.format(i, i * i)
print(s)

# 参数名占位符
s = '{p1} * {p1} = {p2}'.format(p1=i, p2=i * i)
print(s)

s_str = 'Hello World'
s_str.find('e')
s_str.find('l')
s_str.find('l', 4)
s_str.find('l', 4, 6)

text = 'AB CD EF GH IJ'
text.replace(' ', '|', 2)
text.replace(' ', '|')
text.replace(' ', '|', 1)

text.split(' ', )
text.split(' ', maxsplit=0)
text.split(' ', maxsplit=1)
text.split(' ', maxsplit=2)
