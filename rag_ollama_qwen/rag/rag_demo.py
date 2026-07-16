"""
RAG Demo (Python) - 使用 LangChain 实现完整 RAG 流程
====================================================
知识点：文档加载→分块→Embedding→向量存储→检索→生成

需要: pip install langchain langchain-ollama chromadb
"""

# ==================== 1. 文档加载与分块 ====================
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 模拟文档
documents = [
    "Spring Boot 是一个基于 Java 的微服务框架，可以快速构建生产级别的 Spring 应用。"
    "它内置了 Tomcat 服务器，支持自动配置和起步依赖。",

    "Redis 是一个开源的内存数据结构存储系统，可用作数据库、缓存和消息代理。"
    "支持字符串、哈希、列表、集合、有序集合等数据类型。",

    "MySQL 是一个关系型数据库管理系统，使用 SQL 语言进行数据操作。"
    "支持 ACID 事务、外键约束、索引优化等特性。广泛用于 Web 应用。",

    "Docker 是一个容器化平台，可以将应用及其依赖打包到容器中。"
    "容器轻量、可移植，确保环境一致性。Docker Compose 可编排多容器应用。",

    "APISIX 是一个云原生 API 网关，基于 Nginx 和 Lua。提供动态路由、"
    "负载均衡、身份认证、限流限速、日志记录等丰富插件。"
]

# 分块
splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
)
chunks = splitter.create_documents(documents)
print(f"✅ 文档分块完成: {len(documents)} 篇 → {len(chunks)} 块")

# ==================== 2. Embedding + 向量存储 ====================
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

embeddings = OllamaEmbeddings(model="qwen2:7b")
print("✅ Embedding 模型已加载")

# 创建向量数据库
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
)
print(f"✅ 向量数据库已创建: {vector_store._collection.count()} 条记录")

# ==================== 3. 检索 ====================
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)

# 测试检索
test_query = "Redis 是什么？"
results = retriever.get_relevant_documents(test_query)
print(f"\n📝 测试检索: '{test_query}'")
for i, doc in enumerate(results):
    print(f"  [{i+1}] {doc.page_content[:80]}... (score pending)")

# ==================== 4. 检索增强生成 ====================
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

llm = ChatOllama(model="qwen2:7b", temperature=0.3)

# 构建 RAG 链
prompt = ChatPromptTemplate.from_template(
    "你是一个知识助手。基于以下知识片段回答问题。\n\n"
    "知识片段:\n{context}\n\n"
    "问题: {question}\n\n"
    "回答:"
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

print("\n✅ RAG 链已构建")

# ==================== 5. 测试 RAG 问答 ====================
def ask(question):
    print(f"\n👤 问: {question}")
    answer = rag_chain.invoke(question)
    print(f"🤖 答: {answer}")
    return answer

if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("📚 RAG 问答测试")
    print("=" * 50)

    questions = [
        "Spring Boot 有什么特点？",
        "Redis 支持哪些数据类型？",
        "APISIX 是什么？有什么功能？",
    ]

    for q in questions:
        ask(q)
        print("-" * 40)
