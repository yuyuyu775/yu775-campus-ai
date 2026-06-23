import streamlit as st
import os
import sys

# 添加 src 目录到路径（云端部署需要）
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 从 agent 导入
from agent import agent_chat

st.set_page_config(page_title="校园生活百事通助手", page_icon="🏫")
st.title("🏫 安徽交院校园生活百事通助手")

# 初始化会话
if "messages" not in st.session_state:
    st.session_state.messages = []

# 渲染历史对话
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 用户输入
if prompt := st.chat_input("输入校园相关问题，例如：怎么补办一卡通"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        resp = agent_chat(prompt)
        st.markdown(resp)
    
    st.session_state.messages.append({"role": "assistant", "content": resp})