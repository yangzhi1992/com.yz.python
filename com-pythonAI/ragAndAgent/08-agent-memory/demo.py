"""
08-agent-memory: Agent 的 8 种记忆系统
===========================================
学习内容: 记忆类型、实现方式、源码示例
"""

print("=" * 60)
print("📚 Agent 记忆系统 - 8 种记忆")
print("=" * 60)

MEMORY_TYPES = """
┌──────┬──────────────────┬────────────────────────┬──────────────────┐
│  #   │ 记忆类型          │ 描述                   │ 实现方式          │
├──────┼──────────────────┼────────────────────────┼──────────────────┤
│  1   │ 缓冲区记忆        │ 保留最近 N 轮对话       │ 列表滑动窗口       │
│      │ Buffer Memory    │                        │ deque(maxlen=N)   │
├──────┼──────────────────┼────────────────────────┼──────────────────┤
│  2   │ 摘要记忆          │ 总结历史对话并保留摘要   │ LLM 定期汇总       │
│      │ Summary Memory   │                        │ 压缩存储           │
├──────┼──────────────────┼────────────────────────┼──────────────────┤
│  3   │ 向量记忆          │ 用向量检索历史相关对话   │ ChromaDB + BGE    │
│      │ Vector Memory    │                        │ 语义搜索           │
├──────┼──────────────────┼────────────────────────┼──────────────────┤
│  4   │ 实体记忆          │ 提取和记住实体信息       │ 知识图谱           │
│      │ Entity Memory    │                        │ 三元组存储         │
├──────┼──────────────────┼────────────────────────┼──────────────────┤
│  5   │ 知识图谱记忆      │ 结构化知识关系           │ Neo4j / NetworkX  │
│      │ KG Memory        │                        │ 图查询             │
├──────┼──────────────────┼────────────────────────┼──────────────────┤
│  6   │ 会话记忆          │ 完整对话历史             │ 数据库存储         │
│      │ Conversation     │                        │ SQL/NoSQL         │
├──────┼──────────────────┼────────────────────────┼──────────────────┤
│  7   │ 工作记忆          │ 当前任务临时状态         │ 字典 / 状态机      │
│      │ Working Memory   │                        │ 临时变量           │
├──────┼──────────────────┼────────────────────────┼──────────────────┤
│  8   │ 长期记忆          │ 跨会话持久化知识         │ 文件 / 数据库      │
│      │ Long-term Memory │                        │ 向量库             │
└──────┴──────────────────┴────────────────────────┴──────────────────┘
"""
print(MEMORY_TYPES)

print("\n" + "=" * 60)
print("🔧 Demo: 8 种记忆系统实现")
print("=" * 60)

# 1. 缓冲区记忆
print("\n📌 记忆1: Buffer Memory (滑动窗口)")
print("-" * 40)

from collections import deque

class BufferMemory:
    def __init__(self, maxlen=5):
        self.history = deque(maxlen=maxlen)

    def add(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_recent(self, n=3):
        return list(self.history)[-n:]

    def to_prompt(self):
        return "\n".join(f"{m['role']}: {m['content']}" for m in self.history)

bm = BufferMemory(3)
bm.add("user", "你好")
bm.add("assistant", "你好，我是AI助手")
bm.add("user", "RAG是什么")
print(f"  最近2条: {bm.get_recent(2)}")

# 2. 摘要记忆
print("\n📌 记忆2: Summary Memory")
print("-" * 40)

class SummaryMemory:
    def __init__(self, max_tokens=500):
        self.full_history = []
        self.summary = ""
        self.max_tokens = max_tokens

    def add(self, role, content):
        self.full_history.append({"role": role, "content": content})
        # 超过阈值时压缩
        if len(str(self.full_history)) > self.max_tokens:
            self.compress()

    def compress(self):
        self.summary = f"[摘要] 共{len(self.full_history)}条对话记录..."
        self.full_history = []

    def get(self):
        if self.summary:
            return [{"role": "system", "content": self.summary}] + self.full_history
        return self.full_history

sm = SummaryMemory(200)
for i in range(10):
    sm.add("user", f"问题{i}")
    sm.add("assistant", f"回答{i}")
print(f"  压缩后: {len(sm.get())}条消息")
print(f"  摘要: {sm.summary}")

# 3. 向量记忆
print("\n📌 记忆3: Vector Memory")
print("-" * 40)

class VectorMemory:
    def __init__(self):
        self.memories = []

    def add(self, text, metadata=None):
        self.memories.append({"text": text, "metadata": metadata or {}})

    def search(self, query, k=2):
        # 模拟语义检索
        scores = []
        for m in self.memories:
            overlap = len(set(query) & set(m["text"]))
            scores.append(overlap / max(len(set(query)), 1))
        idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [self.memories[i] for i in idx]

vm = VectorMemory()
vm.add("用户喜欢Python编程", {"user": "张三"})
vm.add("用户从事AI开发工作", {"user": "张三"})
vm.add("用户最近在学习RAG技术", {"user": "李四"})
results = vm.search("AI开发")
print(f"  查询 'AI开发' 相关记忆:")
for r in results:
    print(f"    → {r['text']}")

# 4-8: 概念
print("\n📌 记忆4-8: 快速参考")
print("-" * 40)

MORE_MEMORY = """
记忆4: Entity Memory (实体记忆)
  ┌─────────────────────────────────┐
  │ 实体提取: "张三今年25岁"         │
  │ → {实体: "张三", 属性: "年龄",   │
  │    值: "25"}                    │
  │ → 下次提到"张三"时，自动注入年龄  │
  └─────────────────────────────────┘

记忆5: Knowledge Graph Memory
  {"head": "Transformer", "rel": "包含", "tail": "Attention"}
  → 检索 "Transformer" → 返回相关所有关系

记忆6: Conversation Memory (完整历史)
  SQL/Redis 存储 → 按session_id查询
  → 支持分页、时间范围过滤

记忆7: Working Memory (工作记忆)
  Agent = {"task": "计算...", "step": 2, "result": None}
  每一步更新状态 → 完成后清除

记忆8: Long-term Memory (长期记忆)
  跨天持久化: SQLite / ChromaDB / 文件
  每天启动时加载 → 持续积累
"""
print(MORE_MEMORY)

# 综合演示: 多级记忆系统
print("\n🧪 综合: 多级记忆系统架构")

class AgentMemorySystem:
    """完整的 Agent 记忆系统架构"""

    def __init__(self):
        self.working = {}         # 工作记忆 (当前任务)
        self.buffer = BufferMemory(10)  # 短期 (滑动窗口)
        self.vector = VectorMemory()    # 长期 (向量检索)
        self.entities = {}             # 实体记忆

    def update_working(self, key, value):
        self.working[key] = value

    def add_dialog(self, role, content):
        self.buffer.add(role, content)
        # 提取实体
        if "叫" in content or "是" in content:
            self.entities[content[:10]] = content

    def get_context(self, query):
        ctx = {"working": self.working,
               "recent": self.buffer.get_recent(3),
               "entities": self.entities}
        # 向量检索相关记忆
        related = self.vector.search(query, 2)
        ctx["related"] = related
        return ctx

ams = AgentMemorySystem()
ams.update_working("current_task", "客户咨询")
ams.add_dialog("user", "我叫张三，想咨询RAG技术")
ctx = ams.get_context("RAG介绍")
print(f"  工作记忆: {ctx['working']}")
print(f"  实体记忆: {ctx['entities']}")
print(f"  近期对话: {len(ctx['recent'])}条")

print("\n✅ Agent 记忆系统完成！")
