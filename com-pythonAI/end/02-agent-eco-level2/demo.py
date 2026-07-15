"""
02-agent-eco-level2: Agent 三层生态 - Level 2：内部闭环
============================================================
学习内容: 记忆 → 决策 → 行动 → 学习 → (循环)
"""

print("=" * 60)
print("📚 Agent 三层生态 - Level 2：内部闭环")
print("=" * 60)

CLOSED_LOOP = """
┌────────────────────────────────────────────────────────────┐
│               Agent 内部闭环                                │
│                                                            │
│                    ┌──────────┐                            │
│                    │  记忆     │ ← 存储经验                │
│                    └────┬─────┘                            │
│                         │                                  │
│                         ▼                                  │
│                    ┌──────────┐                            │
│                    │  决策     │ ← 分析+判断               │
│                    └────┬─────┘                            │
│                         │                                  │
│                         ▼                                  │
│                    ┌──────────┐                            │
│                    │  行动     │ ← 执行工具                 │
│                    └────┬─────┘                            │
│                         │                                  │
│                         ▼                                  │
│                    ┌──────────┐                            │
│                    │  学习     │ ← 评估+优化               │
│                    └────┬─────┘                            │
│                         │                                  │
│                         └──────→ (回到记忆, 继续循环)      │
│                                                            │
│  每次循环 = 一个"思考-行动"单元                            │
│  多个循环 = 一个完整的 ReAct 步骤                          │
└────────────────────────────────────────────────────────────┘
"""
print(CLOSED_LOOP)

print("\n" + "=" * 60)
print("🔧 Demo: 完整内部闭环实现")
print("=" * 60)

# ============ 完整闭环 ============
class AgentClosedLoop:
    """Agent 内部闭环系统 - 记忆→决策→行动→学习"""

    def __init__(self):
        self.memory = []          # 记忆
        self.experience = {}      # 学习积累
        self.step_count = 0

    # ---- 记忆阶段 ----
    def remember(self, info):
        """存储经验"""
        self.memory.append(info)
        print(f"    [记忆] 存储: {str(info)[:50]}...")
        return self

    def recall(self, query):
        """检索相关记忆"""
        related = [m for m in self.memory if query in str(m)]
        print(f"    [记忆] 检索到 {len(related)} 条相关")
        return related

    # ---- 决策阶段 ----
    def decide(self, task, context):
        """基于记忆和上下文做决策"""
        self.step_count += 1
        print(f"    [决策] 第{self.step_count}步: 分析任务 '{task[:30]}...'")

        # 从经验中学习
        similar_tasks = [k for k in self.experience if task[:5] in k]

        if similar_tasks:
            best = max(similar_tasks, key=lambda k: self.experience[k]["success_rate"])
            print(f"    [决策] 参考历史经验: '{best[:20]}...' (成功率{self.experience[best]['success_rate']:.0%})")
            return self.experience[best]["best_action"]

        # 默认决策逻辑
        if "计算" in task:
            return "calculator"
        elif "搜索" in task or "查" in task:
            return "search"
        elif "发送" in task:
            return "send"
        else:
            return "llm_reply"

    # ---- 行动阶段 ----
    def act(self, decision, params=None):
        """执行决策"""
        actions = {
            "calculator": lambda p: f"计算结果: {p}",
            "search": lambda p: f"搜索结果: 找到{p}相关信息",
            "send": lambda p: f"已发送: {p}",
            "llm_reply": lambda p: f"AI回复: {p}",
        }

        action_fn = actions.get(decision, actions["llm_reply"])
        result = action_fn(params)
        print(f"    [行动] 执行 '{decision}' → {result}")
        return result

    # ---- 学习阶段 ----
    def learn(self, task, decision, result, success):
        """从结果中学习"""
        key = task[:20]
        if key not in self.experience:
            self.experience[key] = {"total": 0, "success": 0, "best_action": decision}

        exp = self.experience[key]
        exp["total"] += 1
        if success:
            exp["success"] += 1
        exp["success_rate"] = exp["success"] / exp["total"]
        exp["best_action"] = decision

        print(f"    [学习] {'✓成功' if success else '✗失败'}, 累计经验: {exp['total']}次")
        return self

    # ---- 完整闭环 ----
    def run_cycle(self, task, params=None):
        """执行一次完整闭环"""
        print(f"\n  🔄 闭环迭代 #{self.step_count + 1}")
        print(f"  任务: {task}")

        # 1. 记忆 - 检索相关经验
        context = self.recall(task)

        # 2. 决策
        decision = self.decide(task, context)

        # 3. 行动
        result = self.act(decision, params)

        # 4. 记忆 - 存储本次经验
        self.remember({"task": task, "decision": decision, "result": result})

        # 5. 学习 - 评估并优化
        success = "结果" in result or "成功" in result
        self.learn(task, decision, result, success)

        return {"decision": decision, "result": result, "success": success}

# ============ 测试 ============
print("\n🧪 测试 Agent 内部闭环:")
agent = AgentClosedLoop()

# 第1轮
r1 = agent.run_cycle("计算 1+2", "1+2")
# 第2轮 (基于第1轮的经验)
r2 = agent.run_cycle("计算 3*4", "3*4")
# 第3轮 (新任务)
r3 = agent.run_cycle("搜索 RAG技术", "RAG检索增强生成")

print(f"\n📊 学习成果:")
print(f"  经验库: {len(agent.experience)} 条")
for k, v in agent.experience.items():
    print(f"    '{k}...' → 最佳决策: {v['best_action']}, 成功率: {v['success_rate']:.0%}")

print("\n✅ Level 2 内部闭环完成！")
