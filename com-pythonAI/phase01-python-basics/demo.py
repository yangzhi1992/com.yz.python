"""
阶段1：Python编程基础
====================
学习内容:
  1. 变量/数据类型/控制流
  2. 函数/类/模块
  3. 文件IO/异常处理
  4. 列表推导式/生成器
  5. 装饰器/上下文管理器
"""

# ============ 1.1 基础语法 ============
print("=== 1.1 基础语法 ===")
name, age, score = "张三", 25, 92.5
is_adult = age >= 18
items = [1, 2, 3, 4, 5]
squared = [x**2 for x in items if x % 2 == 0]
print(f"姓名: {name}, 成年: {is_adult}, 偶数平方: {squared}")

# ============ 1.2 函数与类 ============
print("\n=== 1.2 函数与类 ===")

def fibonacci(n):
    """生成斐波那契数列（生成器）"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

print(f"斐波那契前10项: {list(fibonacci(10))}")

class Stack:
    """栈 - 后进先出"""
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop() if self._items else None

    @property
    def size(self):
        return len(self._items)

    def __len__(self):
        return self.size

    def __str__(self):
        return f"Stack({self._items})"

s = Stack()
s.push(1); s.push(2); s.push(3)
print(f"栈: {s}, pop: {s.pop()}, size: {len(s)}")

# ============ 1.3 装饰器 ============
print("\n=== 1.3 装饰器 ===")
from functools import wraps
import time

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} 耗时 {time.time()-start:.4f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

print(f"结果: {slow_sum(10**6)}")

# ============ 1.4 上下文管理器 ============
print("\n=== 1.4 上下文管理器 ===")

class FileManager:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"  → 打开 {self.name}")
        return self

    def __exit__(self, *args):
        print(f"  → 关闭 {self.name}")

with FileManager("data.txt"):
    print("  → 读写文件")

# ============ 1.5 文件IO ============
print("\n=== 1.5 文件IO ===")
with open("demo_output.txt", "w", encoding="utf-8") as f:
    f.write("Hello Python AI!\n")
    f.write("大模型学习路线\n")

with open("demo_output.txt", "r", encoding="utf-8") as f:
    print(f.read())

print("\n✅ 阶段1完成！")
