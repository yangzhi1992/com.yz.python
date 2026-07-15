"""
01-rag-deep-dive: RAG 技术详解（核心原理与应用）
=================================================
学习内容: RAG完整流程、Naive RAG → Advanced RAG → Modular RAG
"""

print("=" * 60)
print("📚 RAG 技术详解 - 学习路线")
print("=" * 60)

LEARNING = """
【阶段1】RAG 基础概念
  ├── 为什么需要 RAG？
  │   ├── LLM 知识截止日期 (无法知道最新信息)
  │   ├── LLM 幻觉 (编造不存在的知识)
  │   └── 企业私有数据无法训练进模型
  ├── RAG 核心流程
  │   └── 检索 (Retrieval) + 增强 (Augmented) + 生成 (Generation)
  └── RAG vs 微调 vs Prompt 工程
      ├── RAG:    动态外挂知识，适合频繁更新
      ├── 微调:   注入新知识/格式，成本高
      └── Prompt: 零成本，但有限

【阶段2】RAG 三种架构演进
  ┌─────────────────────────────────────────────────────┐
  │ 1. Naive RAG (基础)                                 │
  │    文档 → 分块 → Embedding → 检索 → LLM 生成       │
  │    问题: 检索质量不稳、缺乏上下文                    │
  ├─────────────────────────────────────────────────────┤
  │ 2. Advanced RAG (进阶)                              │
  │    查询重写 + 混合检索 + 重排序 + 上下文压缩        │
  │    优化: 检索前、检索中、检索后 三个环节             │
  ├─────────────────────────────────────────────────────┤
  │ 3. Modular RAG (模块化)                             │
  │    可插拔模块：查询路由 ➜ 检索 ➜ 重写 ➜ 过滤 ➜ 排序 ➜ 生成 │
  │    支持自定义 pipeline                              │
  └─────────────────────────────────────────────────────┘

【阶段3】RAG 核心评估指标
  ├── 检索质量: Hit Rate, MRR, NDCG
  ├── 生成质量: Faithfulness, Answer Relevance
  └── 端到端: 用户满意度、任务完成率
"""
print(LEARNING)

# ============ 三条 RAG 主线实现 ============
print("\n" + "=" * 60)
print("🔧 Demo: RAG 三种架构对比")
print("=" * 60)

import numpy as np

class NaiveRAG:
    """基础 RAG: 文档→分块→检索→生成"""
    def __init__(self):
        self.docs = []
        self.embeddings = []

    def add_docs(self, docs):
        self.docs = docs
        self.embeddings = [np.random.randn(10) for _ in docs]

    def retrieve(self, query, k=2):
        q_vec = np.random.randn(10)
        scores = [np.dot(q_vec, e) for e in self.embeddings]
        idx = np.argsort(scores)[-k:][::-1]
        return [(self.docs[i], scores[i]) for i in idx]

    def query(self, q):
        docs = self.retrieve(q)
        context = "\n".join(d[0] for d in docs)
        return f"[Naive RAG]\n  检索到:\n    {context}\n  生成: 基于以上知识回答: {q}"

class AdvancedRAG:
    """进阶 RAG: 查询重写 + 混合检索 + 重排序"""
    def __init__(self):
        self.docs = []
        self.embeddings = []

    def add_docs(self, docs):
        self.docs = docs
        self.embeddings = [np.random.randn(10) for _ in docs]

    def rewrite_query(self, q):
        """查询重写: 补全/拆解复杂问题"""
        if len(q) < 10:
            return q
        return f"{q} 请提供详细的技术解释和示例"

    def hybrid_search(self, query, k=5):
        """混合检索: 向量 + 关键词"""
        q_vec = np.random.randn(10)
        vec_scores = [np.dot(q_vec, e) for e in self.embeddings]
        # 模拟关键词匹配
        kw_scores = [len([w for w in query.split() if w in d]) * 0.5 for d in self.docs]
        combined = [v + k for v, k in zip(vec_scores, kw_scores)]
        idx = np.argsort(combined)[-k:][::-1]
        return [(self.docs[i], combined[i]) for i in idx]

    def rerank(self, docs, query):
        """重排序: Cross-Encoder 精排"""
        return sorted(docs, key=lambda x: x[1] * np.random.uniform(0.9, 1.1), reverse=True)[:2]

    def query(self, q):
        rewritten = self.rewrite_query(q)
        candidates = self.hybrid_search(rewritten)
        top_docs = self.rerank(candidates, q)
        context = "\n".join(d[0] for d in top_docs)
        return f"[Advanced RAG]\n  原始: {q}\n  重写: {rewritten}\n  精排后:\n    {context}\n  生成: 基于增强检索回答: {q}"

class ModularRAG:
    """模块化 RAG: 可插拔 pipeline"""
    def __init__(self):
        self.modules = {}

    def register(self, name, func):
        self.modules[name] = func

    def pipeline(self, query, module_sequence):
        """按顺序执行模块"""
        state = {"query": query}
        for name in module_sequence:
            if name in self.modules:
                state = self.modules[name](state)
                print(f"    [{name}] → {str(state)[:60]}...")
        return state

# 演示
mr = ModularRAG()
mr.register("query_rewrite", lambda s: {**s, "rewritten": s["query"] + " (技术详解)"})
mr.register("hybrid_search", lambda s: {**s, "candidates": ["结果A", "结果B"]})
mr.register("rerank", lambda s: {**s, "top": s["candidates"][:1]})
mr.register("generate", lambda s: {**s, "answer": f"基于{s['top']}的回答"})

print("\n🧪 Naive RAG:")
n = NaiveRAG()
n.add_docs(["RAG通过检索增强生成减少幻觉", "GraphRAG使用知识图谱结构"])
print(n.query("RAG怎么减少幻觉"))

print("\n🧪 Advanced RAG:")
a = AdvancedRAG()
a.add_docs(["RAG通过检索增强生成减少幻觉", "GraphRAG使用知识图谱结构"])
print(a.query("RAG怎么减少幻觉"))

print("\n🧪 Modular RAG:")
result = mr.pipeline("RAG原理", ["query_rewrite", "hybrid_search", "rerank", "generate"])
print(f"  最终: {result['answer']}")

# ============ RAG 三大组件详解 ============
print("\n" + "=" * 60)
print("🔧 Demo: RAG 三大组件详解")
print("=" * 60)

print("""
┌────────────────────────────────────────────────────┐
│              RAG 三大核心组件                       │
├────────────┬───────────────────┬───────────────────┤
│  检索器     │    增强器         │    生成器          │
│  Retriever │    Augmenter      │    Generator       │
├────────────┼───────────────────┼───────────────────┤
│ 稀疏检索    │  Prompt 模板      │  LLM 调用          │
│  BM25/TF-IDF│  上下文拼接       │  Ollama/OpenAI     │
│            │                   │                    │
│ 稠密检索    │  指令注入         │  流式输出          │
│  Dense     │  chat_template   │  streaming         │
│            │                   │                    │
│ 混合检索    │  引用标注         │  结构化输出        │
│ Hybrid     │  citation        │  JSON mode         │
├────────────┴───────────────────┴───────────────────┤
│  优化方向                                            │
│  检索前: 查询重写、HyDE                              │
│  检索中: 混合检索、MMR                               │
│  检索后: 重排序、上下文压缩                            │
└─────────────────────────────────────────────────────┘
""")

print("✅ RAG技术详解完成！")
