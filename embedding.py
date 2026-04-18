from langchain_core.embeddings import Embeddings
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class QianwenEmbeddings(Embeddings):
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("UNIAPI_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

    def embed_documents(self, texts):
        response = self.client.embeddings.create(
            model="text-embedding-v4",
            input=texts
        )
        return [item.embedding for item in response.data]

    def embed_query(self, query):
        return self.embed_documents([query])[0]