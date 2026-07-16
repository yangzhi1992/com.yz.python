"""
AI Agent Demo (Python)
======================
知识点演示：LLM调用、工具定义、ReAct循环、对话记忆

使用 LangChain 库实现完整的 Agent 模式。
需要: pip install langchain langchain-ollama
"""

# ==================== 1. LLM 调用 ====================
from langchain_ollama import ChatOllama

llm = ChatOllama(model="qwen2:7b", temperature=0.7)
print("✅ LLM 已连接:", llm.model)

# ==================== 2. 工具定义 ====================
from langchain.tools import tool


@tool
def calculator(expression: str) -> str:
    """数学计算器，传入数学表达式如 '2 + 3 * 4'"""
    try:
        # 安全计算（仅允许基本运算）
        allowed = set("0123456789+-*/.() ")
        if not all(c in allowed for c in expression):
            return "错误：表达式包含非法字符"
        result = eval(expression, {"__builtins__": {}}, {})
        return f"计算结果: {result}"
    except Exception as e:
        return f"计算错误: {e}"


@tool
def get_current_time() -> str:
    """获取当前日期和时间"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


print("✅ 已注册工具:", calculator.name, ",", get_current_time.name)

# ==================== 3. Agent 循环（ReAct） ====================
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

tools = [calculator, get_current_time]

# 使用 LangChain Hub 上的 ReAct prompt
prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
)

print("✅ Agent 已创建")

# ==================== 4. 对话测试 ====================
def chat_with_agent():
    print("\n" + "=" * 50)
    print("🤖 Agent 对话测试")
    print("=" * 50)
    print("输入 'exit' 退出, 'clear' 清除记忆\n")

    while True:
        user_input = input("👤 你: ")
        if user_input.lower() in ("exit", "quit", "q"):
            break
        if user_input.lower() == "clear":
            # 注意：LangChain AgentExecutor 默认无记忆
            # 需配合 ConversationBufferMemory 使用
            print("🧹 记忆已清除（需配置 Memory 组件）")
            continue

        response = agent_executor.invoke({"input": user_input})
        print(f"🤖 Agent: {response['output']}\n")


if __name__ == "__main__":
    chat_with_agent()
