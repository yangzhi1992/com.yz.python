"""
03-rag-modules: RAG 应用的关键模块总结
=========================================
学习内容: RAG 系统各模块详解、索引策略、检索策略、生成策略
"""

print("=" * 60)
print("📚 RAG 关键模块总结 - 学习路线")
print("=" * 60)

LEARNING = """
┌──────────────────────────────────────────────────────┐
│              RAG 系统完整模块图                       │
├────────────┬────────────┬────────────┬───────────────┤
│ 文档处理层 │  索引层     │  检索层     │  生成层       │
├────────────┼────────────┼────────────┼───────────────┤
│ 文档加载    │ 分块策略   │ 查询处理    │ Prompt 模板    │
│ PDF/Word   │ 固定/递归  │ 重写/扩展   │ 角色+上下文    │
│            │ 语义       │ HyDE       │               │
├────────────┼────────────┼────────────┼───────────────┤
│ 文档清洗    │ Embedding  │ 检索策略    │ LLM 调用       │
│ OCR/去噪   │ 稠密/稀疏  │ 向量/BM25  │ chat/补全     │
│            │            │ 混合       │ 流式/非流式    │
├────────────┼────────────┼────────────┼───────────────┤
│ 元数据提取  │ 索引存储   │ 重排序      │ 后处理         │
│ 标题/日期   │ 内存/磁盘  │ Cohere/BGE │ 格式/引用/过滤 │
│ 作者/分类   │ 云服务     │ MMR        │               │
└────────────┴────────────┴────────────┴───────────────┘
"""
print(LEARNING)

# ============ 各模块详解 ============
print("\n" + "=" * 60)
print("🔧 Demo: 各模块详解与对比")
print("=" * 60)

print("\n📄 1. 文档加载模块")
print("-" * 40)
print("""
├── TextLoader:      .txt, .md, .py
├── PDFLoader:       PyMuPDF / PDFPlumber
├── CSVLoader:       pandas 读取
├── Docx2txtLoader:  Word文档
├── UnstructuredLoader: 通用 (图片/表格)
├── WebBaseLoader:   网页抓取
└── SeleniumLoader:  动态页面
""")

print("\n✂️ 2. 分块策略对比")
print("-" * 40)

class ChunkStrategies:
    """分块策略对比"""
    @staticmethod
    def fixed_size(text, size=200, overlap=20):
        """固定大小分块"""
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + size, len(text))
            chunks.append(text[start:end])
            start += size - overlap
        return chunks

    @staticmethod
    def recursive(text, chunk_size=200, overlap=20):
        """递归字符分割"""
        chunks = []
        for sep in ["\n\n", "\n", "。", "！", "？", "，", " "]:
            if len(text) <= chunk_size:
                chunks.append(text)
                return chunks
            # 按分隔符拆分
            parts = text.split(sep)
            current = ""
            for part in parts:
                if len(current) + len(part) > chunk_size and current:
                    chunks.append(current)
                    current = current[-overlap:] + part if overlap else part
                else:
                    current += part
            if current:
                chunks.append(current)
            return chunks[:3]  # 演示只返回前3块
        return [text[:chunk_size]]

    @staticmethod
    def semantic(text):
        """语义分块 (基于主题)"""
        # 实际使用 Embedding 检测主题变化
        topics = ["RAG基础", "高级RAG", "GraphRAG"]
        # 模拟: 每200字一个主题
        return [f"[{t}] {text[i:i+200]}" for i, t in enumerate(topics)]

text = "RAG是检索增强生成。它通过外挂知识库来减少幻觉。GraphRAG使用知识图谱增强检索。向量数据库存储文本向量。"
print(f"  原始: {text}")
print(f"  固定分块: {ChunkStrategies.fixed_size(text, 30, 5)}")
print(f"  语义分块: {ChunkStrategies.semantic(text)}")

print("\n🔍 3. 检索策略对比")
print("-" * 40)

RETRIEVAL_STRATEGIES = """
┌───────────────┬──────────────────────┬──────────┬──────────┐
│   策略         │ 原理                 │ 精度     │ 速度     │
├───────────────┼──────────────────────┼──────────┼──────────┤
│ 相似度搜索     │ 余弦相似度 Top-K      │ ⭐⭐⭐   │ ⭐⭐⭐⭐⭐ │
│ MMR           │ 相似度 + 多样性       │ ⭐⭐⭐⭐  │ ⭐⭐⭐⭐  │
│ 混合检索       │ 向量 + BM25 加权融合  │ ⭐⭐⭐⭐⭐ │ ⭐⭐⭐   │
│ HyDE           │ 先生成假设回答再检索   │ ⭐⭐⭐⭐  │ ⭐⭐     │
│ 重排序         │ 粗筛 Top-50 → 精排   │ ⭐⭐⭐⭐⭐ │ ⭐⭐     │
│ 自适应检索     │ 根据query动态调整策略  │ ⭐⭐⭐⭐  │ ⭐⭐⭐   │
└───────────────┴──────────────────────┴──────────┴──────────┘

选择建议:
  • 简单场景: 相似度搜索
  • 需要多样性: MMR
  • 追求精度: 混合检索 + 重排序
  • 复杂查询: HyDE
"""

print(RETRIEVAL_STRATEGIES)

print("\n📝 4. 生成策略")
print("-" * 40)

class GenerationStrategies:
    """生成策略"""

    @staticmethod
    def direct(context, question):
        return f"基于以下内容：{context[:50]}...\n回答：{question}"

    @staticmethod
    def with_citation(context, question):
        return f"回答：{question}\n引用：{context[:50]}..."

    @staticmethod
    def step_by_step(context, question):
        return (f"让我逐步分析：\n1. 首先看相关知识：{context[:50]}...\n"
                f"2. 分析问题：{question}\n3. 综合回答")

    @staticmethod
    def json_output(context, question):
        return '{"answer": "' + question + '", "source": "' + context[:20] + '..."}'

    @staticmethod
    def conditional(context, question):
        has_info = len(context) > 50
        if has_info:
            return f"基于知识库：{context[:50]}..."
        return "知识库中没有相关信息，基于我的理解回答..."

print("  直接生成:", GenerationStrategies.direct("RAG原理", "RAG是什么"))
print("  带引用:", GenerationStrategies.with_citation("RAG原理", "RAG是什么"))
print("  逐步分析:", GenerationStrategies.step_by_step("RAG原理", "RAG是什么"))
print("  结构化:", GenerationStrategies.json_output("RAG原理", "RAG是什么"))

print("\n✅ RAG关键模块完成！")
