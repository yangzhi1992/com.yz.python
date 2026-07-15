"""
05-context-oriented: Context-Oriented 面向上下文的协议
=========================================================
学习内容: 上下文传递协议、共享上下文、上下文生命周期
"""

print("=" * 60)
print("📚 Context-Oriented 面向上下文的协议")
print("=" * 60)

CONTEXT_ORIENTED = """
┌────────────────────────────────────────────────────────────┐
│           Context-Oriented Protocol (COP)                  │
│           面向上下文的 Agent 通信协议                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  核心理念: 上下文是 Agent 通信的核心载体                    │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  每次 Agent 调用都携带上下文                            │  │
│  │                                                      │  │
│  │  {                                                     │  │
│  │    "context": {                        ← 共享上下文    │  │
│  │      "session_id": "sess_001",         会话ID          │  │
│  │      "user": {"id": "u1", "name": "张三"}, 用户信息    │  │
│  │      "history": [...],                  对话历史       │  │
│  │      "metadata": {...},                 元数据         │  │
│  │      "state": {...}                     当前状态       │  │
│  │    },                                                    │  │
│  │    "action": "...",                                     │  │
│  │    "params": {...}                                      │  │
│  │  }                                                     │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  上下文生命周期:                                            │
│  创建 → 传递 → 更新 → 传递 → 更新 → ... → 销毁             │
│                                                            │
│  关键协议:                                                 │
│  ├── ACP (Agent Communication Protocol)                    │
│  ├── MCP (Model Context Protocol)                          │
│  └── Google Agent-to-Agent                                │
└────────────────────────────────────────────────────────────┘
"""
print(CONTEXT_ORIENTED)

print("\n" + "=" * 60)
print("🔧 Demo: 面向上下文的通信协议")
print("=" * 60)

# ============ 上下文管理器 ============
print("\n📌 1. 上下文管理器 (Context Manager)")
print("-" * 40)

class AgentContext:
    """Agent 上下文 — 贯穿整个 Agent 调用链"""

    def __init__(self, session_id, user=None):
        self.session_id = session_id
        self.user = user or {}
        self.history = []
        self.state = {}
        self.metadata = {}
        self.created_at = None
        self.updated_at = None

    def update(self, key, value):
        self.state[key] = value
        self.updated_at = time.time()

    def add_to_history(self, role, content):
        self.history.append({"role": role, "content": content, "time": time.time()})

    def to_dict(self):
        return {
            "protocol": "context-oriented-v1",
            "session_id": self.session_id,
            "user": self.user,
            "history": self.history[-10:],  # 只保留最近10条
            "state": self.state,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data):
        ctx = cls(data.get("session_id"), data.get("user", {}))
        ctx.history = data.get("history", [])
        ctx.state = data.get("state", {})
        ctx.metadata = data.get("metadata", {})
        return ctx

import time

# ============ 标准协议消息 ============
print("\n📌 2. 标准上下文协议消息")
print("-" * 40)

class ContextMessage:
    """基于上下文的协议消息"""

    def __init__(self, action, params=None, context=None):
        self.protocol_version = "context-oriented-v1"
        self.action = action
        self.params = params or {}
        self.context = context or AgentContext("default")

    def to_dict(self):
        return {
            "protocol_version": self.protocol_version,
            "action": self.action,
            "params": self.params,
            "context": self.context.to_dict(),
        }

    @classmethod
    def from_dict(cls, data):
        ctx = AgentContext.from_dict(data.get("context", {}))
        return cls(data["action"], data.get("params"), ctx)

# ============ 上下文传递 Demo ============
print("\n📌 3. 上下文在 Agent 链中传递")
print("-" * 40)

class ContextAwareAgent:
    """支持上下文协议的 Agent"""

    def __init__(self, name):
        self.name = name

    def handle(self, msg):
        ctx = msg.context
        action = msg.action
        params = msg.params

        print(f"\n  [{self.name}] 收到: action={action}")
        print(f"    会话: {ctx.session_id}")
        print(f"    用户: {ctx.user.get('name', '未知')}")
        print(f"    历史: {len(ctx.history)}条")

        # 处理
        if action == "greet":
            reply = f"你好 {ctx.user.get('name', '朋友')}！我是{self.name}"
        elif action == "query":
            reply = f"查询结果: {params.get('question', '')}"
        elif action == "transfer":
            reply = f"转接至: {params.get('target', '')}"
        else:
            reply = f"[{self.name}] 收到: {params}"

        # 更新上下文
        ctx.add_to_history(self.name, reply)
        ctx.update(f"last_agent_{action}", self.name)

        return ContextMessage("response", {"reply": reply}, ctx)

# 创建上下文
ctx = AgentContext("sess_001", {"id": "u001", "name": "张三", "level": "VIP"})
ctx.add_to_history("user", "你好，我想咨询RAG技术")

# Agent 链传递
print("\n🧪 上下文在 Agent 链中传递:")

# Agent A: 客服
agent_a = ContextAwareAgent("客服Agent")
msg = ContextMessage("greet", {"text": "你好"}, ctx)
resp = agent_a.handle(msg)

# Agent B: 技术专家 (携带 Agent A 更新的上下文)
agent_b = ContextAwareAgent("技术专家Agent")
msg2 = ContextMessage("query", {"question": "RAG原理"}, resp.context)
resp2 = agent_b.handle(msg2)

# Agent C: 销售 (携带全部上下文)
agent_c = ContextAwareAgent("销售Agent")
msg3 = ContextMessage("transfer", {"target": "高级顾问"}, resp2.context)
resp3 = agent_c.handle(msg3)

print(f"\n  最终上下文历史: {len(resp3.context.history)}条")
for h in resp3.context.history:
    print(f"    [{h['role']}] {str(h['content'])[:50]}")

# ============ MCP 协议 ============
print("\n" + "=" * 60)
print("🔧 Demo: MCP (Model Context Protocol) 核心概念")
print("=" * 60)

MCP_PROTOCOL = """
┌────────────────────────────────────────────────────────────┐
│  MCP (Model Context Protocol) — Anthropic 提出的标准      │
│                                                            │
│  面向上下文的标准协议                                      │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  MCP 三大组件                                         │  │
│  │                                                      │  │
│  │  1. Resources (资源)                                  │  │
│  │     Agent 可以访问的外部数据源                         │  │
│  │     文件系统 / 数据库 / API / 知识库                   │  │
│  │                                                      │  │
│  │  2. Tools (工具)                                      │  │
│  │     Agent 可以调用的函数                               │  │
│  │     搜索 / 计算 / 发送 / 查询                          │  │
│  │                                                      │  │
│  │  3. Prompts (提示词模板)                               │  │
│  │     预定义的交互模式                                   │  │
│  │     客服 / 翻译 / 分析                                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  MCP 通信流程:                                             │
│  Host (用户端) ↔ MCP Client ↔ MCP Server (Agent)          │
│                                                            │
│  类似 HTTP 之于 Web，MCP 是 AI Agent 的标准协议            │
└────────────────────────────────────────────────────────────┘
"""
print(MCP_PROTOCOL)

class MCPServer:
    """MCP 协议服务器模拟"""

    def __init__(self, name):
        self.name = name
        self.resources = {}
        self.tools = {}
        self.prompts = {}

    def add_resource(self, name, data):
        self.resources[name] = data

    def add_tool(self, name, func, desc):
        self.tools[name] = {"func": func, "desc": desc}

    def add_prompt(self, name, template):
        self.prompts[name] = template

    def handle_request(self, request):
        method = request.get("method")
        params = request.get("params", {})

        if method == "resources/read":
            name = params.get("name")
            return {"content": self.resources.get(name, "未找到")}

        elif method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})
            if name in self.tools:
                result = self.tools[name]["func"](args)
                return {"content": result}
            return {"error": f"未知工具: {name}"}

        elif method == "prompts/get":
            name = params.get("name")
            return {"content": self.prompts.get(name, "未找到")}

        elif method == "ping":
            return {"status": "ok"}

        return {"error": f"未知方法: {method}"}

print("\n🧪 MCP 模拟:")
mcp = MCPServer("知识库MCP")
mcp.add_resource("doc_001", "RAG检索增强生成技术文档...")
mcp.add_tool("search", lambda p: f"搜索'{p.get('query')}'的结果", "知识搜索")
mcp.add_prompt("qa_prompt", "基于以下知识回答问题...")

resp = mcp.handle_request({
    "method": "tools/call",
    "params": {"name": "search", "arguments": {"query": "RAG原理"}}
})
print(f"  MCP 工具调用: {resp}")

print("\n✅ Context-Oriented 完成！")
