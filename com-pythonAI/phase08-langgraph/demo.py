"""
阶段8：LangGraph 工作流编排
============================
学习内容:
  1. 图结构 vs 链式结构
  2. StateGraph / Node / Edge
  3. 条件路由
  4. 多步骤工作流
  5. 带循环的工作流
"""

# ============ 8.1 图结构 vs 链式结构 ============
print("=== 8.1 图结构 vs 链式结构 ===")

COMPARISON = """
📊 链式 vs 图结构

链式（Chain）：           图结构（Graph）：
  A → B → C → D            A → B → C
                              ↓     ↓
                              D ←─ E → F

链式：线性执行，无分支      图：分支、循环、并行

• 链式适合简单顺序任务
• 图结构适合复杂工作流（条件分支、循环、并行）
• LangGraph = LangChain 的图扩展
"""
print(COMPARISON)

# ============ 8.2 StateGraph 基础 ============
print("\n=== 8.2 StateGraph 基础 ===")

# 由于 LangGraph 需要安装且和 LangChain 深度绑定，
# 这里展示核心概念和伪代码

GRAPHGUIDE = """
📝 LangGraph 核心概念

1. State（状态）— 所有节点共享的数据
   class MyState(TypedDict):
       messages: list
       next_step: str

2. Node（节点）— 执行单元
   def process_node(state: MyState) -> MyState:
       # 处理逻辑
       return {"messages": new_messages}

3. Edge（边）— 节点间的连接
   graph.add_edge("node_a", "node_b")  # 固定路径
   graph.add_conditional_edges("check", router)  # 条件路由

4. 条件路由
   def router(state) -> str:
       if state["next_step"] == "rag":
           return "rag_node"
       return "default_node"

5. 编译与执行
   app = graph.compile()
   result = app.invoke({"messages": ["你好"]})
"""

print(GRAPHGUIDE)

# ============ 8.3 多步骤工作流 Demo ============
print("\n=== 8.3 多步骤工作流 Demo ===")

class WorkflowEngine:
    """简易工作流引擎（模拟 LangGraph 概念）"""

    def __init__(self):
        self.nodes = {}
        self.edges = []
        self.conditional_edges = []

    def add_node(self, name, func):
        self.nodes[name] = func

    def add_edge(self, from_node, to_node):
        self.edges.append((from_node, to_node))

    def add_conditional_edge(self, from_node, router_func):
        self.conditional_edges.append((from_node, router_func))

    def run(self, start_node, initial_state):
        current_node = start_node
        state = initial_state.copy()
        step = 0
        max_steps = 10

        while current_node and step < max_steps:
            step += 1
            print(f"  [{step}] 节点: {current_node}")
            state = self.nodes[current_node](state)

            # 检查条件路由
            routed = False
            for from_node, router in self.conditional_edges:
                if from_node == current_node:
                    next_node = router(state)
                    print(f"        → 条件路由到: {next_node}")
                    current_node = next_node
                    routed = True
                    break

            if routed:
                continue

            # 检查固定边
            next_node = None
            for from_node, to_node in self.edges:
                if from_node == current_node:
                    next_node = to_node
                    break
            current_node = next_node

        return state

def demo_workflow():
    """演示：AI 写作工作流"""

    # 节点函数
    def input_check(state):
        topic = state.get("topic", "")
        if len(topic) < 3:
            return {**state, "error": "主题太短"}
        return {**state, "status": "ok"}

    def outline_gen(state):
        outline = f"关于「{state['topic']}」的文章大纲：\n1. 引言\n2. 主体内容\n3. 总结"
        return {**state, "outline": outline}

    def content_gen(state):
        content = f"这是一篇关于{state['topic']}的文章..."
        return {**state, "content": content, "draft": state['outline'] + "\n" + content}

    def polish(state):
        polished = state['content'] + "\n（已润色）"
        return {**state, "final": polished}

    def error_handler(state):
        return {**state, "error": "输入验证失败", "final": None}

    # 路由函数
    def check_topic_router(state):
        return "error_handler" if state.get("error") else "outline_gen"

    # 构建工作流
    wf = WorkflowEngine()
    wf.add_node("input_check", input_check)
    wf.add_node("outline_gen", outline_gen)
    wf.add_node("content_gen", content_gen)
    wf.add_node("polish", polish)
    wf.add_node("error_handler", error_handler)

    wf.add_edge("outline_gen", "content_gen")
    wf.add_edge("content_gen", "polish")
    wf.add_conditional_edge("input_check", check_topic_router)

    # 执行
    print("✅ 工作流 - 正常路径:")
    result = wf.run("input_check", {"topic": "人工智能"})
    print(f"  结果: {result['final'][:60]}...")

    print("\n❌ 工作流 - 错误路径:")
    result = wf.run("input_check", {"topic": "AB"})
    print(f"  结果: error={result.get('error')}")

demo_workflow()

# ============ 8.4 带循环的工作流（Agent 风格）============
print("\n=== 8.4 带循环的工作流 ===")

class AgentWorkflow:
    """模拟 Agent 的 ReAct 循环工作流"""

    def __init__(self, max_iters=5):
        self.max_iters = max_iters

    def run(self, task):
        state = {"task": task, "steps": [], "result": None, "done": False}
        iteration = 0

        while not state["done"] and iteration < self.max_iters:
            iteration += 1
            print(f"  迭代 {iteration}:")

            # 1. 推理（Think）
            thought = f"正在分析: {state['task']}, 已执行步骤: {len(state['steps'])}"
            state["thought"] = thought
            print(f"    思考: {thought}")

            # 2. 检查是否需要工具
            if "计算" in state["task"] and not any("calculate" in s for s in state["steps"]):
                # 调用工具
                state["steps"].append("calculate")
                state["task"] = state["task"].replace("计算", "已计算")
                print(f"    🔧 调用计算器")
            else:
                # 3. 完成
                state["result"] = f"任务完成！最终结果: {state['task']}"
                state["done"] = True
                print(f"    ✅ {state['result']}")

        return state

wf = AgentWorkflow()
print("🤖 Agent 风格工作流:")
result = wf.run("计算 5+3 并告诉我结果")
print(f"  最终状态: {result}")

print("\n✅ 阶段8完成！")
