"""
RAG Demo - 从零实现（无第三方框架）
=====================================
知识点：手动实现分块、余弦相似度检索、上下文拼接

需要: pip install requests numpy
"""

import requests
import json
import numpy as np
from typing import List

OLLAMA_BASE = "http://localhost:11434"
EMBED_MODEL = "qwen2:7b"
LLM_MODEL = "qwen2:7b"


def get_embedding(text: str) -> List[float]:
    """调用 Ollama Embedding API"""
    resp = requests.post(f"{OLLAMA_BASE}/api/embed", json={
        "model": EMBED_MODEL,
        "input": [text],
    })
    return resp.json()["embeddings"][0]


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class SimpleRAG:
    """从零实现的 RAG 系统"""

    def __init__(self):
        self.chunks = []
        self.vectors = []

    def add_documents(self, texts: List[str]):
        """1. 文档分块 + 2. Embedding"""
        for text in texts:
            # 简单分块
            for chunk in self._chunk(text):
                self.chunks.append(chunk)
                vec = get_embedding(chunk)
                self.vectors.append(np.array(vec))

        print(f"✅ 已入库 {len(self.chunks)} 个知识块")

    def _chunk(self, text: str, max_len=200):
        """简单分块：按句号分割"""
        parts = text.replace("。", "。\n").split("\n")
        chunks, current = [], ""
        for p in parts:
            if len(current) + len(p) > max_len and current:
                chunks.append(current.strip())
                current = p
            else:
                current += p
        if current.strip():
            chunks.append(current.strip())
        return chunks

    def retrieve(self, query: str, top_k=3):
        """3. 向量检索（余弦相似度）"""
        q_vec = np.array(get_embedding(query))
        scores = [cosine_similarity(q_vec, v) for v in self.vectors]
        top_idx = np.argsort(scores)[-top_k:][::-1]

        results = []
        for idx in top_idx:
            results.append((self.chunks[idx], scores[idx]))
        return results

    def generate(self, query: str, context: str) -> str:
        """4. LLM 生成"""
        prompt = (f"基于以下知识回答问题：\n\n{context}\n\n问题：{query}\n回答：")

        resp = requests.post(f"{OLLAMA_BASE}/api/chat", json={
            "model": LLM_MODEL,
            "stream": False,
            "messages": [{"role": "user", "content": prompt}],
        })
        return resp.json()["message"]["content"]

    def query(self, question: str) -> str:
        """完整 RAG 流程"""
        results = self.retrieve(question)
        context = "\n".join(f"[{i+1}] {r[0]}" for i, r in enumerate(results))
        answer = self.generate(question, context)

        return f"{answer}\n\n---\n📎 引用:\n" + "\n".join(
            f"  {i+1}. (相似度:{r[1]:.2f}) {r[0][:50]}..."
            for i, r in enumerate(results)
        )


if __name__ == "__main__":
    rag = SimpleRAG()

    # 加载预置知识
    rag.add_documents([
        "Spring Boot 是一个基于 Java 的微服务框架，内置 Tomcat，支持自动配置。",
        "Redis 支持字符串、哈希、列表、集合、有序集合五种基本数据类型。",
        "MySQL 是一个关系型数据库，支持 ACID 事务和 SQL 查询。",
        "Docker 是一个容器平台，可以将应用打包为镜像，保证环境一致性。",
        "APISIX 是云原生 API 网关，支持动态路由和负载均衡。",
    ])

    # 测试
    print("\n📚 手写 RAG 测试")
    for q in ["Redis 支持什么？", "什么是 Docker？", "APISIX 有什么用？"]:
        print(f"\n👤 {q}")
        print(f"🤖 {rag.query(q)}")
        print("=" * 50)
