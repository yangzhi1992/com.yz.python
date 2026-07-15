"""
阶段13：多Agent多智能体系统
===========================
学习内容:
  1. 多Agent 架构模式
  2. 角色分工与协作
  3. 通信机制
  4. 任务分解与分配
  5. 多Agent 框架 CrewAI
"""

# ============ 13.1 多Agent 架构 ============
print("=== 13.1 多Agent 架构 ===")

ARCH_PATTERNS = """
🏗️ 多Agent 架构模式

1. 管理器-工作者 (Manager-Worker)
   ┌──────────┐
   │  Manager │ ← 分配任务、汇总结果
   └────┬─────┘
        │
   ┌────┴────┬─────┐
   │Worker1  │W2   │W3
   └─────────┴─────┘

2. 辩论式 (Debate)
   Agent A → 论证观点 → Agent B → 反驳 → ...
   用于：事实核查、逻辑验证

3. 流水线 (Pipeline)
   输入 → Agent1(分析) → Agent2(规划) → Agent3(执行) → Agent4(质检)

4. 市场式 (Marketplace)
   多个 Agent 竞标任务，最优者执行
   用于：资源调度、任务分配

适用场景:
  • 复杂软件开发（PM+架构师+开发者+测试者）
  • 研究报告（研究员+分析师+写作者+审核者）
  • 客服系统（分类Agent+专业Agent+质检Agent）
"""
print(ARCH_PATTERNS)

# ============ 13.2 手写多Agent 系统 ============
print("\n=== 13.2 手写多Agent 系统 ===")

class AgentBase:
    """Agent 基类"""
    def __init__(self, name, role, expertise):
        self.name = name
        self.role = role
        self.expertise = expertise
        self.memory = []

    def think(self, task):
        return f"[{self.name}({self.role})] 正在处理: {task}"

    def execute(self, task):
        return f"[{self.name}] 基于{self.expertise}经验完成任务"

    def collaborate(self, other_agent, task):
        return f"[{self.name}] 请求[{other_agent.name}]协助: {task}"


class ManagerAgent(AgentBase):
    """管理 Agent - 分配任务、汇总结果"""

    def __init__(self, name="PM"):
        super().__init__(name, "项目经理", "项目管理")

    def assign_task(self, worker, task):
        self.memory.append(f"分配: {task} → {worker.name}")
        return f"[{self.name}] 分配给[{worker.name}]: {task}"

    def review_result(self, result):
        review = f"[{self.name}] 审核通过 ✓" if "完成" in result else f"[{self.name}] 需要修改 ✗"
        return review

    def summarize(self, results):
        summary = f"\n📋 项目总结:\n"
        for name, result in results.items():
            summary += f"  • {name}: {result[:50]}...\n"
        return summary


class CodingAgent(AgentBase):
    """编码 Agent"""
    def __init__(self):
        super().__init__("Coder", "开发工程师", "Python/Java")

    def execute(self, task):
        return f"[{self.name}] 完成编码: {task}，输出: demo.py"


class TestingAgent(AgentBase):
    """测试 Agent"""
    def __init__(self):
        super().__init__("Tester", "测试工程师", "自动化测试")

    def execute(self, task):
        return f"[{self.name}] 完成测试: {task}，发现3个bug，已修复"

class AnalysisAgent(AgentBase):
    """分析 Agent"""
    def __init__(self):
        super().__init__("Analyst", "数据分析师", "数据分析/可视化")

    def execute(self, task):
        return f"[{self.name}] 完成分析: {task}，输出分析报告"


# 演示多Agent合作
pm = ManagerAgent()
coder = CodingAgent()
tester = TestingAgent()
analyst = AnalysisAgent()

print("🤝 多Agent 协作演示 - 软件开发流程")
print("=" * 50)

# 阶段1：需求分析
task = "开发一个RAG问答系统"
print(f"\n📌 任务: {task}")
print(analyst.think("分析需求"))
print(analyst.execute("分析{task}的可行性"))
result_analysis = f"{analyst.name}: 需求可行"

# 阶段2：分配任务
print(f"\n{pm.assign_task(coder, task)}")
print(f"{pm.assign_task(tester, '编写测试用例')}")

# 阶段3：执行
result_coding = coder.execute(task)
print(f"\n{result_coding}")

result_testing = tester.execute("对RAG系统进行集成测试")
print(f"{result_testing}")

# 阶段4：审核
print(f"\n{pm.review_result(result_coding)}")
print(f"{pm.review_result(result_testing)}")

# 阶段5：总结
results = {
    "需求分析": result_analysis,
    "编码开发": result_coding,
    "测试验证": result_testing,
}
print(pm.summarize(results))

# ============ 13.3 CrewAI ============
print("\n=== 13.3 CrewAI 框架介绍 ===")

CREWAI_GUIDE = """
🧑‍🤝‍🧑 CrewAI 多Agent 框架

# 安装: pip install crewai

from crewai import Agent, Task, Crew, Process

# 定义 Agent
researcher = Agent(
    role="研究员",
    goal="收集和分析信息",
    backstory="你是一个资深研究员",
    tools=[],  # 可调用工具
    llm="qwen2:7b",
)

writer = Agent(
    role="作家",
    goal="撰写高质量文章",
    backstory="你是一个资深科技作家",
)

# 定义任务
research_task = Task(
    description="研究大模型的最新发展趋势",
    agent=researcher,
)

write_task = Task(
    description="基于研究结果撰写一篇3000字的文章",
    agent=writer,
)

# 创建团队
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,  # 顺序执行
    verbose=True,
)

# 执行
# result = crew.kickoff()
# print(result)

# 流程模式:
#   sequential: 顺序执行（一个接一个）
#   hierarchical: 层级管理（有Manager Agent）
#   consensual: 协商共识
"""
print(CREWAI_GUIDE)

print("\n✅ 阶段13完成！")
