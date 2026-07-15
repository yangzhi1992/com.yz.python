"""
10-agent-lowcode: 基于 Dify / Coze 的低代码 Agent 搭建
=========================================================
学习内容: 低代码平台对比、可视化搭建、工作流编排
"""

print("=" * 60)
print("📚 低代码 Agent 搭建 - 学习路线")
print("=" * 60)

LOWCODE_OVERVIEW = """
┌─────────────────────────────────────────────────────────────┐
│              低代码 Agent 平台对比                           │
├──────────────┬───────────────┬───────────────┬──────────────┤
│  维度        │  Dify         │  Coze          │  Flowise    │
├──────────────┼───────────────┼───────────────┼──────────────┤
│ 开发商       │ 开源社区      │ 字节跳动      │ 开源社区     │
│ 部署方式     │ Docker 私有   │ 云服务         │ Docker 私有  │
│ 模型接入     │ OpenAI/Ollama │ 豆包/OpenAI    │ 20+ 种       │
│ 知识库       │ ✅            │ ✅             │ ❌           │
│ 工作流       │ ✅ 图编排     │ ✅ 线性        │ ✅ 图编排    │
│ 插件系统     │ ✅            │ ✅ 丰富        │ ✅          │
│ 发布渠道     │ API/Web       │ 飞书/微信/Web  │ API/Web     │
│ 开源         │ ✅ Apache 2.0 │ ❌             │ ✅ Apache 2.0│
│ 难度         │ ⭐⭐          │ ⭐             │ ⭐⭐⭐      │
└──────────────┴───────────────┴───────────────┴──────────────┘
"""
print(LOWCODE_OVERVIEW)

print("\n" + "=" * 60)
print("🔧 Demo: Dify / Coze 核心概念与配置")
print("=" * 60)

# ============ Dify 工作流 ============
print("\n📌 Dify 低代码 Agent 搭建")
print("-" * 40)

DIFY_GUIDE = """
┌────────────────────────────────────────────────────────────────┐
│  Dify Agent 搭建流程                                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. 创建 Agent 应用                                            │
│     → 选择 "Agent" 类型                                       │
│     → 填写名称、描述                                           │
│                                                                │
│  2. 配置 LLM                                                   │
│     → 选择模型: Ollama/qwen2:7b                                │
│     → 系统提示词: "你是客服助手，负责回答产品问题"               │
│     → 参数: temperature=0.1, max_tokens=2048                  │
│                                                                │
│  3. 添加工具                                                    │
│     → 知识库检索 (绑定知识库)                                   │
│     → 日历查询                                                  │
│     → 天气查询                                                  │
│     → 自定义 API 工具                                           │
│                                                                │
│  4. 配置知识库                                                  │
│     → 上传文档 (PDF/Word/TXT)                                  │
│     → 选择分块策略                                              │
│     → 选择 Embedding 模型                                       │
│                                                                │
│  5. 调试与发布                                                  │
│     → 对话测试                                                  │
│     → 发布 API                                                  │
│     → 嵌入网页 / 对接飞书                                       │
│                                                                │
│  Dify 中的 Agent 类型:                                          │
│    • ReAct Agent: 标准 ReAct 循环                               │
│    • Function Calling Agent: OpenAI 格式                        │
│    • 工作流 Agent: LangGraph 风格的图编排                        │
│                                                                │
│  企业级功能:                                                    │
│    • RBAC 权限控制                                              │
│    • API 调用日志                                               │
│    • 对话标注                                                  │
│    • 模型监控                                                  │
└────────────────────────────────────────────────────────────────┘
"""
print(DIFY_GUIDE)

# ============ Coze ============
print("\n📌 Coze 低代码 Agent 搭建")
print("-" * 40)

COZE_GUIDE = """
┌────────────────────────────────────────────────────────────────┐
│  Coze (扣子) 搭建流程                                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  1. 创建 Bot                                                    │
│     → coze.cn 登录                                             │
│     → 点击 "创建 Bot"                                          │
│     → 填写 Bot 名称和功能介绍                                    │
│                                                                │
│  2. 人设与回复逻辑                                              │
│     → 系统提示词: 角色+任务+约束                                 │
│     → 示例: "你是银行客服助手，专业友好，回答不超过200字"        │
│                                                                │
│  3. 技能配置                                                    │
│     → 知识库: 上传FAQ/产品手册                                  │
│     → 插件: 日历/天气/图片识别/网页搜索                         │
│     → 工作流: 多步骤流程编排                                     │
│     → 对话: 开场白、预设问题                                     │
│                                                                │
│  4. 发布渠道                                                    │
│     → 网页链接                                                  │
│     → 飞书机器人                                                │
│     → 微信客服                                                  │
│     → API                                                      │
│                                                                │
│  Coze vs Dify 差异:                                             │
│    Coze: 上手更快，插件市场丰富，适合快速验证                    │
│    Dify: 开源可自建，工作流更强大，适合企业定制                  │
└────────────────────────────────────────────────────────────────┘
"""
print(COZE_GUIDE)

# ============ 低代码模拟器 ============
print("📌 Demo: 低代码 Agent 构建模拟器")
print("-" * 40)

class LowCodeAgentBuilder:
    """模拟低代码 Agent 搭建"""

    def __init__(self):
        self.config = {
            "name": "",
            "llm": {"model": "qwen2:7b", "temperature": 0.1},
            "prompt": "",
            "knowledge_base": [],
            "tools": [],
            "workflow": [],
            "channels": [],
        }

    def set_name(self, name):
        self.config["name"] = name
        return self

    def set_llm(self, model, temp=0.1):
        self.config["llm"] = {"model": model, "temperature": temp}
        return self

    def set_prompt(self, prompt):
        self.config["prompt"] = prompt
        return self

    def add_knowledge(self, docs):
        self.config["knowledge_base"].extend(docs)
        return self

    def add_tool(self, tool):
        self.config["tools"].append(tool)
        return self

    def add_workflow_step(self, step):
        self.config["workflow"].append(step)
        return self

    def add_channel(self, channel):
        self.config["channels"].append(channel)
        return self

    def build(self):
        print(f"\n  🤖 Agent: {self.config['name']}")
        print(f"  📝 Prompt: {self.config['prompt'][:50]}...")
        print(f"  📚 知识库: {len(self.config['knowledge_base'])}条")
        print(f"  🔧 工具: {', '.join(self.config['tools'])}")
        print(f"  📋 工作流: {len(self.config['workflow'])}步")
        print(f"  📢 渠道: {', '.join(self.config['channels'])}")
        return self.config

# 构建客服 Agent
print("\n🧪 构建客服 Agent:")
builder = LowCodeAgentBuilder()
agent = (builder
    .set_name("智能客服助手")
    .set_llm("qwen2:7b", 0.1)
    .set_prompt("你是银行客服助手，回答问题不超过200字")
    .add_knowledge(["产品FAQ v2.0", "常见问题处理流程"])
    .add_tool("订单查询")
    .add_tool("退款处理")
    .add_tool("知识库检索")
    .add_workflow_step("意图识别")
    .add_workflow_step("知识检索")
    .add_workflow_step("LLM生成")
    .add_channel("网页")
    .add_channel("飞书")
    .build()
)

print("\n✅ 低代码 Agent 完成！")
