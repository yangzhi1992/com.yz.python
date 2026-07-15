# coding=utf-8
class Horse:
    def __init__(self, name):
        self.name = name

    def show_info(self):
        return "马的名字：{0}".format(self.name)

    def run(self):
        print("马跑。。。")


class Donkey:
    def __init__(self, name):
        self.name = name

    def show_info(self):
        return "驴的名字：{0}".format(self.name)

    def run(self):
        print("驴跑。。。")

    def roll(self):
        print("驴打滚。。。")


class Mule(Horse, Donkey):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age


m = Mule('萝莉宝', 1)
m.run()
m.roll()
print(m.show_info())
