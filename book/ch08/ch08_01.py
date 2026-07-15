def rect_area(width, height):
    area = width * height
    return area


print(rect_area(320, 480))


def print_area(width, height):
    area = width * height
    print("{0} x {1} 长方形的面积：{2}".format(width, height, area))


print_area(320, 480)

r_area = rect_area(320, 480)
print("{0} x {1} 长方形的面积：{2:.2f}".format(320, 480, r_area))

r_area = rect_area(width=320, height=480)


def make_coffee(name="卡布奇洛"):
    return "制作一杯{0}咖啡。".format(name)


coffee = make_coffee("拿铁")
coffee1 = make_coffee()

print(coffee)
print(coffee1)
