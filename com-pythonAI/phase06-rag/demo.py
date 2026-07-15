"""
阶段6：RAG 检索增强生成
=========================
学习内容:
  1. 文档分块 Chunking
  2. Embedding 向量化
  3. 向量数据库（ChromaDB）
  4. 检索 + 增强生成
  5. 完整的 RAG 问答系统
"""

import os
import json

# ============ 6.1 文档分块 ============
print("=== 6.1 文档分块 Chunking ===")

class DocumentChunker:
    def __init__(self, chunk_size=200, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text):
        """递归字符分割"""
        chunks = []
        paragraphs = text.split("\n")
        current = ""
        for para in paragraphs:
            if not para.strip():
                continue
            if len(current) + len(para) > self.chunk_size and current:
                chunks.append(current.strip())
                current = current[-self.overlap:] if self.overlap else ""
            current += para + "\n"
        if current.strip():
            chunks.append(current.strip())
        return chunks

chunker = DocumentChunker(100, 20)
doc = """大语言模型（LLM）是一种基于Transformer架构的深度学习模型。
它通过海量文本数据训练，能够理解和生成自然语言。
RAG（检索增强生成）是一种让LLM外挂知识库的技术。
它先检索相关文档，再将文档作为上下文注入Prompt，
让LLM基于检索到的知识回答问题，有效减少幻觉。"""
chunks = chunker.chunk(doc)
print(f"原始文档: {len(doc)}字 → {len(chunks)}个块")
for i, c in enumerate(chunks):
    print(f"  块{i+1}: {c[:60]}... ({len(c)}字)")

# ============ 6.2 向量检索（手工实现）============
print("\n=== 6.2 向量检索（手工实现）===")
import numpy as np

class SimpleVectorDB:
    def __init__(self):
        self.chunks = []
        self.vectors = []

    def add(self, chunk, vector):
        self.chunks.append(chunk)
        self.vectors.append(vector)

    def search(self, query_vector, top_k=3):
        """余弦相似度检索"""
        scores = [self._cosine_sim(query_vector, v) for v in self.vectors]
        indices = np.argsort(scores)[-top_k:][::-1]
        return [(self.chunks[i], scores[i]) for i in indices]

    def _cosine_sim(self, a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# 模拟向量（实际使用 Embedding API）
vdb = SimpleVectorDB()
vdb.add("Python是一种编程语言", np.random.rand(10))
vdb.add("大模型需要大量GPU训练", np.random.rand(10))
vdb.add("RAG可以解决幻觉问题", np.random.rand(10))

query = np.random.rand(10)
results = vdb.search(query, top_k=2)
print("检索结果:")
for chunk, score in results:
    print(f"  [{score:.3f}] {chunk}")

# ============ 6.3 ChromaDB 向量数据库 ============
print("\n=== 6.3 ChromaDB 向量数据库 ===")

def demo_chromadb():
    try:
        import chromadb
        client = chromadb.Client()
        collection = client.create_collection("demo_kb")

        # 添加文档
        collection.add(
            documents=[
                "大语言模型基于Transformer架构",
                "RAG是检索增强生成的缩写",
                "向量数据库用于存储和检索向量",
                "LangChain是LLM应用开发框架",
            ],
            ids=["doc1", "doc2", "doc3", "doc4"]
        )

        # 检索
        results = collection.query(
            query_texts=["什么是RAG"],
            n_results=2
        )
        print("ChromaDB 检索结果:")
        for doc in results['documents'][0]:
            print(f"  → {doc}")

    except ImportError:
        print("ChromaDB 未安装 (pip install chromadb)")

demo_chromadb()

# ============ 6.4 完整 RAG 流程 ============
print("\n=== 6.4 完整 RAG 流程 ===")

class RAGSystem:
    """简易 RAG 问答系统"""

    def __init__(self):
        self.chunks = []
        self.vectors = []
        self.llm_base = "http://localhost:11434"

    def add_documents(self, texts):
        """添加文档到知识库"""
        for text in texts:
            chunked = DocumentChunker(200, 30).chunk(text)
            for chunk in chunked:
                vec = self._get_embedding(chunk)
                self.chunks.append(chunk)
                self.vectors.append(np.array(vec))
        print(f"知识库: {len(self.chunks)}个片段")

    def _get_embedding(self, text):
        """调用 Embedding API（或生成模拟向量）"""
        import requests
        try:
            resp = requests.post(f"{self.llm_base}/api/embed", json={
                "model": "qwen2:7b",
                "input": [text],
            }, timeout=10)
            return resp.json()["embeddings"][0]
        except:
            return np.random.rand(768).tolist()

    def query(self, question):
        """RAG 问答"""
        # 1. 问题向量化
        q_vec = np.array(self._get_embedding(question))

        # 2. 检索 Top-3
        scores = [np.dot(q_vec, v)/(np.linalg.norm(q_vec)*np.linalg.norm(v))
                  for v in self.vectors]
        top_idx = np.argsort(scores)[-3:][::-1]
        context = "\n".join(self.chunks[i] for i in top_idx)

        # 3. 增强生成
        prompt = f"基于以下知识回答问题：\n\n{context}\n\n问题：{question}\n回答："
        return self._call_llm(prompt)

    def _call_llm(self, prompt):
        import requests
        try:
            resp = requests.post(f"{self.llm_base}/api/chat", json={
                "model": "qwen2:7b",
                "stream": False,
                "messages": [{"role": "user", "content": prompt}],
            }, timeout=30)
            return resp.json()["message"]["content"]
        except:
            return "[LLM不可用] 检索结果如上"

# 测试
rag = RAGSystem()
rag.add_documents([
    "RAG（检索增强生成）是一种让大模型外挂知识库的技术。"
    "它先检索相关文档，再将文档作为上下文注入Prompt，"
    "让LLM基于检索到的知识回答问题，有效减少幻觉。",

    "向量数据库（如ChromaDB、FAISS、Milvus）专门用于存储"
    "和检索向量。它们通过余弦相似度找到语义相近的文本。",

    "LangChain是一个流行的LLM应用开发框架，提供了文档加载、"
    "文本分割、向量存储、链式调用等模块化工具。"
])

# 测试问答
print("\nRAG 问答测试:")
test_questions = [
    "RAG是什么？有什么用？",
    "向量数据库的作用是什么？",
]
for q in test_questions:
    print(f"\n👤 问: {q}")
    answer = rag.query(q)
    print(f"🤖 答: {answer[:200]}")

print("\n✅ 阶段6完成！")
