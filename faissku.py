import faiss
import numpy as np

from embedding import QianwenEmbeddings


# ===== 1. 读取文档 =====
def load_documents(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        docs = f.readlines()
    return [doc.strip() for doc in docs if doc.strip()]


# ===== 2. 主流程 =====
def build_faiss():
    documents = load_documents("documents.txt")
    print("加载文档:", documents)

    embedding = QianwenEmbeddings()

    # ===== 3. 获取向量 =====
    vectors = embedding.embed_documents(documents)

    print("向量维度:", len(vectors[0]))

    # ===== 4. 创建 FAISS =====
    index = faiss.IndexFlatL2(len(vectors[0]))
    index.add(np.array(vectors).astype("float32"))

    # ===== 5. 保存 =====
    faiss.write_index(index, "faiss_index.index")

    # 保存原始文本（用于查询返回）
    with open("docs_store.txt", "w", encoding="utf-8") as f:
        for doc in documents:
            f.write(doc + "\n")

    print(f"✅ 成功创建 {len(documents)} 条向量数据")


if __name__ == "__main__":
    build_faiss()