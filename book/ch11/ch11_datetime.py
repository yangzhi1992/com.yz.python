import datetime
print(datetime.datetime(2020,2,28))
print(datetime.datetime.today())
print(datetime.datetime.now())
print(datetime.datetime.now(tz = None))
print(datetime.datetime.fromtimestamp(9999999999.999))

print(datetime.date(2020,2,28))
print(datetime.date.today())
print(datetime.date.fromtimestamp(9999999999.999))

print(datetime.time(23,59,58,1999))

# 获取当前本地日期
d = datetime.date.today()
# 创建10天后的timedelta对象
delta = datetime.timedelta(days=1)
# 当前日期+1天
d += delta
print(d)

delta = datetime.timedelta(weeks=1)
d += delta
print(d)


print(d.strftime("%Y-%m-%d %H:%M:%S"))
print(d.strftime("%Y-%m-%d"))
date = datetime.datetime.strptime("2026-07-23 00:00:00","%Y-%m-%d %H:%M:%S")
print(date)

