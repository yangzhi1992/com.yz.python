"""
模块3：Embedding 向量嵌入
==========================
作用：将文本/图像转为向量，用于RAG检索、语义搜索

文件格式: .pt 向量文件
路径示例: /embeddings/*.pt
"""

# ============ 3.1 学习路线 ============
print("=" * 60)
print("📚 Embedding 向量嵌入 - 学习路线")
print("=" * 60)

LEARNING_ROADMAP = """
【阶段1】Embedding 基础
  ├── 词嵌入 (Word Embedding)
  │   ├── One-Hot → 稀疏表示
  │   ├── Word2Vec (CBOW + Skip-gram)
  │   ├── GloVe (全局词向量)
  │   └── FastText (子词嵌入)
  ├── 句子嵌入 (Sentence Embedding)
  │   ├── CLS Token / Mean Pooling
  │   └── Sentence-BERT
  └── 图像嵌入 (Image Embedding)
      └── CNN / ViT 特征提取

【阶段2】Embedding 模型
  ├── 通用英文: text-embedding-ada-002, voyage
  ├── 通用中文: text2vec, BGE, m3e, stella
  ├── 专用领域: bge-law, bge-medical
  └── 多模态: CLIP (图文对齐)

【阶段3】Embedding 应用
  ├── 语义搜索 (Top-K检索)
  ├── RAG 检索 (文档检索)
  ├── 聚类分析 (K-means)
  ├── 异常检测 (孤立点检测)
  └── 推荐系统 (用户/物品向量)

【阶段4】Embedding 优化
  ├── 批量Embedding (batch)
  ├── 缓存策略 (LRU Cache)
  ├── 量化压缩 (int8/binary)
  └── 索引优化 (HNSW/IVF)
"""
print(LEARNING_ROADMAP)

# ============ 3.2 从零实现词嵌入 ============
print("\n" + "=" * 60)
print("🔧 Demo: 从零实现 Embedding")
print("=" * 60)

import torch
import torch.nn as nn
import math

class EmbeddingLayer(nn.Module):
    """嵌入层 - 将 token ID 转为向量"""
    def __init__(self, vocab_size, d_model):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)

    def forward(self, x):
        return self.embed(x)

# 文本 → 向量
vocab = {"我": 0, "爱": 1, "Python": 2, "编程": 3, "AI": 4}
d_model = 8
embed_layer = EmbeddingLayer(len(vocab), d_model)

# 输入: token IDs
tokens = torch.tensor([[vocab["我"], vocab["爱"], vocab["AI"]]])
vectors = embed_layer(tokens)
print(f"Embedding 示例:")
print(f"  输入 token IDs: {tokens}")
print(f"  输出形状: {vectors.shape}")
print(f"  '我' 的向量: {vectors[0, 0].detach().numpy()}")
print(f"  '爱' 的向量: {vectors[0, 1].detach().numpy()}")
print(f"  'AI' 的向量: {vectors[0, 2].detach().numpy()}")

# ============ 3.3 余弦相似度 ============
print("\n" + "=" * 60)
print("🔧 Demo: 余弦相似度语义检索")
print("=" * 60)

import numpy as np

class EmbeddingSearch:
    """基于Embedding的语义检索"""
    def __init__(self, dim=768):
        self.dim = dim
        self.documents = []
        self.vectors = []

    def add_doc(self, text, vector=None):
        self.documents.append(text)
        if vector is None:
            vector = np.random.randn(self.dim)  # 模拟向量
            vector = vector / np.linalg.norm(vector)
        self.vectors.append(vector)

    def search(self, query_vec, top_k=3):
        scores = [np.dot(query_vec, v) for v in self.vectors]
        indices = np.argsort(scores)[-top_k:][::-1]
        return [(self.documents[i], scores[i]) for i in indices]

# 测试
se = EmbeddingSearch(dim=10)
se.add_doc("Python是一种编程语言")
se.add_doc("大模型基于Transformer架构")
se.add_doc("RAG检索增强生成解决幻觉")
se.add_doc("LoRA是一种高效微调方法")
se.add_doc("机器学习是AI的一个分支")

query = np.random.randn(10)
query = query / np.linalg.norm(query)
results = se.search(query, top_k=2)
print("相似度检索结果:")
for text, score in results:
    print(f"  [{score:.4f}] {text}")

# ============ 3.4 使用现成Embedding模型 ============
print("\n" + "=" * 60)
print("🔧 Demo: 使用 Sentence-Transformers")
print("=" * 60)

ST_GUIDE = """
# 安装: pip install sentence-transformers

from sentence_transformers import SentenceTransformer

# 中文 Embedding 模型推荐
models = {
    "BAAI/bge-small-zh-v1.5":   "384维, 轻量, 推荐",
    "BAAI/bge-base-zh-v1.5":    "768维, 平衡, 推荐",
    "BAAI/bge-large-zh-v1.5":   "1024维, 最准确, 慢",
    "shibing624/text2vec-base-chinese": "中文基线",
    "moka-ai/m3e-base":         "768维, 中英双语",
    "infgrad/stella-base-zh":   "768维, 指令优化",
}

model = SentenceTransformer("BAAI/bge-small-zh-v1.5")

# 文本 → 向量
sentences = ["如何学习大模型", "Transformer 原理", "今天天气很好"]
embeddings = model.encode(sentences)
print(f"文本数: {len(sentences)}, 向量维度: {embeddings.shape[1]}")

# 相似度矩阵
sim_matrix = model.similarity(embeddings, embeddings)
print(f"相似度矩阵:\n{sim_matrix}")

# RAG 检索
from sentence_transformers import util
query = "怎么入门大模型"
q_vec = model.encode(query)
scores = util.cos_sim(q_vec, embeddings)[0]
top_idx = scores.argsort(descending=True)[:2]
print(f"查询: '{query}'")
for idx in top_idx:
    print(f"  [{scores[idx]:.4f}] {sentences[idx]}")
"""
print(ST_GUIDE)

# ============ 3.5 Embedding 维度可视化 ============
print("\n" + "=" * 60)
print("🔧 Demo: 维度与模型对比")
print("=" * 60)

print(f"{'模型':<35} {'维度':<8} {'参数量':<12} {'适用场景'}")
print("-" * 75)
data = [
    ("BGE-small-zh-v1.5",      384,  "24M",  "轻量/移动端"),
    ("BGE-base-zh-v1.5",       768,  "102M", "通用推荐"),
    ("BGE-large-zh-v1.5",      1024, "326M", "最高精度"),
    ("text2vec-base-chinese",  768,  "110M", "中文基线"),
    ("text-embedding-ada-002", 1536, "未知",  "OpenAI"),
    ("CLIP ViT-B/32",          512,  "150M", "图文对齐"),
]
for name, dim, params, scene in data:
    print(f"{name:<35} {dim:<8} {params:<12} {scene}")

print("\n✅ Embedding模块完成！")
