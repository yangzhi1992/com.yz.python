"""
AI Agent Demo - 从零实现 ReAct 模式（无第三方框架）
=================================================
知识点：手动实现 Agent 循环，理解 ReAct 核心原理
需要: pip install requests
"""

import requests
import json
import re

OLLAMA_BASE = "http://localhost:11434"
MODEL = "qwen2:7b"


def call_llm(messages):
    """调用 Ollama API"""
    resp = requests.post(f"{OLLAMA_BASE}/api/chat", json={
        "model": MODEL,
        "stream": False,
        "messages": messages,
    })
    return resp.json()["message"]["content"]


# 工具定义
TOOLS = {
    "calculator": {
        "description": "数学计算器，输入JSON: {\"op\":\"add\",\"a\":1,\"b\":2}",
        "exec": lambda args: str(eval(json.loads(args).get("expr", "0")))
    },
    "date_time": {
        "description": "获取当前日期时间",
        "exec": lambda _: __import__("datetime").datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
}

SYSTEM_PROMPT = f"""你是智能助手。可用工具:
{chr(10).join(f'- {k}: {v["description"]}' for k, v in TOOLS.items())}

当需要工具时，回复: TOOL_CALL: 工具名 | 参数JSON
当不需要工具时，直接回复。
"""


def react_agent(user_input):
    """手写 ReAct 循环"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    for i in range(5):
        reply = call_llm(messages)
        print(f"  [{i}] LLM思考: {reply[:80]}...")

        if reply.startswith("TOOL_CALL:"):
            parts = reply.replace("TOOL_CALL:", "").strip().split("|", 1)
            tool_name = parts[0].strip()
            args = parts[1].strip() if len(parts) > 1 else "{}"

            if tool_name in TOOLS:
                result = TOOLS[tool_name]["exec"](args)
                print(f"  🔧 工具[{tool_name}] → {result}")
                messages.append({"role": "assistant", "content": reply})
                messages.append({"role": "tool", "content": f"结果: {result}"})
            else:
                return f"未知工具: {tool_name}"
        else:
            return reply

    return "已达最大迭代次数"


if __name__ == "__main__":
    print("🤖 手写 ReAct Agent 测试")
    while True:
        q = input("\n👤 你: ")
        if q.lower() in ("exit", "q"): break
        print("🤖:", react_agent(q))
