# Run: uv run streamlit run Chapter5_Advanced_Systems/5.3.2_streamlit_chatbot_with_memory.py
# 학습 포인트: Streamlit session_state로 챗봇 대화 메모리를 유지합니다.
# 초보자 읽기: st.session_state.messages에 대화가 쌓이면서 웹 챗봇이 이전 질문과 답변을 화면에 유지하는 방식을 봅니다.
import streamlit as st
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_threaded_prompt

load_dotenv()

st.set_page_config(page_title="Prompt-style Chatbot with Memory", layout="wide")
st.title("Prompt-style Chatbot with Memory")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a Microsoft Foundry hands-on assistant. Answer in Korean and remember the conversation.",
        }
    ]

for message in st.session_state.messages:
    if message["role"] in {"user", "assistant"}:
        with st.chat_message(message["role"]):
            st.write(message["content"])

if prompt := st.chat_input("prompt-style agent에게 질문하세요"):
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        answer = run_threaded_prompt(
            st.session_state.messages,
            prompt,
            scenario_name="chapter5.streamlit.memory",
        )
        st.write(answer)
