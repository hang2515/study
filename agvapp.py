import os
import faiss
import streamlit as st
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_community.docstore import InMemoryDocstore
from langchain_core.documents import Document
from embedding import QianwenEmbeddings
from dotenv import load_dotenv
load_dotenv()

# ===== 1. 加载文本 =====
def load_docs():
    with open("docs_store.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]


# ===== 2. 初始化 =====
embedding = QianwenEmbeddings()

faiss_index = faiss.read_index("faiss_index.index")

documents = load_docs()

documents_obj = [Document(page_content=doc) for doc in documents]

docstore = InMemoryDocstore({
    i: documents_obj[i] for i in range(len(documents_obj))
})

index_to_docstore_id = {i: i for i in range(len(documents_obj))}

vectorstore = FAISS(
    index=faiss_index,
    embedding_function=embedding,
    docstore=docstore,
    index_to_docstore_id=index_to_docstore_id
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 3})


# ===== 3. 千问模型 =====
llm = ChatOpenAI(
    model="qwen3.5-flash",
    api_key=os.getenv("UNIAPI_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.7
)


# ===== 4. RAG =====
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever
)


# ===== 5. UI =====
st.title("智能问答系统")

query = st.text_input("请输入问题：")

if query:
    docs_with_score = vectorstore.similarity_search_with_score(query, k=3)

    top_score = docs_with_score[0][1]

    THRESHOLD = 0.8  # 可以调

    if top_score > THRESHOLD:
        st.write("⚠️ 未命中知识库，使用大模型回答")
        result = llm.invoke(query).content
    else:
        st.write("📚 命中知识库")
        result = qa_chain.run(query)

    st.write("回答：", result)