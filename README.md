# Chain 示例项目

基于 **LangChain** 与 **Streamlit** 的小示例仓库，包含两个独立入口：**AI 文章生成** 与 **AGV 知识库智能问答**（RAG）。两者均通过阿里云 DashScope 的 OpenAI 兼容接口调用模型，需在环境中配置 API Key。

---

## 环境要求

- **Python**：3.10 及以上
- **网络**：可访问 DashScope 兼容模式地址（代码中已写死 `base_url`）

---

## 两个应用说明

| 入口文件 | 功能 | 核心逻辑 |
|-----------|------|-----------|
| `app.py` | **AI 文章生成器**：输入主题、选择风格（正式 / 幽默 / 科普 / 故事化），生成标题与正文 | `chain.py`：标题链 + 正文链，`qwen3-vl-flash` |
| `agvapp.py` | **AGV 智能问答**：基于本地 FAISS 向量库做检索增强问答；检索相似度不足时回退为纯 LLM 回答 | `RetrievalQA` + `docs_store.txt` / `faiss_index.index`，`qwen3.5-flash` |

---

## 环境变量

在项目根目录创建 `.env`（或直接在系统中设置），至少包含：

| 变量名 | 说明 |
|--------|------|
| `UNIAPI_KEY` | DashScope API Key，文章生成、问答、向量嵌入均使用此 Key |

嵌入模型在 `embedding.py` 中固定为 `text-embedding-v4`；对话模型在 `chain.py` / `agvapp.py` 中分别指定，无需再通过环境变量改模型名（若需修改可改源码）。

---

## 安装依赖

`requirements.txt` 已包含两个应用与 `faissku.py` 索引构建所需的依赖，一条命令即可：

```bash
pip install -r requirements.txt
```

若你更倾向使用 GPU 版 FAISS，可自行将依赖中的 `faiss-cpu` 换为对应平台可用的 `faiss` 包，并避免同时安装冲突的 CPU/GPU 变体。

---

## 运行方式

**文章生成：**

```bash
streamlit run app.py
```

**AGV 问答：**

需已存在 `faiss_index.index` 与 `docs_store.txt`（见下一节）。然后：

```bash
streamlit run agvapp.py
```

---

## AGV 知识库：如何构建索引

问答应用依赖向量索引与对齐的文本行。编辑根目录 **`documents.txt`**（每行一条知识，或按你现有格式一行一段），然后执行：

```bash
python faissku.py
```

脚本会：

1. 读取 `documents.txt` 并调用千问嵌入接口生成向量；
2. 写入 **`faiss_index.index`**；
3. 将用于检索展示的文本写入 **`docs_store.txt`**。

之后即可用 `streamlit run agvapp.py` 启动问答界面。`agvapp.py` 中通过 **相似度分数阈值**（默认 `THRESHOLD = 0.8`）决定是走知识库 RAG 还是直接 LLM 回答，可按实际效果微调。

---

## 项目结构（主要文件）

| 文件 | 作用 |
|------|------|
| `app.py` | 文章生成 Streamlit 界面 |
| `agvapp.py` | AGV 问答 Streamlit 界面（RAG + 阈值回退） |
| `chain.py` | 文章标题与正文生成链 |
| `embedding.py` | 千问嵌入封装（`QianwenEmbeddings`） |
| `faissku.py` | 从 `documents.txt` 构建 FAISS 索引与 `docs_store.txt` |
| `documents.txt` | 构建索引时的原始知识文本（每行一条） |
| `docs_store.txt` / `faiss_index.index` | 运行 `faissku.py` 后的产物，供 `agvapp.py` 使用 |
| `requirements.txt` | 两个应用与索引构建的 Python 依赖列表 |

---

## 说明

- 两个应用可分别运行，互不依赖；仅 AGV 问答需要预先构建索引文件。
- API 与模型配置以当前仓库源码为准；升级 LangChain 或更换模型时注意接口兼容性。
