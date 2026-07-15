"""
04-rag-tips: 提升 RAG 效果的实用技巧
=======================================
学习内容: 检索前优化、检索中优化、检索后优化、高级技巧
"""

print("=" * 60)
print("📚 提升 RAG 效果 - 实用技巧")
print("=" * 60)

TIPS_OVERVIEW = """
┌────────────────────────────────────────────────────────────┐
│              RAG 优化全链路                                │
├──────────────┬──────────────┬──────────────┬───────────────┤
│  数据准备     │  检索前优化   │  检索中优化   │  检索后优化   │
├──────────────┼──────────────┼──────────────┼───────────────┤
│ 文档清洗      │ 查询重写     │ 混合检索      │ 重排序        │
│ 表格结构化    │ 查询扩展     │ MMR 多样性   │ 上下文压缩    │
│ 元数据标注    │ HyDE        │ 多路检索     │ 引用过滤      │
│ 标题/摘要     │ 多语言翻译   │ 自适应检索   │ 重复去除      │
│ 去重           │ 问题分解    │ 分层检索     │ 结果融合      │
└──────────────┴──────────────┴──────────────┴───────────────┘
"""
print(TIPS_OVERVIEW)

# ============ 10 个实用技巧 Demo ============
print("\n" + "=" * 60)
print("🔧 Demo: 10 个提升 RAG 效果的实用技巧")
print("=" * 60)

# ---------- 技巧1: 查询重写 ----------
print("\n📌 技巧1: 查询重写 (Query Rewrite)")
print("-" * 40)

class QueryRewrite:
    @staticmethod
    def expand_abbr(query):
        abbr = {"RAG": "检索增强生成", "LLM": "大语言模型", "AI": "人工智能"}
        for k, v in abbr.items():
            query = query.replace(k, f"{k}({v})")
        return query

    @staticmethod
    def decompose(query):
        """复杂问题拆解"""
        if "和" in query and "区别" in query:
            parts = query.split("和")
            main = parts[0].replace("区别", "").strip()
            rest = parts[1].replace("是什么", "").strip()
            return [f"{main}的详细介绍", f"{rest}的详细介绍", f"{main}和{rest}的区别"]
        return [query]

    @staticmethod
    def add_context(query):
        queries = [
            query,
            f"什么是{query}",
            f"请详细介绍{query}的工作原理和应用场景",
        ]
        return queries

q = "RAG和微调的区别"
print(f"  原始: {q}")
print(f"  缩写展开: {QueryRewrite.expand_abbr(q)}")
print(f"  问题拆解: {QueryRewrite.decompose(q)}")
print(f"  多视角: {QueryRewrite.add_context(q)}")

# ---------- 技巧2: HyDE（假设文档嵌入）----------
print("\n📌 技巧2: HyDE (Hypothetical Document Embeddings)")
print("-" * 40)

HYDE = """
HyDE 核心思想:
  先让 LLM 生成一个"假设的理想文档"（想象中的完美回答）
  然后用这个假设文档去检索真实文档

为什么有效？
  查询空间: "怎么减少幻觉" → 50条
  文档空间: "RAG通过外挂知识库..." → 向量在文档侧
  假设文档: "减少幻觉的一种方法是RAG..." → 向量更接近文档

流程:
  查询 → LLM → 假设文档 → Embedding → 检索 → 真实文档

示例:
  Query: "如何减少LLM幻觉"
  ↓
  HyDE: "减少LLM幻觉的方法包括：1.RAG检索增强生成..."
  ↓
  用 HyDE 的向量去检索，找到更匹配的文档
  ↓
  最终基于真实文档回答

效果: Hit Rate 提升 10-20%
"""
print(HYDE)

# ---------- 技巧3: 混合检索 ----------
print("\n📌 技巧3: 混合检索 (Hybrid Search)")
print("-" * 40)

class HybridSearch:
    """稀疏检索(BM25) + 稠密检索(向量) 加权融合"""
    def __init__(self):
        self.docs = []
        self.alpha = 0.3  # BM25 权重

    def bm25_score(self, query, doc):
        """模拟 BM25 关键词匹配"""
        q_words = set(query.lower().split())
        d_words = set(doc.lower().split())
        if not q_words:
            return 0
        overlap = len(q_words & d_words)
        return overlap / len(q_words)

    def vector_score(self, query, doc):
        """模拟向量相似度"""
        import numpy as np
        np.random.seed(hash(query + doc) % 2**32)
        return float(np.random.uniform(0.5, 1.0))

    def search(self, query, docs, k=2):
        scores = []
        for doc in docs:
            bm25 = self.bm25_score(query, doc)
            vec = self.vector_score(query, doc)
            hybrid = self.alpha * bm25 + (1 - self.alpha) * vec
            scores.append(hybrid)
        idx = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [(docs[i], scores[i]) for i in idx]

hs = HybridSearch()
docs = [
    "RAG通过检索外部知识库来增强大模型回答",
    "微调是在预训练模型基础上用领域数据继续训练",
    "Prompt工程通过精心设计提示词引导模型输出",
    "Agent可以自主调用工具完成复杂任务",
]
print(f"  查询: 'RAG和数据库'")
results = hs.search("RAG数据库", docs)
for doc, score in results:
    print(f"    [{score:.3f}] {doc}")

# ---------- 技巧4-10 ----------
print("\n📌 技巧4-10 快速参考")
print("-" * 40)

MORE_TIPS = """
┌──────┬────────────────────────────────┬──────────────────────────┐
│  #   │  技巧                          │  效果                    │
├──────┼────────────────────────────────┼──────────────────────────┤
│  4   │  MMR 多样性控制                 │ 避免检索结果过于相似      │
│      │  score = λ*sim(q,d) - (1-λ)*max_sim(d,selected) │          │
├──────┼────────────────────────────────┼──────────────────────────┤
│  5   │  Slide Window Chunking         │ 保留上下文连贯性         │
│      │  块1: [A][B][C]               │ 相邻块有重叠             │
│      │  块2: [C][D][E]               │                          │
├──────┼────────────────────────────────┼──────────────────────────┤
│  6   │  元数据过滤                     │ 大幅减少检索范围         │
│      │  按日期/作者/分类筛选再检索     │ 精度↑ 速度↑             │
├──────┼────────────────────────────────┼──────────────────────────┤
│  7   │  多路检索融合 (RRF)            │ 综合多种检索结果          │
│      │  score = Σ 1/(k + rank_i)     │ 鲁棒性↑                 │
├──────┼────────────────────────────────┼──────────────────────────┤
│  8   │  上下文压缩                     │ 减少 token 消耗          │
│      │  用 LLM 压缩/提取关键信息      │ 成本↓ 速度↑             │
├──────┼────────────────────────────────┼──────────────────────────┤
│  9   │  Self-RAG                       │ 自我反思 RAG            │
│      │  检索→判断是否需要→生成→评估   │ 按需检索，减少噪声       │
├──────┼────────────────────────────────┼──────────────────────────┤
│  10  │  多轮对话 RAG                   │ 持续对话记忆             │
│      │  历史查询+当前查询→重写→检索   │ 上下文连贯               │
└──────┴────────────────────────────────┴──────────────────────────┘
"""
print(MORE_TIPS)

print("\n✅ RAG 实用技巧完成！")
