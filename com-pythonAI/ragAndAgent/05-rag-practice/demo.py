"""
05-rag-practice: 基于 RAG 的 LLM 应用实践
===========================================
学习内容: 完整 RAG 项目实战、RAG 评估、RAG 监控
"""

print("=" * 60)
print("📚 RAG 应用实践 - 学习路线")
print("=" * 60)

PRACTICE_ROADMAP = """
【实战项目1】企业知识库问答系统
  ├── 技术栈: LangChain + ChromaDB + Ollama
  ├── 功能: PDF上传 → 自动分块 → 问答
  └── 难点: 文档格式多样、表格处理、长文档

【实战项目2】客服知识库助手
  ├── 技术栈: FastAPI + FAISS + BGE
  ├── 功能: 用户问题 → 检索 → 回答 → 评价
  └── 难点: 多轮对话、时效性、准确性

【实战项目3】内部文档搜索引擎
  ├── 技术栈: ElasticSearch + 向量 + BM25
  ├── 功能: 混合检索 + 高亮 + 分页
  └── 难点: 大量文档、实时更新

【实战项目4】多模态 RAG
  ├── 技术栈: LLaVA + CLIP + 向量库
  ├── 功能: 图文联合检索、图表解读
  └── 难点: 多模态对齐、存储
"""
print(PRACTICE_ROADMAP)

# ============ 完整 RAG 应用架构 ============
print("\n" + "=" * 60)
print("🔧 Demo: 完整 RAG 应用代码模板")
print("=" * 60)

FULL_APP_TEMPLATE = """
# =====================================
# 完整的 RAG 问答应用 (FastAPI 模板)
# =====================================

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
import os

app = FastAPI(title="RAG 知识库系统")

# --- 初始化 ---
embedding = OllamaEmbeddings(model="qwen2:7b")
llm = ChatOllama(model="qwen2:7b", temperature=0)
client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection("knowledge_base")

# --- 模型 ---
class Query(BaseModel):
    question: str
    top_k: int = 3

class Document(BaseModel):
    content: str
    source: str = "user_upload"

# --- API ---

@app.post("/upload")
async def upload_doc(doc: Document):
    \"\"\"上传文档到知识库\"\"\"
    # 分块
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    )
    chunks = splitter.split_text(doc.content)

    # 向量化 + 存储
    vectors = embedding.embed_documents(chunks)
    ids = [f"{doc.source}_{i}" for i in range(len(chunks))]
    collection.add(
        documents=chunks,
        embeddings=vectors,
        ids=ids,
        metadatas=[{"source": doc.source}] * len(chunks)
    )
    return {"status": "ok", "chunks": len(chunks)}

@app.post("/query")
async def query(q: Query):
    \"\"\"RAG 问答\"\"\"
    # 1. 查询向量化
    q_vec = embedding.embed_query(q.question)

    # 2. 检索
    results = collection.query(
        query_embeddings=[q_vec],
        n_results=q.top_k
    )

    if not results["documents"]:
        return {"answer": "未找到相关信息", "source": []}

    # 3. 构建上下文
    context = "\\n".join(results["documents"][0])

    # 4. LLM 生成
    prompt = f"基于以下知识回答问题：\\n{context}\\n\\n问题：{q.question}"
    answer = llm.invoke(prompt)

    return {
        "answer": answer.content,
        "sources": [
            {"content": d[:100], "score": s}
            for d, s in zip(results["documents"][0], results["distances"][0])
        ]
    }

@app.get("/stats")
async def stats():
    \"\"\"知识库统计\"\"\"
    count = collection.count()
    return {"total_docs": count}

# 启动: uvicorn app:app --port 8000
"""

print(FULL_APP_TEMPLATE)

# ============ RAG 评估 ============
print("\n" + "=" * 60)
print("🔧 Demo: RAG 评估指标")
print("=" * 60)

class RAGEvaluator:
    """RAG 效果评估"""

    @staticmethod
    def faithfulness(hypothesis, reference):
        """忠实度: 回答是否基于给定知识"""
        # 模拟评估
        overlap = len(set(hypothesis) & set(reference))
        return min(overlap / max(len(set(hypothesis)), 1), 1.0)

    @staticmethod
    def answer_relevance(question, answer):
        """回答相关性: 是否回答到点上"""
        q_words = set(question.lower().split())
        a_words = set(answer.lower().split())
        overlap = len(q_words & a_words)
        return min(overlap / max(len(q_words), 1), 1.0)

    @staticmethod
    def context_relevance(query, retrieved_docs):
        """上下文相关性: 检索结果是否相关"""
        scores = []
        for doc in retrieved_docs:
            overlap = len(set(query) & set(doc))
            scores.append(overlap / max(len(set(query)), 1))
        return sum(scores) / max(len(scores), 1)

    def evaluate(self, question, answer, context, retrieved_docs):
        return {
            "faithfulness": self.faithfulness(answer, context),
            "answer_relevance": self.answer_relevance(question, answer),
            "context_relevance": self.context_relevance(question, retrieved_docs),
            "avg_score": 0.0,  # 加权平均
        }

# 模拟评估
ev = RAGEvaluator()
result = ev.evaluate(
    question="RAG怎么减少幻觉",
    answer="RAG通过检索外部知识库来减少LLM的幻觉问题",
    context="RAG通过检索外部知识库来增强生成",
    retrieved_docs=["RAG通过检索外部知识库", "RAG检索增强生成减少幻觉"]
)
result["avg_score"] = (
    0.4 * result["faithfulness"] +
    0.3 * result["answer_relevance"] +
    0.3 * result["context_relevance"]
)
print("RAG 评估结果:")
for k, v in result.items():
    print(f"  {k}: {v:.3f}")

print("\n✅ RAG 应用实践完成！")
