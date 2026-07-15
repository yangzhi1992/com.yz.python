"""
06-inter-agent: Inter-Agent 面向 Agent 间通信的协议
=======================================================
学习内容: Agent 间通信模式、消息路由、协作协议、A2A 协议
"""

print("=" * 60)
print("📚 Inter-Agent 面向 Agent 间通信的协议")
print("=" * 60)

INTER_AGENT = """
┌────────────────────────────────────────────────────────────┐
│           Inter-Agent Protocol (IAP)                       │
│           面向 Agent 间通信的标准化协议                     │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  通信模式:                                                 │
│                                                            │
│  1. 点对点 (Peer-to-Peer)                                 │
│     Agent A ──────消息──────→ Agent B                      │
│                                                            │
│  2. 广播 (Broadcast)                                      │
│     Agent A ──────消息──────→ Agent B                      │
│                      ├──────→ Agent C                      │
│                      └──────→ Agent D                      │
│                                                            │
│  3. 发布-订阅 (Pub/Sub)                                   │
│     Agent A → [消息队列] → 订阅者 Agent B/C                │
│                                                            │
│  4. 请求-响应 (Request-Reply)                             │
│     Agent A → 请求 → Agent B → 响应 → Agent A              │
│                                                            │
│  5. 协商 (Negotiation)                                    │
│     Agent A ↔ Agent B ↔ Agent C (多方讨论)                │
│                                                            │
│  代表协议:                                                 │
│  ├── Google Agent-to-Agent (A2A)                          │
│  ├── OpenAI Function Calling (工具间通信)                  │
│  └── AutoGen 对话协议 (微软)                              │
└────────────────────────────────────────────────────────────┘
"""
print(INTER_AGENT)

print("\n" + "=" * 60)
print("🔧 Demo: Agent 间通信协议实现")
print("=" * 60)

# ============ 1. 消息协议 ============
print("\n📌 1. Agent 间标准消息协议")
print("-" * 40)

class AgentMessage:
    """Agent 间通信的标准消息格式"""

    def __init__(self, sender, receiver, msg_type, payload, msg_id=None):
        import uuid
        self.msg_id = msg_id or str(uuid.uuid4())[:8]
        self.sender = sender
        self.receiver = receiver
        self.msg_type = msg_type  # request / response / broadcast / error
        self.payload = payload
        self.timestamp = time.time()

    def to_dict(self):
        return {
            "protocol": "inter-agent-v1",
            "msg_id": self.msg_id,
            "sender": self.sender,
            "receiver": self.receiver,
            "type": self.msg_type,
            "payload": self.payload,
            "timestamp": self.timestamp,
        }

import time

# ============ 2. 消息路由器 ============
print("\n📌 2. Agent 消息路由器")
print("-" * 40)

class AgentMessageRouter:
    """Agent 消息路由器 — 负责消息分发"""

    def __init__(self):
        self.agents = {}
        self.message_log = []

    def register(self, agent_id, agent_instance):
        self.agents[agent_id] = agent_instance
        print(f"  注册: {agent_id}")

    def route(self, message):
        """路由消息到指定 Agent"""
        self.message_log.append(message)

        receiver = message.receiver
        if receiver == "broadcast":
            # 广播
            results = []
            for aid, agent in self.agents.items():
                if aid != message.sender:
                    result = agent.receive(message)
                    results.append({aid: result})
            return results

        elif receiver in self.agents:
            return self.agents[receiver].receive(message)

        else:
            return {"error": f"Agent '{receiver}' 不存在"}

    def get_log(self, count=5):
        return self.message_log[-count:]

# ============ 3. 标准 Agent ============
print("\n📌 3. 支持 Inter-Agent 通信的标准 Agent")
print("-" * 40)

class InterAgent:
    """支持 Agent 间通信的 Agent"""

    def __init__(self, agent_id, name, role):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.router = None
        self.knowledge = {}

    def connect(self, router):
        self.router = router
        router.register(self.agent_id, self)

    def send(self, receiver, msg_type, payload):
        """发送消息给另一个 Agent"""
        msg = AgentMessage(self.agent_id, receiver, msg_type, payload)
        if self.router:
            return self.router.route(msg)
        return None

    def broadcast(self, payload):
        """广播消息"""
        return self.send("broadcast", "broadcast", payload)

    def receive(self, message):
        """接收消息"""
        msg_type = message.msg_type
        payload = message.payload

        print(f"    [{self.name}] 收到来自 [{message.sender}] 的消息: {msg_type}")

        if msg_type == "request":
            return self.handle_request(message.sender, payload)
        elif msg_type == "response":
            return self.handle_response(message.sender, payload)
        elif msg_type == "broadcast":
            return self.handle_broadcast(message.sender, payload)
        elif msg_type == "negotiate":
            return self.handle_negotiate(message.sender, payload)
        elif msg_type == "ping":
            return {"status": "alive", "agent": self.agent_id}
        return {"error": "未知消息类型"}

    def handle_request(self, sender, payload):
        """处理请求"""
        action = payload.get("action")
        if action == "query":
            return {"result": f"[{self.name}] 查询结果: {payload.get('question')}"}
        elif action == "execute":
            return {"result": f"[{self.name}] 执行: {payload.get('task')}"}
        elif action == "info":
            return {"agent_id": self.agent_id, "name": self.name, "role": self.role}
        return {"result": f"[{self.name}] 已收到请求"}

    def handle_response(self, sender, payload):
        return {"status": "ok"}

    def handle_broadcast(self, sender, payload):
        print(f"      → 广播内容: {payload.get('message', '')[:50]}...")
        return {"status": "received"}

    def handle_negotiate(self, sender, payload):
        return {"status": "ok", "agree": True}

# ============ 测试通信 ============
print("\n🧪 Agent 间通信:")
router = AgentMessageRouter()

# 创建 Agent 们
agent_cs = InterAgent("cs_001", "客服Agent", "客服")
agent_trans = InterAgent("trans_001", "翻译Agent", "翻译")
agent_ana = InterAgent("ana_001", "分析Agent", "数据分析")
agent_pm = InterAgent("pm_001", "管理Agent", "项目经理")

for agent in [agent_cs, agent_trans, agent_ana, agent_pm]:
    agent.connect(router)

# 1. 点对点: 客服 → 翻译
print("\n📌 点对点通信:")
result = agent_cs.send("trans_001", "request", {
    "action": "query",
    "question": "翻译 'Hello World' 到中文"
})
print(f"  结果: {result}")

# 2. 广播: 管理员广播通知
print("\n📌 广播通信:")
result = agent_pm.broadcast({"message": "系统升级通知: 今晚2点维护"})

# 3. 管理器-工作者: PM 分配任务
print("\n📌 管理器-工作者模式:")
result = agent_pm.send("ana_001", "request", {
    "action": "execute",
    "task": "分析Q3销售数据"
})
print(f"  结果: {result}")

# ============ A2A 协议 ============
print("\n" + "=" * 60)
print("🔧 Demo: Google Agent-to-Agent (A2A) 协议")
print("=" * 60)

A2A_PROTOCOL = """
┌────────────────────────────────────────────────────────────┐
│  Google Agent-to-Agent (A2A) 协议                          │
│                                                            │
│  目标: 不同厂商的 Agent 可以互相发现、通信、协作            │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  A2A 核心组件:                                       │  │
│  │                                                      │  │
│  │  Agent Card — Agent 的名片                           │  │
│  │    {                                                  │  │
│  │      "name": "翻译Agent",                             │  │
│  │      "description": "支持100+语言翻译",               │  │
│  │      "capabilities": ["翻译", "语言检测"],            │  │
│  │      "url": "https://api.example.com/agent",          │  │
│  │      "price": 0.02,                                   │  │
│  │      "rating": 4.8                                    │  │
│  │    }                                                  │  │
│  │                                                      │  │
│  │  通信流程:                                            │  │
│  │  1. Agent A 查询 Agent Card 发现 Agent B              │  │
│  │  2. Agent A 发送标准化请求给 Agent B                   │  │
│  │  3. Agent B 处理并返回标准化响应                       │  │
│  │  4. 双方更新上下文                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  A2A vs MCP:                                               │
│  ├── MCP: 面向上下文，Agent ↔ 工具/资源                     │
│  └── A2A: 面向通信，Agent ↔ Agent                         │
└────────────────────────────────────────────────────────────┘
"""
print(A2A_PROTOCOL)

class AgentCard:
    """Agent 名片 (A2A 协议)"""

    def __init__(self, agent_id, name, desc, capabilities, endpoint, price=0.01):
        self.agent_id = agent_id
        self.name = name
        self.description = desc
        self.capabilities = capabilities
        self.endpoint = endpoint
        self.price = price
        self.rating = 5.0

    def to_dict(self):
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities,
            "endpoint": self.endpoint,
            "price": self.price,
            "rating": self.rating,
        }

class AgentDiscovery:
    """Agent 发现服务"""

    def __init__(self):
        self.cards = {}

    def publish(self, card):
        self.cards[card.agent_id] = card
        print(f"  发布 Agent Card: {card.name}")

    def discover(self, capability=None, max_price=None):
        results = []
        for card in self.cards.values():
            if capability and capability not in card.capabilities:
                continue
            if max_price and card.price > max_price:
                continue
            results.append(card)
        return results

    def get_card(self, agent_id):
        return self.cards.get(agent_id)

# 测试 A2A
print("\n🧪 A2A Agent 发现与协作:")
discovery = AgentDiscovery()

# 发布 Agent 名片
discovery.publish(AgentCard("trans_001", "翻译专家", "支持100+语言", ["翻译", "语言检测"], "http://trans-api", 0.02))
discovery.publish(AgentCard("search_001", "搜索专家", "搜索互联网知识", ["搜索", "知识检索"], "http://search-api", 0.01))
discovery.publish(AgentCard("data_001", "数据分析师", "数据分析与可视化", ["分析", "报表", "图表"], "http://data-api", 0.05))

# 发现翻译 Agent
results = discovery.discover(capability="翻译")
print(f"\n  发现 '翻译' 能力的 Agent:")
for card in results:
    print(f"    → {card.name} (¥{card.price}/次, 评分:{card.rating})")

# Agent A 通过 A2A 协议与 Agent B 协作
class A2AClient:
    """A2A 协议客户端"""

    def __init__(self, discovery):
        self.discovery = discovery

    def call_agent(self, agent_id, action, params):
        card = self.discovery.get_card(agent_id)
        if not card:
            return {"error": "Agent 未找到"}

        print(f"\n  呼叫 [{card.name}]: {action}")
        print(f"    能力: {card.capabilities}")
        print(f"    费用: ¥{card.price}")

        # 模拟 A2A 通信
        return {
            "status": "ok",
            "from": card.name,
            "result": f"[A2A] {card.name} 执行 '{action}' 完成",
            "cost": card.price,
        }

a2a = A2AClient(discovery)
result = a2a.call_agent("trans_001", "translate", {"text": "Hello", "target": "zh"})
print(f"  响应: {result}")

print("\n✅ Inter-Agent 通信协议完成！")
