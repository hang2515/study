import os

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

texts = [
    "LangChain 是一个用于构建 LLM 应用的框架",
    "RAG 是检索增强生成技术",
]

vectorstore = FAISS.from_texts(texts, OpenAIEmbeddings())
retriever = vectorstore.as_retriever()

from dotenv import load_dotenv
load_dotenv()

# 模型
llm = ChatOpenAI(model=os.getenv("MODEL_NAME"),
                 api_key=os.getenv("UNIAPI_KEY"),
                 base_url=os.getenv("BASE_URL"),
                 temperature=0.7)
# 字符解析器
parser = StrOutputParser()

# 标题生成链
title_prompt = PromptTemplate(
    input_variables=["topic"],
    template="请为以下主题写一个吸引人的文章标题：{topic}"
)

# 内容生成链
content_prompt = PromptTemplate(
    input_variables=["title", "style"],
    template="根据标题写一篇{style}风格的文章：{title}"
)

title_chain = title_prompt | llm | parser
content_chain = content_prompt | llm | parser


# 自定义函数（两个输入）
def generate_article(topic, style):
    title = title_chain.invoke({"topic": topic})
    content = content_chain.invoke({
        "title": title,
        "style": style
    })

    return title, content