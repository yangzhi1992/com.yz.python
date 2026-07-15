"""
阶段9：Agent 智能体开发
========================
学习内容:
  1. Agent 核心概念（ReAct）
  2. 工具定义与注册
  3. ReAct 循环实现
  4. LangChain Agent
  5. 从零手写 Agent
"""

# ============ 9.1 Agent 核心概念 ============
print("=== 9.1 Agent 核心概念 ===")

CORE_CONCEPTS = """
🤖 Agent 核心概念

Agent = 能自主使用工具的 AI 系统

核心循环（ReAct）：
  1. Reason（推理）— LLM 分析任务，决定下一步
  2. Act（行动）— 调用工具/API
  3. Observe（观察）— 获取工具返回结果
  4. 回到步骤 1，直到任务完成

关键组件：
  • LLM — 大脑（推理能力）
  • Tools — 工具集（行动能力）
  • Memory — 记忆（上下文保持）
  • Planner — 规划器（任务分解）

应用场景：
  • 客服 Agent（查订单+退款+咨询）
  • 数据分析 Agent（查数据库+画图+报告）
  • 代码 Agent（读代码+修改+测试）
"""
print(CORE_CONCEPTS)

# ============ 9.2 工具定义 ============
print("\n=== 9.2 工具定义 ===")

# 方式一：函数装饰器
from functools import wraps

def tool(name=None, description=""):
    def decorator(func):
        tool_name = name or func.__name__
        func.is_tool = True
        func.tool_name = tool_name
        func.tool_description = description or func.__doc__
        return func
    return decorator

@tool(name="calculator", description="数学计算")
def calculator(expr: str) -> str:
    """执行数学表达式计算"""
    import math
    allowed = set("0123456789+-*/.() ")
    if not all(c in allowed for c in expr):
        return "错误：非法字符"
    try:
        return str(eval(expr, {"__builtins__": {}}, {"math": math}))
    except Exception as e:
        return f"计算错误: {e}"

@tool(name="get_time", description="获取当前时间")
def get_time(_: str) -> str:
    """获取当前日期和时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"注册工具: {calculator.tool_name} - {calculator.tool_description}")
print(f"注册工具: {get_time.tool_name} - {get_time.tool_description}")
print(f"  测试计算: {calculator('(15+27)*3')}")
print(f"  测试时间: {get_time('')}")

# ============ 9.3 从零手写 Agent ============
print("\n=== 9.3 从零手写 Agent ===")

class Agent:
    """手写 ReAct Agent"""

    def __init__(self, llm_api="http://localhost:11434/api/chat", model="qwen2:7b"):
        self.llm_api = llm_api
        self.model = model
        self.tools = {}
        self.messages = []

    def register_tool(self, func):
        self.tools[func.tool_name] = func

    def _call_llm(self, messages):
        import requests
        try:
            resp = requests.post(self.llm_api, json={
                "model": self.model, "stream": False, "messages": messages,
            }, timeout=30)
            return resp.json()["message"]["content"]
        except Exception as e:
            return f"[LLM Error: {e}]"

    def run(self, task, max_iterations=5):
        system_prompt = f"""你是智能助手。可用工具：
{chr(10).join(f'- {n}: {t.tool_description}' for n, t in self.tools.items())}

需要工具时回复：TOOL_CALL: 工具名 | 参数
不需要工具时直接回复。"""

        self.messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": task},
        ]

        for i in range(max_iterations):
            print(f"  [迭代{i+1}] 思考中...")
            response = self._call_llm(self.messages)

            if response.startswith("TOOL_CALL:"):
                parts = response.replace("TOOL_CALL:", "").strip().split("|", 1)
                tool_name = parts[0].strip()
                args = parts[1].strip() if len(parts) > 1 else ""

                if tool_name in self.tools:
                    result = self.tools[tool_name](args)
                    print(f"    🔧 调用了 {tool_name} → {result}")
                    self.messages.append({"role": "assistant", "content": f"调用{tool_name}结果: {result}"})
                else:
                    return f"错误: 未知工具 '{tool_name}'"
            else:
                return response

        return "已达最大迭代次数"

# 测试 Agent
print("创建 Agent...")
agent = Agent()
agent.register_tool(calculator)
agent.register_tool(get_time)

print("\n🤖 Agent 对话:")
# 测试计算
result = agent.run("计算 123 + 456 等于多少")
print(f"  回复: {result}")

print("\n✅ 阶段9完成！")
