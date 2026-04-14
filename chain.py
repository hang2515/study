import os

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


from dotenv import load_dotenv
load_dotenv()

# 模型
llm = ChatOpenAI(model="qwen3-vl-flash",
                 api_key=os.getenv("UNIAPI_KEY"),
                 base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
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