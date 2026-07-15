"""
阶段2：算法基础
==============
学习内容:
  1. 时间复杂度/空间复杂度
  2. 排序算法（快排/归并）
  3. 二分查找
  4. 链表/栈/队列
  5. 哈希表/二叉树
  6. 动态规划入门
"""

import time
import random

# ============ 2.1 排序算法 ============
print("=== 2.1 排序算法 ===")

def quick_sort(arr):
    """快速排序 O(nlogn)"""
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    mid  = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)

def merge_sort(arr):
    """归并排序 O(nlogn)"""
    if len(arr) <= 1:
        return arr
    mid = len(arr)//2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]

arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
print(f"原始: {arr}")
print(f"快排: {quick_sort(arr)}")
print(f"归并: {merge_sort(arr)}")

# ============ 2.2 二分查找 ============
print("\n=== 2.2 二分查找 ===")

def binary_search(arr, target):
    """二分查找 O(log n)"""
    left, right = 0, len(arr)-1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

arr = sorted([3, 7, 1, 9, 4, 6, 8, 2, 5])
print(f"有序数组: {arr}")
print(f"查找 7: 下标={binary_search(arr, 7)}")
print(f"查找 10: 下标={binary_search(arr, 10)}")

# ============ 2.3 哈希表 ============
print("\n=== 2.3 哈希表 ===")

def two_sum(nums, target):
    """两数之和 - 哈希表 O(n)"""
    seen = {}
    for i, v in enumerate(nums):
        complement = target - v
        if complement in seen:
            return [seen[complement], i]
        seen[v] = i
    return []

print(f"两数之和 [2,7,11,15], target=9 → {two_sum([2,7,11,15], 9)}")

# ============ 2.4 动态规划 ============
print("\n=== 2.4 动态规划 ===")

def fibonacci_dp(n):
    """斐波那契 - DP O(n)"""
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

print(f"fib(10) = {fibonacci_dp(10)}")
print(f"fib(50) = {fibonacci_dp(50)}")

# 0-1背包问题
def knapsack(weights, values, capacity):
    """0-1背包 DP O(n*capacity)"""
    n = len(weights)
    dp = [[0]*(capacity+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for w in range(1, capacity+1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w],
                               dp[i-1][w-weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]
    return dp[n][capacity]

print(f"背包最大价值: {knapsack([2,3,4,5], [3,4,5,6], 8)}")

# ============ 2.5 BFS/DFS ============
print("\n=== 2.5 BFS/DFS ===")
from collections import deque

graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

def bfs(graph, start, target):
    """广度优先搜索 - 最短路径"""
    visited = {start}
    queue = deque([(start, [start])])
    while queue:
        node, path = queue.popleft()
        if node == target:
            return path
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None

print(f"BFS A→F 最短路径: {bfs(graph, 'A', 'F')}")

def dfs(graph, start, target, visited=None, path=None):
    """深度优先搜索"""
    if visited is None:
        visited, path = set(), []
    visited.add(start)
    path = path + [start]
    if start == target:
        return path
    for neighbor in graph[start]:
        if neighbor not in visited:
            result = dfs(graph, neighbor, target, visited, path)
            if result:
                return result
    return None

print(f"DFS A→F 路径: {dfs(graph, 'A', 'F')}")

print("\n✅ 阶段2完成！")
