"""
03-agent-eco-level3: Agent 三层生态 - Level 3：Agent 市场/任务分发层
========================================================================
学习内容: 注册中心、任务队列、调度器、信用评级、计费系统
"""

print("=" * 60)
print("📚 Agent 三层生态 - Level 3：Agent 市场/任务分发")
print("=" * 60)

MARKET_LAYER = """
┌────────────────────────────────────────────────────────────┐
│            Level 3: Agent 市场 / 任务分发层                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                    Agent 市场                         │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐    │  │
│  │  │ 客服A   │  │ 翻译B   │  │ 分析C   │  │ 编码D   │    │  │
│  │  │★4.8    │  │★4.5    │  │★4.9    │  │★4.6    │    │  │
│  │  │¥0.01/次│  │¥0.02/次│  │¥0.05/次│  │¥0.03/次│    │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘    │  │
│  └──────────────────────────────────────────────────────┘  │
│                            │                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                任务分发系统                            │  │
│  │  ├── 注册中心: Agent 注册/发现/状态管理                │  │
│  │  ├── 任务队列: 请求排队/优先级/超时                     │  │
│  │  ├── 调度器:  匹配/路由/负载均衡                        │  │
│  │  └── 监控:    信用/计费/日志/告警                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  类比: App Store + 外卖平台 + 云计算                       │
│  开发者上架 Agent → 用户按需调用 → 平台抽成                │
└────────────────────────────────────────────────────────────┘
"""
print(MARKET_LAYER)

print("\n" + "=" * 60)
print("🔧 Demo: Agent 市场与任务分发系统")
print("=" * 60)

# ============ 1. Agent 注册中心 ============
print("\n📌 1. Agent 注册中心")
print("-" * 40)

class AgentRegistry:
    """Agent 注册中心"""

    def __init__(self):
        self.agents = {}

    def register(self, agent_id, info):
        self.agents[agent_id] = {
            **info,
            "status": "online",
            "total_tasks": 0,
            "success_tasks": 0,
            "rating": 5.0,
        }
        print(f"  注册 Agent: {agent_id} ({info['name']})")

    def unregister(self, agent_id):
        if agent_id in self.agents:
            self.agents[agent_id]["status"] = "offline"
            print(f"  注销 Agent: {agent_id}")

    def discover(self, capability=None):
        """发现可用的 Agent"""
        results = []
        for aid, info in self.agents.items():
            if info["status"] == "online":
                if not capability or capability in info.get("capabilities", []):
                    results.append({"id": aid, **info})
        return results

    def get_stats(self):
        return {
            "total": len(self.agents),
            "online": sum(1 for a in self.agents.values() if a["status"] == "online"),
            "total_tasks": sum(a["total_tasks"] for a in self.agents.values()),
        }

registry = AgentRegistry()
registry.register("agent_001", {"name": "客服助手", "capabilities": ["客服", "问答"], "price": 0.01})
registry.register("agent_002", {"name": "翻译官", "capabilities": ["翻译", "语言"], "price": 0.02})
registry.register("agent_003", {"name": "数据分析师", "capabilities": ["分析", "报表"], "price": 0.05})

print(f"\n  在线 Agent: {len(registry.discover())}个")
print(f"  客服类: {len(registry.discover('客服'))}个")
print(f"  统计: {registry.get_stats()}")

# ============ 2. 任务队列 ============
print("\n📌 2. 任务队列")
print("-" * 40)

from collections import deque
import time
import json

class TaskQueue:
    """任务队列"""

    def __init__(self):
        self.queue = deque()
        self.history = []

    def submit(self, task):
        task["id"] = f"task_{int(time.time())}_{len(self.history)}"
        task["status"] = "pending"
        task["created_at"] = time.time()
        self.queue.append(task)
        self.history.append(task)
        print(f"  提交任务: {task['id']} ({task.get('type', '未知')})")
        return task["id"]

    def prioritize(self, task_id, priority):
        """调整优先级 (数字越小越优先)"""
        for task in self.queue:
            if task["id"] == task_id:
                task["priority"] = priority
                print(f"  调整优先级: {task_id} → {priority}")
                break

    def next_task(self):
        """获取下一个最高优先级的任务"""
        if not self.queue:
            return None
        best = min(self.queue, key=lambda t: t.get("priority", 5))
        self.queue.remove(best)
        best["status"] = "processing"
        return best

    def complete(self, task_id, result):
        for task in self.history:
            if task["id"] == task_id:
                task["status"] = "completed"
                task["result"] = result
                task["completed_at"] = time.time()
                break

tq = TaskQueue()
tq.submit({"type": "客服", "content": "退货咨询", "priority": 1})
tq.submit({"type": "分析", "content": "Q3报表", "priority": 3})
tq.submit({"type": "翻译", "content": "合同翻译", "priority": 2})

task = tq.next_task()
print(f"\n  分发: {task['id']} ({task['content']})")
tq.complete(task["id"], "已完成")
print(f"  待处理: {len(tq.queue)}个任务")

# ============ 3. 调度器 ============
print("\n📌 3. 调度器 (任务 ↔ Agent 匹配)")
print("-" * 40)

class Scheduler:
    """任务调度器"""

    def __init__(self, registry):
        self.registry = registry
        self.strategies = {
            "round_robin": self._round_robin,
            "best_match": self._best_match,
            "lowest_load": self._lowest_load,
        }

    def _round_robin(self, task, candidates):
        """轮询"""
        idx = hash(task["id"]) % len(candidates)
        return candidates[idx]

    def _best_match(self, task, candidates):
        """最佳匹配"""
        task_type = task.get("type", "")
        scored = []
        for c in candidates:
            score = sum(1 for cap in c.get("capabilities", []) if cap in task_type)
            scored.append((c, score))
        return max(scored, key=lambda x: x[1])[0]

    def _lowest_load(self, task, candidates):
        """最少负载"""
        return min(candidates, key=lambda c: c.get("total_tasks", 0))

    def schedule(self, task, strategy="best_match"):
        candidates = self.registry.discover()
        if not candidates:
            return None

        matcher = self.strategies.get(strategy, self._best_match)
        selected = matcher(task, candidates)
        selected["total_tasks"] += 1
        print(f"  调度策略: {strategy}")
        print(f"  匹配 Agent: {selected['name']} ({selected['id']})")
        return selected

scheduler = Scheduler(registry)

task1 = {"id": "task_001", "type": "客服咨询"}
task2 = {"id": "task_002", "type": "数据分析"}

scheduler.schedule(task1, "best_match")
scheduler.schedule(task2, "best_match")

# ============ 4. 信用评级 ============
print("\n📌 4. 信用评级系统")
print("-" * 40)

class CreditRating:
    """Agent 信用评级"""

    def __init__(self):
        self.ratings = {}

    def init_agent(self, agent_id):
        self.ratings[agent_id] = {
            "score": 100, "total": 0, "success": 0,
            "avg_response_time": 0, "rating": 5.0
        }

    def record_result(self, agent_id, success, response_time):
        if agent_id not in self.ratings:
            self.init_agent(agent_id)
        r = self.ratings[agent_id]
        r["total"] += 1
        if success:
            r["success"] += 1
        r["avg_response_time"] = (
            (r["avg_response_time"] * (r["total"] - 1) + response_time) / r["total"]
        )
        # 信用分更新
        r["score"] += 5 if success else -10
        r["score"] = max(0, min(200, r["score"]))
        # 评级
        if r["score"] >= 150:
            r["rating"] = 5.0
        elif r["score"] >= 100:
            r["rating"] = 4.0
        elif r["score"] >= 60:
            r["rating"] = 3.0
        else:
            r["rating"] = 1.0

    def get_level(self, agent_id):
        score = self.ratings.get(agent_id, {}).get("score", 0)
        if score >= 150: return "⭐ 钻石"
        if score >= 100: return "⭐ 黄金"
        if score >= 60:  return "⭐ 白银"
        return "⭐ 青铜"

cr = CreditRating()
cr.init_agent("agent_001")
cr.record_result("agent_001", True, 1.2)
cr.record_result("agent_001", True, 0.8)
cr.record_result("agent_001", False, 3.0)
cr.record_result("agent_001", True, 0.5)

print(f"  信用分: {cr.ratings['agent_001']['score']}")
print(f"  等级: {cr.get_level('agent_001')}")
print(f"  成功率: {cr.ratings['agent_001']['success']/cr.ratings['agent_001']['total']:.0%}")

# ============ 5. 计费系统 ============
print("\n📌 5. 计费系统")
print("-" * 40)

class BillingSystem:
    """Agent 计费系统"""

    def __init__(self):
        self.prices = {}
        self.usage = {}  # agent_id → {user_id: count}

    def set_price(self, agent_id, price_per_call):
        self.prices[agent_id] = price_per_call

    def charge(self, agent_id, user_id):
        if agent_id not in self.usage:
            self.usage[agent_id] = {}
        if user_id not in self.usage[agent_id]:
            self.usage[agent_id][user_id] = 0
        self.usage[agent_id][user_id] += 1

        cost = self.prices.get(agent_id, 0.01)
        return cost

    def get_bill(self, user_id):
        total = 0
        items = []
        for agent_id, users in self.usage.items():
            if user_id in users:
                count = users[user_id]
                price = self.prices.get(agent_id, 0.01)
                subtotal = count * price
                total += subtotal
                items.append({"agent": agent_id, "calls": count, "subtotal": subtotal})
        return {"user": user_id, "items": items, "total": total}

bs = BillingSystem()
bs.set_price("agent_001", 0.01)
bs.set_price("agent_002", 0.02)
bs.set_price("agent_003", 0.05)

bs.charge("agent_001", "user_zhang")
bs.charge("agent_001", "user_zhang")
bs.charge("agent_002", "user_zhang")
bs.charge("agent_003", "user_zhang")

bill = bs.get_bill("user_zhang")
print(f"  用户: {bill['user']}")
for item in bill['items']:
    print(f"    {item['agent']}: {item['calls']}次 × ¥{item['subtotal']/item['calls']:.2f} = ¥{item['subtotal']:.2f}")
print(f"  总计: ¥{bill['total']:.2f}")

# ============ 综合：完整市场 ============
print("\n" + "=" * 60)
print("🔧 Demo: 完整 Agent 市场运行")
print("=" * 60)

class AgentMarket:
    """完整的 Agent 市场"""

    def __init__(self):
        self.registry = AgentRegistry()
        self.queue = TaskQueue()
        self.scheduler = Scheduler(self.registry)
        self.credit = CreditRating()
        self.billing = BillingSystem()

    def publish_agent(self, agent_id, info, price):
        self.registry.register(agent_id, info)
        self.billing.set_price(agent_id, price)
        self.credit.init_agent(agent_id)

    def submit_task(self, task):
        return self.queue.submit(task)

    def process_next(self):
        """处理下一个任务"""
        task = self.queue.next_task()
        if not task:
            return None

        agent = self.scheduler.schedule(task)
        if not agent:
            return {"error": "无可用的Agent"}

        # 计费
        cost = self.billing.charge(agent["id"], task.get("user", "anonymous"))

        # 执行 (模拟)
        success = True
        response_time = 0.5

        # 记录信用
        self.credit.record_result(agent["id"], success, response_time)

        self.queue.complete(task["id"], {"agent": agent["id"], "cost": cost})
        return {
            "task": task["id"],
            "assigned_to": agent["name"],
            "cost": cost,
            "credit_level": self.credit.get_level(agent["id"]),
        }

# 完整演示
print("\n🧪 完整 Agent 市场演示:")
market = AgentMarket()

# 发布 Agent
market.publish_agent("cs_001", {"name": "金牌客服", "capabilities": ["客服", "投诉", "咨询"]}, 0.02)
market.publish_agent("trans_001", {"name": "翻译专家", "capabilities": ["翻译", "语言"]}, 0.03)
market.publish_agent("data_001", {"name": "数据分析师", "capabilities": ["分析", "报表", "图表"]}, 0.05)

# 提交任务
tasks = [
    {"type": "客服咨询", "content": "我想退货", "user": "user_zhang", "priority": 1},
    {"type": "数据分析", "content": "Q3销售报表", "user": "user_li", "priority": 2},
    {"type": "翻译", "content": "合同翻译成英文", "user": "user_wang", "priority": 3},
]

for t in tasks:
    task_id = market.submit_task(t)
    result = market.process_next()
    print(f"  处理结果: {result}")

print(f"\n  市场统计: {market.registry.get_stats()}")

print("\n✅ Level 3 Agent 市场完成！")
