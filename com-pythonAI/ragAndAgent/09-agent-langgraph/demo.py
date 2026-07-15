"""
09-agent-langgraph: 从 ReAct Agent 到 LangGraph Agent 的搭建
==============================================================
学习内容: ReAct → 状态机 → LangGraph 完整演进
"""

print("=" * 60)
print("📚 ReAct → LangGraph Agent - 学习路线")
print("=" * 60)

EVOLUTION = """
Agent 演进路线:

阶段1: 简单 ReAct (手写循环)
  while True: LLM → 工具 → 观察 → 继续/停止
  优点: 核心逻辑清晰
  缺点: 无状态管理、难扩展

阶段2: 带状态机的 ReAct
  state = {task, steps, result}
  while True: think(state) → act(state) → update(state)
  优点: 可追踪状态
  缺点: 分支逻辑复杂

阶段3: LangGraph Agent
  StateGraph → 节点 → 边 → 条件路由 → 编译
  优点: 清晰的状态管理 + 灵活的路由 + 并行
"""
print(EVOLUTION)

print("\n" + "=" * 60)
print("🔧 Demo: 三个阶段逐步实现")
print("=" * 60)

# ============ 阶段1: 简单 ReAct ============
print("\n📌 阶段1: 简单 ReAct Agent")
print("-" * 40)

class SimpleReAct:
    def __init__(self):
        self.tools = {}

    def register(self, name, fn):
        self.tools[name] = fn

    def run(self, task):
        steps = []
        for i in range(5):
            thought = f"Step{i}: 分析{task}"
            steps.append({"thought": thought, "action": "思考中"})

            if "计算" in task and "calculator" in self.tools:
                result = self.tools["calculator"]("1+2")
                steps[-1]["action"] = f"调用了calculator → {result}"
                task = task.replace("计算", "")
                if "剩下" not in task or len(task.strip()) < 3:
                    steps[-1]["final"] = f"最终回答: {result}"
                    break
            else:
                steps[-1]["final"] = f"最终回答: 处理完毕"
                break
        return steps

sr = SimpleReAct()
sr.register("calculator", lambda x: "3")
print(sr.run("计算 1+2"))

# ============ 阶段2: 带状态的 ReAct ============
print("\n📌 阶段2: 带状态机的 ReAct")
print("-" * 40)

class StateMachineReAct:
    """带状态管理的 ReAct Agent"""

    def __init__(self):
        self.tools = {}

    def register(self, name, fn):
        self.tools[name] = fn

    def think(self, state):
        """推理阶段"""
        state["thought"] = f"分析了{state['task']}，决定下一步"
        return state

    def act(self, state):
        """行动阶段"""
        if state.get("use_tool"):
            tool = self.tools.get(state["tool_name"])
            if tool:
                state["result"] = tool(state["tool_args"])
                state["observation"] = f"工具返回: {state['result']}"
        return state

    def should_continue(self, state):
        """判断是否继续"""
        return state.get("step", 0) < state.get("max_steps", 5)

    def run(self, task):
        state = {
            "task": task,
            "step": 0,
            "max_steps": 5,
            "results": [],
        }

        while self.should_continue(state):
            state = self.think(state)
            if "计算" in state["task"]:
                state["use_tool"] = True
                state["tool_name"] = "calculator"
                state["tool_args"] = "1+2"
            else:
                state["use_tool"] = False

            state = self.act(state)
            state["results"].append({
                "step": state["step"],
                "thought": state.get("thought"),
                "result": state.get("result", "直接回答"),
            })
            state["step"] += 1

            if state["step"] >= 2:
                break

        state["final"] = f"完成: {state['task']}"
        return state

sm = StateMachineReAct()
sm.register("calculator", lambda x: "3")
result = sm.run("计算任务")
print(f"  步骤数: {result['step']}")
print(f"  结果: {result['final']}")

# ============ 阶段3: LangGraph 风格 ============
print("\n📌 阶段3: LangGraph 风格 Agent")
print("-" * 40)

class GraphNode:
    """LangGraph 中的节点"""
    def __init__(self, name, func):
        self.name = name
        self.func = func

class GraphEdge:
    """LangGraph 中的边"""
    def __init__(self, src, dst, condition=None):
        self.src = src
        self.dst = dst
        self.condition = condition  # None=固定边, func=条件边

class LangGraphAgent:
    """简易 LangGraph 风格 Agent"""

    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.state = {}

    def add_node(self, name, func):
        self.nodes[name] = func

    def add_edge(self, src, dst):
        self.edges.append(GraphEdge(src, dst))

    def add_conditional_edge(self, src, condition_fn):
        self.edges.append(GraphEdge(src, None, condition_fn))

    def compile(self):
        """编译图"""
        self.entry_point = "start"
        self.node_order = []
        visited = set()
        queue = [self.entry_point]

        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            if node in self.nodes:
                self.node_order.append(node)

            for edge in self.edges:
                if edge.src == node:
                    if edge.dst:
                        queue.append(edge.dst)
        return self

    def invoke(self, initial_state):
        """执行图"""
        self.state = initial_state
        current = self.entry_point

        while current:
            if current in self.nodes:
                print(f"    ▶ 执行节点: {current}")
                self.state = self.nodes[current](self.state)

            next_node = None
            for edge in self.edges:
                if edge.src == current:
                    if edge.condition:
                        next_node = edge.condition(self.state)
                        print(f"      → 条件路由: {next_node}")
                        break
                    else:
                        next_node = edge.dst
                        break
            current = next_node

        return self.state

# 构建 LangGraph
def node_llm(state):
    state["thought"] = f"分析: {state['task']}"
    if "计算" in state["task"]:
        state["need_tool"] = True
    return state

def node_calculator(state):
    state["result"] = "计算结果: 3"
    return state

def node_respond(state):
    state["final"] = f"最终回答: {state.get('result', '无结果')}"
    return state

def router(state):
    return "calculator" if state.get("need_tool") else "respond"

graph = LangGraphAgent()
graph.add_node("start", node_llm)
graph.add_node("calculator", node_calculator)
graph.add_node("respond", node_respond)
graph.add_conditional_edge("start", router)
graph.add_edge("calculator", "respond")
graph.compile()

print("\n🧪 LangGraph 执行:")
result = graph.invoke({"task": "计算 1+2", "step": 0})
print(f"  最终: {result['final']}")

print("\n✅ ReAct → LangGraph 完成！")
