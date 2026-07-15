"""
06-agent-patterns: Agent 的 8 种设计模式
============================================
学习内容: Agent 设计模式详解与对比
"""

print("=" * 60)
print("📚 Agent 8 种设计模式 - 学习路线")
print("=" * 60)

PATTERNS = """
┌──────┬────────────────────────┬────────────────────────────────┐
│  #   │ 模式                   │ 一句话描述                     │
├──────┼────────────────────────┼────────────────────────────────┤
│  1   │ ReAct                  │ 思考→行动→观察循环             │
│  2   │ Plan-and-Execute       │ 先计划→再执行                  │
│  3   │ Reflection             │ 自我反思和纠错                  │
│  4   │ Tool-Using             │ 调用外部工具                   │
│  5   │ Multi-Agent            │ 多角色协作                     │
│  6   │ Memory-Augmented       │ 带记忆系统的 Agent             │
│  7   │ Self-Discovery         │ 自动发现和生成工具              │
│  8   │ Tree-of-Thought        │ 多路径搜索 + 评估              │
└──────┴────────────────────────┴────────────────────────────────┘
"""
print(PATTERNS)

print("\n" + "=" * 60)
print("🔧 Demo: 8 种 Agent 设计模式实现")
print("=" * 60)

# 1. ReAct
print("\n📌 模式1: ReAct (Standard)")
print("-" * 40)

class ReActAgent:
    """思考→行动→观察 循环"""
    def __init__(self, tools=None):
        self.tools = tools or {}
        self.max_steps = 5

    def add_tool(self, name, func, desc=""):
        self.tools[name] = {"func": func, "desc": desc}

    def run(self, task):
        state = {"task": task, "steps": [], "result": None}
        for i in range(self.max_steps):
            # Reason
            thought = f"第{i+1}步思考: 需要{'调用工具' if i < 1 else '综合结果'}"
            state["thought"] = thought
            # Act
            if i == 0 and "计算" in task and "calculator" in self.tools:
                result = self.tools["calculator"]["func"]("1+2")
                state["steps"].append(f"调用了calculator → {result}")
            else:
                state["result"] = f"最终回答: {task}的答案是3"
                break
        return state

re = ReActAgent()
re.add_tool("calculator", lambda x: "3", "数学计算")
print(re.run("计算 1+2"))

# 2. Plan-and-Execute
print("\n📌 模式2: Plan-and-Execute")
print("-" * 40)

class PlanExecuteAgent:
    """先制定计划，再逐步执行"""
    def run(self, task):
        # Plan
        plan = [f"步骤1: 分析{task}", "步骤2: 收集信息", "步骤3: 综合回答"]
        results = []
        for step in plan:
            results.append(f"执行: {step} ✓")
        return {"plan": plan, "results": results,
                "final": f"计划完成: {task}"}

pe = PlanExecuteAgent()
result = pe.run("写一篇关于RAG的文章")
print(f"  计划: {result['plan']}")
print(f"  结果: {result['final']}")

# 3. Reflection
print("\n📌 模式3: Reflection (自我反思)")
print("-" * 40)

class ReflectionAgent:
    """生成 → 反思 → 改进 循环"""
    def generate(self, task):
        return f"初版回答: {task}"

    def critique(self, output):
        return f"建议: 补充更多技术细节和示例"

    def improve(self, output, feedback):
        return f"改进版: {output}\n{feedback}"

    def run(self, task):
        v1 = self.generate(task)
        fb = self.critique(v1)
        v2 = self.improve(v1, fb)
        return {"v1": v1, "feedback": fb, "v2": v2, "iterations": 2}

rf = ReflectionAgent()
r = rf.run("解释RAG")
print(f"  初版: {r['v1']}")
print(f"  反馈: {r['feedback']}")
print(f"  改进: {r['v2']}")

# 4. Tool-Using
print("\n📌 模式4: Tool-Using")
print("-" * 40)

class ToolUsingAgent:
    def __init__(self):
        self.tools = {}

    def register(self, name, fn, desc):
        self.tools[name] = {"fn": fn, "desc": desc}

    def run(self, task, tool_name):
        if tool_name in self.tools:
            return self.tools[tool_name]["fn"](task)
        return f"未知工具: {tool_name}"

tu = ToolUsingAgent()
tu.register("search", lambda q: f"搜索'{q}'的结果...", "搜索知识库")
tu.register("calculate", lambda e: str(eval(e)), "数学计算")
print(f"  搜索: {tu.run('RAG原理', 'search')}")
print(f"  计算: {tu.run('1+2*3', 'calculate')}")

# 5-8: 概念
print("\n📌 模式5-8: 概念速览")
print("-" * 40)

MORE_PATTERNS = """
模式5: Multi-Agent (多Agent协作)
  PM Agent → 分解任务 → Coder Agent → 编码
                      → Tester Agent → 测试
                      → Reviewer Agent → 审查

模式6: Memory-Augmented (记忆增强)
  短期记忆: 当前对话上下文 (滑动窗口)
  长期记忆: 向量数据库 (历史总结)
  工作记忆: 当前任务状态

模式7: Self-Discovery (自我发现)
  Agent 自动探索环境 → 发现可用API
  → 生成工具描述 → 注册为工具

模式8: Tree-of-Thought (思维树)
  问题 → 3条路径 → 每条路径再分3条 → 评估
  → 选择最优路径 → 逐步深入
  适合: 数学推理、规划问题
"""
print(MORE_PATTERNS)

print("\n✅ Agent 设计模式完成！")
