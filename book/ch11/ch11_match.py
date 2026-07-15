import re
p = r'\w+@zhijieketang\.com'
email = 'tony_guan588@zhijieketang.com'
m = re.match(p,email)
print(m)
print(type(m))

email2 = 'tony_guan588@163.com'
m = re.match(p,email2)
print(m)

print(re.search(p,email))

p = r'Java|java|JAVA'
text = 'I like java and Java and JAVA'
match_list = re.findall(p,text)
print(match_list)

p = r'\d+'
text = 'ABCD12EFG12'
repace_text = re.sub(p,'*',text)
print(repace_text)

print(re.split(p,text))


