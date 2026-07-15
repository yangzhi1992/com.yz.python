"""
阶段7：LangChain 开发框架
=========================
学习内容:
  1. LangChain 核心概念
  2. ChatModel / PromptTemplate
  3. Chain（链式调用）
  4. Document Loaders
  5. Text Splitters
  6. VectorStore + RetrievalQA
"""

# ============ 7.1 LangChain 核心概念 ============
print("=== 7.1 LangChain 核心概念 ===")

CONCEPTS = """
🔷 LangChain 核心组件

1. ChatModel — 大模型封装
   from langchain_ollama import ChatOllama
   llm = ChatOllama(model="qwen2:7b")

2. PromptTemplate — 提示词模板
   from langchain_core.prompts import ChatPromptTemplate
   prompt = ChatPromptTemplate.from_template("翻译: {text}")

3. Chain — 链式调用
   from langchain_core.runnables import RunnablePassthrough
   chain = prompt | llm | StrOutputParser()

4. Document Loaders — 文档加载
   from langchain_community.document_loaders import TextLoader
   loader = TextLoader("file.txt")

5. Text Splitters — 文本分割
   from langchain.text_splitter import RecursiveCharacterTextSplitter
   splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)

6. VectorStore — 向量存储
   from langchain_chroma import Chroma
   vectorstore = Chroma.from_documents(docs, embedding)

7. RetrievalQA — RAG 问答链
   qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=vectorstore.as_retriever())
"""
print(CONCEPTS)

# ============ 7.2 基础链调用 ============
print("\n=== 7.2 基础链调用 ===")

def basic_chain_demo():
    try:
        from langchain_ollama import ChatOllama
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser

        llm = ChatOllama(model="qwen2:7b", temperature=0)
        prompt = ChatPromptTemplate.from_template(
            "将以下文本翻译成英文: {text}"
        )
        chain = prompt | llm | StrOutputParser()
        result = chain.invoke({"text": "大语言模型改变了人工智能世界"})
        print(f"翻译结果: {result}")

    except ImportError as e:
        print(f"需要安装: pip install langchain langchain-ollama ({e})")
    except Exception as e:
        print(f"[跳过] {e}")

basic_chain_demo()

# ============ 7.3 文档加载与分割 ============
print("\n=== 7.3 文档加载与分割 ===")

def doc_loading_demo():
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_community.document_loaders import TextLoader

        # 创建测试文件
        with open("langchain_test.txt", "w", encoding="utf-8") as f:
            f.write("""大语言模型是人工智能领域的重要突破。
它基于Transformer架构，通过海量数据训练。
GPT系列模型展示了强大的文本生成能力。
BERT模型则在理解任务上表现优异。
RAG技术让大模型能够外挂知识库，
有效解决了模型幻觉和知识更新问题。""")

        # 加载
        loader = TextLoader("langchain_test.txt", encoding="utf-8")
        docs = loader.load()
        print(f"加载文档: {len(docs)}篇, {len(docs[0].page_content)}字")

        # 分割
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=50, chunk_overlap=10,
            separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""],
        )
        chunks = splitter.split_documents(docs)
        print(f"分割后: {len(chunks)}块")
        for i, c in enumerate(chunks):
            print(f"  块{i+1}: {c.page_content}")

    except ImportError as e:
        print(f"[跳过] {e}")

doc_loading_demo()

# ============ 7.4 RAG 问答链 ============
print("\n=== 7.4 RAG 问答链 ===")

def rag_chain_demo():
    try:
        from langchain_ollama import ChatOllama, OllamaEmbeddings
        from langchain_chroma import Chroma
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnablePassthrough

        # 准备知识
        texts = [
            "大语言模型（LLM）是基于Transformer架构的深度学习模型。"
            "通过海量文本数据训练，能够理解和生成自然语言。",

            "RAG（检索增强生成）让大模型外挂知识库进行问答。"
            "包含文档分块、向量化、检索和生成四个步骤。",

            "Agent是能自主使用工具的AI智能体，通过ReAct循环"
            "（推理→行动→观察）完成复杂任务。",

            "微调（Fine-tuning）是在预训练模型基础上用领域数据"
            "继续训练，LoRA通过低秩矩阵实现高效微调。",
        ]

        splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20)
        docs = splitter.create_documents(texts)

        # 创建向量库
        embeddings = OllamaEmbeddings(model="qwen2:7b")
        vectorstore = Chroma.from_documents(docs, embeddings)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

        # RAG 链
        llm = ChatOllama(model="qwen2:7b", temperature=0)
        prompt = ChatPromptTemplate.from_template(
            "基于以下知识回答问题：\n{context}\n\n问题：{question}\n回答："
        )

        def format_docs(docs):
            return "\n".join(d.page_content for d in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt | llm | StrOutputParser()
        )

        # 测试
        answer = rag_chain.invoke("什么是RAG？")
        print(f"RAG问答: {answer[:200]}")

    except ImportError as e:
        print(f"[跳过] LangChain未安装: {e}")
    except Exception as e:
        print(f"[跳过] {e}")

rag_chain_demo()

# ============ 7.5 LCEL 可运行表达式 ============
print("\n=== 7.5 LCEL 可运行表达式 ===")

LCEL = """
🔗 LCEL (LangChain Expression Language)

# 管道操作符 | 链式调用
chain = prompt | llm | output_parser

# 并行执行
chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

# 条件路由
chain = RunnableBranch(
    (lambda x: x.startswith("?"), qa_chain),
    (lambda x: x.startswith("/"), tool_chain),
    default_chain,
)

# 绑定运行时参数
chain = llm.bind(stop=["\n"], temperature=0.5) | output_parser
"""
print(LCEL)

print("\n✅ 阶段7完成！")
