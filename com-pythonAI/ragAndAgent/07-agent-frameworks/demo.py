"""
07-agent-frameworks: 19 类 Agent 框架对比
===========================================
学习内容: 主流 Agent 框架对比、选型建议
"""

print("=" * 60)
print("📚 Agent 框架对比 - 19 类框架")
print("=" * 60)

FRAMEWORKS = """
┌────────────────────────────────────────────────────────────────────┐
│                       Agent 框架全景图                            │
├──────────────┬───────────┬──────────┬──────────┬──────────────────┤
│ 框架         │ 类型      │ 语言     │ 特色     │ 适合场景         │
├──────────────┼───────────┼──────────┼──────────┼──────────────────┤
│ LangChain    │ 通用框架  │ Python   │ 生态最大 │ 快速原型          │
│ LangGraph    │ 工作流    │ Python   │ 图编排   │ 复杂流程          │
│ CrewAI       │ 多Agent   │ Python   │ 角色分工 │ 团队协作          │
│ AutoGen      │ 多Agent   │ Python   │ 微软     │ 对话式多Agent     │
│ SemanticKernel│ 通用     │ C#/Py    │ 微软     │ 企业集成          │
│ Dify         │ 低代码    │ Web UI   │ 可视化   │ 非技术人员        │
│ Coze         │ 低代码    │ Web UI   │ 字节     │ 快速搭建          │
│ FastGPT      │ RAG平台   │ Web UI   │ 知识库   │ 企业知识库        │
│ RAGFlow      │ RAG平台   │ Web UI   │ 文档解析 │ 企业文档          │
│ Flowise      │ 低代码    │ Web UI   │ 开源     │ 可视化流程        │
│ n8n          │ 自动化    │ Web UI   │ 通用     │ 工作流自动化      │
│ Haystack     │ 搜索RAG   │ Python   │ 企业级   │ 搜索系统          │
│ LlamaIndex   │ RAG框架   │ Python   │ 数据     │ 数据索引          │
│ OpenAI Swarm │ 多Agent   │ Python   │ 轻量     │ 实验/学习         │
│ smol-agent   │ 轻量Agent │ Python   │ <1000行  │ 学习原理          │
│ BabyAGI      │ 任务驱动  │ Python   │ 自主     │ 研究探索          │
│ AutoGPT      │ 自主Agent │ Python   │ 综合     │ 复杂任务          │
│ MetaGPT      │ 软件公司  │ Python   │ 角色     │ 软件开发          │
│ ChatDev      │ 软件公司  │ Python   │ 对话式   │ 软件开发          │
└──────────────┴───────────┴──────────┴──────────┴──────────────────┘
"""
print(FRAMEWORKS)

print("=" * 60)
print("🔧 Demo: 框架分类与选型")
print("=" * 60)

class FrameworkSelector:
    """Agent 框架选型助手"""

    categories = {
        "开发框架": ["LangChain", "LangGraph", "LlamaIndex"],
        "多Agent": ["CrewAI", "AutoGen", "MetaGPT", "ChatDev"],
        "低代码": ["Dify", "Coze", "Flowise"],
        "RAG平台": ["FastGPT", "RAGFlow", "Haystack"],
        "学习研究": ["OpenAI Swarm", "smol-agent", "BabyAGI", "AutoGPT"],
    }

    @staticmethod
    def recommend(needs):
        """根据需求推荐框架"""
        scores = {}
        for cat, frameworks in FrameworkSelector.categories.items():
            for fw in frameworks:
                score = 0
                if "快速" in needs: score += 1
                if "多Agent" in needs and fw in ["CrewAI", "AutoGen", "MetaGPT"]: score += 2
                if "工作流" in needs and fw in ["LangGraph", "n8n"]: score += 2
                if "低代码" in needs and fw in ["Dify", "Coze", "Flowise"]: score += 2
                if "RAG" in needs and fw in ["FastGPT", "RAGFlow", "LlamaIndex"]: score += 2
                if score > 0:
                    scores[fw] = score
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)

# 测试
print("\n🧪 选型示例:")
cases = ["快速搭建RAG知识库", "开发多Agent协作系统", "低代码构建客服"]
for case in cases:
    print(f"\n  需求: {case}")
    recs = FrameworkSelector.recommend(case)
    for fw, score in recs[:3]:
        print(f"    → {fw} (匹配度: {score})")

print("\n" + "=" * 60)
print("🔧 Demo: 各框架核心代码对比")
print("=" * 60)

FRAMEWORK_CODE = """
# === LangChain Agent ===
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool

@tool
def my_tool(x): return x
agent = create_react_agent(llm, [my_tool], prompt)
executor = AgentExecutor(agent=agent, tools=[my_tool])

# === CrewAI ===
from crewai import Agent, Task, Crew
researcher = Agent(role="研究员", goal="研究", llm=llm)
task = Task(description="研究RAG", agent=researcher)
crew = Crew(agents=[researcher], tasks=[task])
crew.kickoff()

# === AutoGen ===
from autogen import AssistantAgent, UserProxyAgent
assistant = AssistantAgent("assistant", llm_config={"config_list": [{"model": "qwen2:7b"}]})
user = UserProxyAgent("user", code_execution_config=False)
user.initiate_chat(assistant, message="帮我研究RAG")

# === Dify (低代码) ===
# Web UI 操作: 拖拽节点 → 配置 → 发布API
# 节点: LLM / 知识库 / 工具 / 代码 / 条件分支

# === LlamaIndex ===
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
docs = SimpleDirectoryReader("./data").load_data()
index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()
response = query_engine.query("RAG是什么")
"""
print(FRAMEWORK_CODE)

print("\n✅ Agent 框架对比完成！")
