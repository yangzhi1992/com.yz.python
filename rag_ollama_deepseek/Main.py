import streamlit as st
import tempfile
import os

# HuggingFace 国内镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains.llm import LLMChain
from langchain_classic.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_classic.chains import RetrievalQA

# 颜色主题
primary_color = "#1E90FF"
secondary_color = "#FF6347"
background_color = "#F5F5F5"
text_color = "#4561e9"

# 自定义 CSS
st.markdown(f"""
<style>
.stApp {{
    background-color: {background_color};
    color: {text_color};
}}
.stButton>button {{
    background-color: {primary_color};
    color: white;
    border-radius: 5px;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
}}
.stTextInput>div>div>input {{
    border: 2px solid {primary_color};
    border-radius: 5px;
    padding: 10px;
    font-size: 16px;
}}
.stFileUploader>div>div>button {{
    background-color: {secondary_color};
    color: white;
    border-radius: 5px;
    border: none;
    padding: 10px 20px;
    font-size: 16px;
}}
</style>
""", unsafe_allow_html=True)

# Streamlit 应用标题
st.title("使用 DeepSeek R1 和 Ollama 构建 RAG 系统")

# 加载 PDF
uploaded_file = st.file_uploader("上传 PDF 文件", type="pdf")

if uploaded_file:
    docs = None
    documents = None
    retriever = None
    llm = None

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name

        loader = PDFPlumberLoader(tmp_path)
        docs = loader.load()
    except Exception as e:
        st.error(f"PDF 加载失败: {e}")
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

    if docs is None:
        st.stop()

    try:
        text_splitter = SemanticChunker(HuggingFaceEmbeddings(model_name="all-mpnet-base-v2"))
        documents = text_splitter.split_documents(docs)
    except Exception as e:
        st.error(f"文本分块失败: {e}")

    if documents is None:
        st.stop()

    try:
        embedder = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
        vector = FAISS.from_documents(documents, embedder)
        retriever = vector.as_retriever(search_type="similarity", search_kwargs={"k": 3})
    except Exception as e:
        st.error(f"向量库构建失败: {e}")

    if retriever is None:
        st.stop()

    try:
        llm = Ollama(model="deepseek-r1:7b")
    except Exception as e:
        st.error(f"Ollama 连接失败，请确认 Ollama 已启动: {e}")

    if llm is None:
        st.stop()

    # 提示模板
    prompt = """
1. 使用以下上下文回答问题。
2. 如果不知道答案，请直接说"我不知道"，不要自行编造答案。
3. 回答简洁，控制在 3-4 句话以内。

上下文: {context}

问题: {question}

有用的回答:
"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(prompt)

    llm_chain = LLMChain(
        llm=llm,
        prompt=QA_CHAIN_PROMPT,
        callbacks=None,
        verbose=True
    )

    document_prompt = PromptTemplate(
        input_variables=["page_content", "source"],
        template="上下文: \n内容: {page_content}\n来源: {source}"
    )

    combine_documents_chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="context",
        document_prompt=document_prompt,
        callbacks=None
    )

    qa = RetrievalQA(
        combine_documents_chain=combine_documents_chain,
        verbose=True,
        retriever=retriever,
        return_source_documents=True
    )

    # 用户输入
    user_input = st.text_input("向 PDF 提问：")

    # 处理用户输入
    if user_input:
        with st.spinner("处理中..."):
            try:
                response = qa(user_input)["result"]
                st.write("回答：")
                st.write(response)
            except Exception as e:
                st.error(f"查询失败: {e}")
else:
    st.write("请上传 PDF 文件以继续。")
