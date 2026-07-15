"""
01-agent-eco-level1: Agent 三层生态 - Level 1：核心组件
============================================================
学习内容: LLM + 工具集 + 记忆 + 决策 + 行动 + 学习
"""

print("=" * 60)
print("📚 Agent 三层生态 - Level 1：核心组件")
print("=" * 60)

ECOSYSTEM = """
┌────────────────────────────────────────────────────────────┐
│                   Agent 三层生态架构                        │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  Level 3: Agent 市场 / 任务分发层                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  注册中心 | 任务队列 | 调度器 | 信用评级 | 计费系统   │  │
│  └──────────────────────────────────────────────────────┘  │
│                        ↑                                   │
│  Level 2: Agent 内部闭环                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  记忆 → 决策 → 行动 → 学习 → (循环)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                        ↑                                   │
│  Level 1: Agent 核心组件 (当前模块)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  LLM | 工具集 | 记忆 | 决策 | 行动 | 学习             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
"""
print(ECOSYSTEM)

print("\n" + "=" * 60)
print("🔧 Demo: Agent 6 大核心组件详解")
print("=" * 60)

# ============ 1. LLM ============
print("\n📌 1. LLM（大脑 - 推理与生成）")
print("-" * 40)

LLM_COMPONENT = """
┌─────────────────────────────────────────────────────────────┐
│  LLM = Agent 的"大脑"                                       │
│                                                             │
│  功能:                                                      │
│  ├── 理解用户意图（自然语言理解）                             │
│  ├── 规划任务步骤（推理与计划）                               │
│  ├── 决定调用什么工具（决策）                                 │
│  └── 生成最终回复（文本生成）                                 │
│                                                             │
│  接入方式:                                                  │
│  ├── Ollama (本地)   → qwen2:7b, llama3.1:8b               │
│  ├── OpenAI          → gpt-4o, gpt-4o-mini                 │
│  ├── Anthropic       → claude-3.5-sonnet                   │
│  └── 国产            → DeepSeek, 通义千问, 文心一言          │
│                                                             │
│  关键配置:                                                  │
│  ├── model:    模型名称                                      │
│  ├── temperature: 0.0~1.0 (确定性→创造性)                   │
│  ├── max_tokens: 最大输出长度                                │
│  └── stream:    是否流式输出                                 │
└─────────────────────────────────────────────────────────────┘
"""
print(LLM_COMPONENT)

# ============ 2. 工具集 ============
print("\n📌 2. 工具集（手脚 - 外部能力）")
print("-" * 40)

class ToolSet:
    """Agent 工具集"""

    def __init__(self):
        self.tools = {}

    def register(self, name, func, desc, category="通用"):
        self.tools[name] = {
            "func": func, "desc": desc, "category": category
        }

    def list_tools(self, category=None):
        if category:
            return {k: v for k, v in self.tools.items() if v["category"] == category}
        return self.tools

    def execute(self, name, args=None):
        if name not in self.tools:
            return f"未知工具: {name}"
        return self.tools[name]["func"](args)

    def get_descriptions(self):
        """生成工具描述给 LLM 看"""
        return "\n".join(
            f"  - {n}: {v['desc']} [{v['category']}]"
            for n, v in self.tools.items()
        )

# 注册各种工具
ts = ToolSet()
ts.register("search_web", lambda _: "搜索结果...", "搜索互联网", "信息检索")
ts.register("search_kb", lambda _: "知识库结果...", "搜索内部知识库", "信息检索")
ts.register("calculator", lambda a: str(eval(a)), "数学计算", "数据处理")
ts.register("send_email", lambda a: f"邮件已发送: {a}", "通信", "办公")
ts.register("create_chart", lambda a: "图表已生成", "数据可视化", "数据分析")
ts.register("query_db", lambda a: "查询结果", "数据库查询", "数据处理")

print("  工具分类:")
for cat in ["信息检索", "数据处理", "办公", "数据分析"]:
    tools = ts.list_tools(cat)
    if tools:
        print(f"    [{cat}]: {', '.join(tools.keys())}")

print(f"\n  工具描述(给LLM):\n{ts.get_descriptions()}")
print(f"\n  执行测试: {ts.execute('calculator', '1+2*3')}")

# ============ 3. 记忆 ============
print("\n📌 3. 记忆（经验 - 上下文保持）")
print("-" * 40)

class MemorySystem:
    """Agent 记忆系统"""

    def __init__(self):
        self.working = {}       # 工作记忆 (当前任务)
        self.short_term = []    # 短期记忆 (最近N轮)
        self.long_term = {}     # 长期记忆 (持久化知识)
        self.episodic = []      # 情景记忆 (重要事件)

    def remember_working(self, key, value):
        self.working[key] = value

    def remember_dialog(self, role, content):
        self.short_term.append({"role": role, "content": content})
        if len(self.short_term) > 20:
            self.short_term.pop(0)

    def remember_fact(self, key, value):
        self.long_term[key] = value

    def remember_event(self, event):
        self.episodic.append(event)

    def recall(self, query):
        """综合检索记忆"""
        results = []

        # 工作记忆
        if query in self.working:
            results.append(("working", self.working[query]))

        # 长期记忆
        for k, v in self.long_term.items():
            if query in k:
                results.append(("long_term", v))

        # 情景记忆
        for e in self.episodic:
            if query in str(e):
                results.append(("episodic", e))

        return results

ms = MemorySystem()
ms.remember_working("current_task", "客户咨询")
ms.remember_dialog("user", "你好，我想咨询RAG技术")
ms.remember_fact("张三", "VIP客户")
ms.remember_event({"type": "购买", "product": "企业版", "amount": 50000})

print("  记忆类型:")
print(f"    工作记忆: {ms.working}")
print(f"    短期记忆: {len(ms.short_term)}条对话")
print(f"    长期记忆: {list(ms.long_term.keys())}")
print(f"    情景记忆: {len(ms.episodic)}条")
print(f"  检索 '张三': {ms.recall('张三')}")

# ============ 4. 决策 ============
print("\n📌 4. 决策（判断 - 选择下一步）")
print("-" * 40)

class DecisionEngine:
    """Agent 决策引擎"""

    def __init__(self):
        self.strategies = {}

    def register_strategy(self, name, func):
        self.strategies[name] = func

    def decide(self, state):
        """综合决策"""
        results = []
        for name, strategy in self.strategies.items():
            decision = strategy(state)
            results.append({"strategy": name, "decision": decision})
        # 加权投票
        final = max(results, key=lambda r: r.get("confidence", 0.5))
        return final

# 决策策略
def rule_based(state):
    """基于规则的决策"""
    if "计算" in state.get("task", ""):
        return {"decision": "call_calculator", "confidence": 0.9}
    if "搜索" in state.get("task", ""):
        return {"decision": "call_search", "confidence": 0.8}
    return {"decision": "direct_reply", "confidence": 0.5}

def priority_based(state):
    """基于优先级"""
    if state.get("user_level") == "VIP":
        return {"decision": "priority_handle", "confidence": 0.9}
    return {"decision": "normal_handle", "confidence": 0.6}

de = DecisionEngine()
de.register_strategy("rules", rule_based)
de.register_strategy("priority", priority_based)

state1 = {"task": "计算1+2", "user_level": "normal"}
state2 = {"task": "你好", "user_level": "VIP"}

print(f"  决策1: {de.decide(state1)}")
print(f"  决策2: {de.decide(state2)}")

# ============ 5. 行动 ============
print("\n📌 5. 行动（执行 - 调用工具/API）")
print("-" * 40)

class ActionExecutor:
    """行动执行器"""

    def __init__(self):
        self.actions = {}

    def register(self, name, fn):
        self.actions[name] = fn

    def execute(self, action, params=None):
        if action not in self.actions:
            return {"status": "error", "msg": f"未知行动: {action}"}

        try:
            result = self.actions[action](params)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "msg": str(e)}

    def batch_execute(self, actions):
        """批量执行"""
        return [self.execute(a, p) for a, p in actions]

ae = ActionExecutor()
ae.register("api_call", lambda p: f"API调用: {p}")
ae.register("db_query", lambda p: f"查询: {p}")
ae.register("send_msg", lambda p: f"发送: {p}")
ae.register("file_write", lambda p: f"写入: {p}")

results = ae.batch_execute([
    ("api_call", "GET /user"),
    ("db_query", "SELECT * FROM users"),
    ("send_msg", "回复用户"),
])
for r in results:
    print(f"  {r['status']}: {r['result']}")

# ============ 6. 学习 ============
print("\n📌 6. 学习（进化 - 自我优化）")
print("-" * 40)

class LearningModule:
    """Agent 学习模块"""

    def __init__(self):
        self.feedback_log = []
        self.success_patterns = {}
        self.error_patterns = {}

    def record_feedback(self, action, result, success):
        """记录反馈"""
        self.feedback_log.append({
            "action": action, "result": result, "success": success
        })
        if success:
            self.success_patterns[action] = self.success_patterns.get(action, 0) + 1
        else:
            self.error_patterns[action] = self.error_patterns.get(action, 0) + 1

    def analyze(self):
        """分析学习结果"""
        total = len(self.feedback_log)
        if total == 0:
            return {"msg": "暂无数据"}

        success_rate = sum(1 for f in self.feedback_log if f["success"]) / total
        best_action = max(self.success_patterns, key=self.success_patterns.get) if self.success_patterns else None
        worst_action = max(self.error_patterns, key=self.error_patterns.get) if self.error_patterns else None

        return {
            "total": total,
            "success_rate": f"{success_rate:.1%}",
            "best_action": best_action,
            "worst_action": worst_action,
        }

    def recommend(self, task):
        """基于学习推荐行动"""
        # 选择成功率最高的同类行动
        return max(self.success_patterns, key=self.success_patterns.get) if self.success_patterns else None

lm = LearningModule()
lm.record_feedback("search", "找到结果", True)
lm.record_feedback("search", "找到结果", True)
lm.record_feedback("calculate", "3", True)
lm.record_feedback("api_call", "超时", False)

print(f"  学习分析: {lm.analyze()}")
print(f"  推荐行动: {lm.recommend('查询')}")

print("\n✅ Level 1 核心组件完成！")
