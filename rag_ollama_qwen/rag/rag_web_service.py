"""
DeepSeek R1 + Ollama RAG Web 服务
===================================
纯本地方案：TF-IDF 向量化 + 余弦相似度检索 + DeepSeek R1 生成
无需 embedding API，兼容所有 Ollama 版本
"""

import os
import uuid
import shutil
import time
import json
import pickle
import numpy as np
from typing import List
from pathlib import Path

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import TextLoader, PyPDFLoader

# ==================== 配置 ====================
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
INDEX_FILE = BASE_DIR / "rag_index.pkl"
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".md"}

LLM_MODEL = "deepseek-r1:7b"
OLLAMA_BASE_URL = "http://localhost:11434"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
TOP_K = 4

os.makedirs(UPLOAD_DIR, exist_ok=True)

# ==================== FastAPI ====================
app = FastAPI(title="DeepSeek R1 RAG 服务", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


# ==================== 本地 RAG 引擎 ====================
class LocalRAGEngine:
    """纯本地 RAG 引擎 — TF-IDF 检索 + DeepSeek R1 生成"""

    def __init__(self):
        self.chunks = []          # 文本列表
        self.metadatas = []       # 元数据列表
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(2, 4),
            max_features=50000,
            lowercase=True,
        )
        self.feature_matrix = None   # (N, D) numpy array
        self._fitted = False
        self.llm = ChatOllama(
            model=LLM_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=0.3,
            num_predict=4096,
        )

        # 尝试加载持久化索引
        if INDEX_FILE.exists():
            try:
                self._load()
            except Exception:
                pass

    def _save(self):
        """持久化到磁盘"""
        data = {
            "chunks": self.chunks,
            "metadatas": self.metadatas,
            "fitted": self._fitted,
        }
        if self._fitted:
            data["vectorizer"] = self.vectorizer
            data["feature_matrix"] = self.feature_matrix
        with open(INDEX_FILE, "wb") as f:
            pickle.dump(data, f)

    def _load(self):
        """从磁盘加载"""
        with open(INDEX_FILE, "rb") as f:
            data = pickle.load(f)
        self.chunks = data.get("chunks", [])
        self.metadatas = data.get("metadatas", [])
        self._fitted = data.get("fitted", False)
        if self._fitted and "vectorizer" in data:
            self.vectorizer = data["vectorizer"]
            self.feature_matrix = data["feature_matrix"]

    def add_texts(self, texts: List[str], metadatas: List[dict]):
        """添加文本并重建索引"""
        self.chunks.extend(texts)
        self.metadatas.extend(metadatas)
        self._rebuild_index()
        self._save()

    def _rebuild_index(self):
        """重建 TF-IDF 索引"""
        if not self.chunks:
            self._fitted = False
            self.feature_matrix = None
            return
        self.feature_matrix = self.vectorizer.fit_transform(self.chunks).toarray()
        self._fitted = True

    def similarity_search(self, query: str, k: int = TOP_K):
        """余弦相似度检索"""
        if not self._fitted or len(self.chunks) == 0:
            return []

        query_vec = self.vectorizer.transform([query]).toarray()[0]

        scores = []
        for i, doc_vec in enumerate(self.feature_matrix):
            sim = 1 - cosine(query_vec, doc_vec) if np.any(doc_vec) else 0
            scores.append((i, sim))

        scores.sort(key=lambda x: x[1], reverse=True)
        results = []
        for idx, score in scores[:k]:
            if score > 0:
                results.append({
                    "content": self.chunks[idx],
                    "metadata": self.metadatas[idx],
                    "score": round(float(score), 4),
                })
        return results

    def query(self, question: str) -> dict:
        """完整 RAG 问答"""
        start = time.time()

        # 1. 检索
        results = self.similarity_search(question, TOP_K)

        # 2. 构建上下文
        context = "\n\n".join(
            f"[{i+1}] {r['content']}"
            for i, r in enumerate(results)
        )

        # 3. 如果没有检索到相关文档
        if not context.strip():
            answer = "知识库中没有相关信息。"
            return {
                "question": question,
                "answer": answer,
                "sources": [],
                "time_seconds": round(time.time() - start, 2),
            }

        # 4. LLM 生成
        prompt_text = (
            "你是一个技术知识助手，基于以下知识片段回答问题。\n\n"
            f"知识片段:\n{context}\n\n"
            f"问题: {question}\n\n"
            "要求:\n"
            "1. 如果知识片段中有相关信息，请基于这些信息回答\n"
            "2. 如果知识片段中没有相关信息，请说'知识库中没有相关信息'\n"
            "3. 不要在回答中输出思考过程标签（如 ／think ／think），直接给答案\n"
            "4. 用中文回答\n\n"
            "回答:"
        )

        # 调用 DeepSeek R1
        response = self.llm.invoke(prompt_text)
        answer = response.content if hasattr(response, 'content') else str(response)
        # 过滤思考标签
        import re
        answer = re.sub(r'<think>.*?</think>', '', answer, flags=re.DOTALL).strip()
        answer = re.sub(r'^回答[：:]\s*', '', answer).strip()

        elapsed = time.time() - start

        # 去重来源
        seen_sources = set()
        sources = []
        for r in results:
            src = r["metadata"].get("source", "unknown")
            if src not in seen_sources:
                seen_sources.add(src)
            sources.append({
                "content": r["content"][:200],
                "source": src,
                "score": r["score"],
            })

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "time_seconds": round(elapsed, 2),
        }

    def get_stats(self):
        return {
            "total_chunks": len(self.chunks),
            "llm_model": LLM_MODEL,
            "index_type": "TF-IDF (char_wb 2-4gram)",
            "vector_dim": self.feature_matrix.shape[1] if self._fitted else 0,
        }

    def clear(self):
        self.chunks = []
        self.metadatas = []
        self._fitted = False
        self.feature_matrix = None
        if INDEX_FILE.exists():
            os.remove(INDEX_FILE)

    def list_docs(self):
        """按源文件分组统计"""
        sources = {}
        for m in self.metadatas:
            src = m.get("source", "unknown")
            sources[src] = sources.get(src, 0) + 1
        return {
            "total_chunks": len(self.chunks),
            "total_documents": len(sources),
            "documents": [
                {"name": name, "chunks": count}
                for name, count in sorted(sources.items())
            ],
        }


# ==================== 初始化引擎 ====================
rag_engine = LocalRAGEngine()
print(f"✅ RAG 引擎就绪 | LLM: {LLM_MODEL} | 知识块: {rag_engine.get_stats()['total_chunks']}")


# ==================== 文档处理 ====================
def load_document(file_path: str):
    ext = Path(file_path).suffix.lower()
    if ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    elif ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext == ".md":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"不支持的文件类型: {ext}")
    return loader.load()


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
    )
    return splitter.split_documents(documents)


# ==================== API 路由 ====================

@app.get("/", response_class=HTMLResponse)
async def index():
    with open(BASE_DIR / "templates" / "index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/api/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []
    total_chunks = 0

    for file in files:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            results.append({"file": file.filename, "status": "skip", "reason": "不支持的文件类型"})
            continue

        file_path = UPLOAD_DIR / f"{uuid.uuid4()}{ext}"
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        try:
            documents = load_document(str(file_path))
            chunks = split_documents(documents)
            texts = [c.page_content for c in chunks]
            metas = [{**c.metadata, "source": file.filename} for c in chunks]
            rag_engine.add_texts(texts, metas)
            total_chunks += len(chunks)
            results.append({"file": file.filename, "status": "success", "chunks": len(chunks)})
        except Exception as e:
            results.append({"file": file.filename, "status": "error", "reason": str(e)})

    return {"results": results, "total_chunks_added": total_chunks, "stats": rag_engine.get_stats()}


@app.post("/api/chat")
async def chat(question: str = Form(...)):
    if not question.strip():
        raise HTTPException(400, "问题不能为空")
    return rag_engine.query(question)


@app.get("/api/chat")
async def chat_get(question: str):
    if not question.strip():
        raise HTTPException(400, "问题不能为空")
    return rag_engine.query(question)


@app.get("/api/stats")
async def stats():
    return rag_engine.get_stats()


@app.get("/api/list")
async def list_documents():
    return rag_engine.list_docs()


@app.post("/api/clear")
async def clear_knowledge():
    rag_engine.clear()
    return {"status": "ok", "message": "知识库已清空"}


# ==================== 启动 ====================
if __name__ == "__main__":
    port = 8085
    print(f"🚀 DeepSeek R1 RAG 服务")
    print(f"   LLM: {LLM_MODEL} | 索引: TF-IDF (纯本地)")
    print(f"   🌐 http://localhost:{port}")
    print(f"   📡 http://localhost:{port}/docs")
    uvicorn.run(app, host="0.0.0.0", port=port)
