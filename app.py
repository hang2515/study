import streamlit as st
from chain import generate_article

st.set_page_config(page_title="AI文章生成器", layout="centered")

st.title("📝 AI文章生成器")
st.write("基于 LangChain + Streamlit")

# 输入区域
topic = st.text_input("请输入文章主题：")
style = st.selectbox(
    "选择写作风格：",
    ["正式", "幽默", "科普", "故事化"]
)

# 按钮
if st.button("生成文章"):
    if topic:
        with st.spinner("正在生成中..."):
            title, content = generate_article(topic, style)

        st.subheader("📌 标题")
        st.write(title)

        st.subheader("📖 正文")
        st.write(content)
    else:
        st.warning("请输入主题！")