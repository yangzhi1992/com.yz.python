"""
04-standard-protocols: 标准化协议三大优势
=============================================
学习内容: 互操作性、可扩展性、维护便利性
"""

print("=" * 60)
print("📚 标准化协议三大优势")
print("=" * 60)

PROTOCOL_ADVANTAGES = """
┌────────────────────────────────────────────────────────────┐
│               Agent 标准化协议                              │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  标准化协议 = Agent 世界的"HTTP协议"                  │  │
│  │  定义 Agent 之间如何通信、交互、协作                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  三大优势:                                                 │
│  ┌──────────────┬─────────────────────────────────────────┐│
│  │ 互操作性      │ 不同厂商Agent可协作，打破技术壁垒      ││
│  ├──────────────┼─────────────────────────────────────────┤│
│  │ 可扩展性      │ 新Agent通过标准接口快速接入            ││
│  ├──────────────┼─────────────────────────────────────────┤│
│  │ 维护便利性    │ 统一标准让监控、调试更简单             ││
│  └──────────────┴─────────────────────────────────────────┘│
│                                                            │
└────────────────────────────────────────────────────────────┘
"""
print(PROTOCOL_ADVANTAGES)

print("\n" + "=" * 60)
print("🔧 Demo: 三大优势实现")
print("=" * 60)

# ============ 1. 互操作性 ============
print("\n📌 1. 互操作性 (Interoperability)")
print("-" * 40)

INTEROP = """
│  问题: Agent A 是公司X开发的，Agent B 是公司Y开发的       │
│        它们使用不同的API格式、不同的数据格式               │
│        无法直接协作                                       │
│                                                           │
│  解决方案: 标准化协议                                    │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Agent 统一接口规范：                                │  │
│  │                                                      │  │
│  │  POST /agent/execute                                 │  │
│  │  {                                                    │  │
│  │    "protocol_version": "1.0",   ← 协议版本           │  │
│  │    "agent_id": "客服A",          ← 目标 Agent         │  │
│  │    "action": "process",          ← 动作               │  │
│  │    "input": {"text": "你好"},    ← 统一输入格式       │  │
│  │    "context": {...}              ← 统一上下文格式     │  │
│  │  }                                                    │  │
│  │                                                      │  │
│  │  → {"status": "ok", "output": {...}}                 │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                           │
│  效果:                                                    │
│  ✅ 任意厂商的 Agent 只要实现统一接口即可互操作            │
│  ✅ 阿里客服Agent + 腾讯翻译Agent + 百度搜索Agent         │
"""
print(INTEROP)

class UnifiedAgentAdapter:
    """统一 Agent 适配器 — 实现互操作性"""

    def __init__(self, agent_id, agent_name, vendor):
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.vendor = vendor
        self.capabilities = []

    def standard_execute(self, request):
        """标准化的执行接口"""
        # 校验协议版本
        if request.get("protocol_version") != "1.0":
            return {"status": "error", "msg": "不支持的协议版本"}

        action = request.get("action")
        if action not in self.get_actions():
            return {"status": "error", "msg": f"不支持的动作: {action}"}

        # 执行
        result = self._execute_action(action, request.get("input", {}))
        return {
            "status": "ok",
            "output": result,
            "agent_id": self.agent_id,
            "vendor": self.vendor,
        }

    def get_actions(self):
        return ["process", "health", "capabilities"]

    def _execute_action(self, action, input_data):
        if action == "health":
            return {"status": "healthy", "load": 0.5}
        if action == "capabilities":
            return {"capabilities": self.capabilities}
        return self.process(input_data)

    def process(self, input_data):
        raise NotImplementedError

# 不同厂商的 Agent 实现统一接口
class VendorAServiceAgent(UnifiedAgentAdapter):
    def __init__(self):
        super().__init__("cs_001", "金牌客服", "阿里云")
        self.capabilities = ["客服", "售后", "投诉"]

    def process(self, input_data):
        return {"reply": f"[阿里客服] 已处理: {input_data.get('text', '')}"}

class VendorBTranslationAgent(UnifiedAgentAdapter):
    def __init__(self):
        super().__init__("trans_001", "翻译专家", "腾讯")
        self.capabilities = ["翻译", "语言转换"]

    def process(self, input_data):
        return {"reply": f"[腾讯翻译] 翻译结果: {input_data.get('text', '')}"}

# 通过统一接口协作
print("\n🧪 互操作性演示:")
agent_a = VendorAServiceAgent()
agent_b = VendorBTranslationAgent()

req = {"protocol_version": "1.0", "action": "process", "input": {"text": "我想退货"}}
res_a = agent_a.standard_execute(req)
print(f"  阿里 Agent: {res_a['output']}")

req2 = {"protocol_version": "1.0", "action": "process", "input": {"text": "Hello, how are you?"}}
res_b = agent_b.standard_execute(req2)
print(f"  腾讯 Agent: {res_b['output']}")

# ============ 2. 可扩展性 ============
print("\n📌 2. 可扩展性 (Extensibility)")
print("-" * 40)

class ProtocolPlugin:
    """标准化协议插件 — 实现可扩展性"""

    def __init__(self):
        self.plugins = {}

    def register(self, name, plugin_class):
        """注册新 Agent 插件"""
        self.plugins[name] = plugin_class
        print(f"  注册插件: {name}")

    def create(self, name, *args, **kwargs):
        """创建 Agent 实例"""
        if name not in self.plugins:
            raise ValueError(f"未知插件: {name}")
        instance = self.plugins[name](*args, **kwargs)
        # 自动包装为标准接口
        return self._wrap_standard(instance)

    def _wrap_standard(self, instance):
        """自动包装为标准接口"""
        if not hasattr(instance, "standard_execute"):
            # 动态添加标准方法
            def standard_execute(request):
                action = request.get("action")
                if action == "process":
                    return {
                        "status": "ok",
                        "output": instance.handle(request.get("input", {})),
                        "agent_id": getattr(instance, "agent_id", "unknown"),
                    }
                return {"status": "error", "msg": "未知动作"}
            instance.standard_execute = standard_execute
        return instance

# 新 Agent 只需要实现 handle 方法即可接入
class NewSearchAgent:
    def __init__(self):
        self.agent_id = "search_002"

    def handle(self, input_data):
        return {"results": f"搜索: {input_data.get('query', '')}", "count": 5}

class NewImageAgent:
    def __init__(self):
        self.agent_id = "img_001"

    def handle(self, input_data):
        return {"image_url": "https://example.com/generated.png", "style": input_data.get("style")}

print("\n🧪 可扩展性演示:")
registry = ProtocolPlugin()

# 注册新 Agent（无需改任何现有代码）
registry.register("search", NewSearchAgent)
registry.register("image_gen", NewImageAgent)

# 创建并使用
search_agent = registry.create("search")
result = search_agent.standard_execute({
    "protocol_version": "1.0",
    "action": "process",
    "input": {"query": "RAG技术"}
})
print(f"  新搜索Agent: {result['output']}")

img_agent = registry.create("image_gen")
result = img_agent.standard_execute({
    "protocol_version": "1.0",
    "action": "process",
    "input": {"style": "水墨画"}
})
print(f"  新图像Agent: {result['output']}")

print("\n  ✅ 新增 Agent 无需修改现有系统，即插即用")

# ============ 3. 维护便利性 ============
print("\n📌 3. 维护便利性 (Maintainability)")
print("-" * 40)

class AgentMonitor:
    """统一监控系统 — 基于标准协议"""

    def __init__(self):
        self.logs = []

    def inspect(self, agent, request):
        """统一检查 Agent"""
        # 1. 健康检查
        health = agent.standard_execute({
            "protocol_version": "1.0",
            "action": "health"
        })

        # 2. 能力查询
        caps = agent.standard_execute({
            "protocol_version": "1.0",
            "action": "capabilities"
        })

        # 3. 执行
        start = time.time()
        result = agent.standard_execute(request)
        elapsed = time.time() - start

        self.logs.append({
            "agent": getattr(agent, "agent_id", "unknown"),
            "action": request.get("action"),
            "health": health["output"],
            "capabilities": caps.get("output", {}).get("capabilities", []),
            "elapsed": f"{elapsed:.3f}s",
            "result_status": result["status"],
        })

        return {"health": health, "capabilities": caps, "result": result}

    def report(self):
        print(f"\n  📊 监控报告:")
        print(f"  {'Agent':<20} {'动作':<15} {'耗时':<10} {'状态'}")
        print(f"  {'-'*55}")
        for log in self.logs:
            print(f"  {log['agent']:<20} {log['action']:<15} {log['elapsed']:<10} {log['result_status']}")

    def debug(self, agent_id):
        """调试特定 Agent"""
        agent_logs = [l for l in self.logs if l["agent"] == agent_id]
        print(f"\n  🔍 调试 Agent '{agent_id}':")
        for i, log in enumerate(agent_logs):
            print(f"    调用 #{i+1}: {log['action']} | {log['elapsed']} | {log['result_status']}")

import time

print("\n🧪 维护便利性演示:")
monitor = AgentMonitor()

# 检查并执行多个 Agent
for agent in [agent_a, search_agent]:
    monitor.inspect(agent, {
        "protocol_version": "1.0",
        "action": "process",
        "input": {"text": "测试"}
    })

monitor.report()

print("\n✅ 标准化协议三大优势完成！")
