# Run: uv run streamlit run Chapter5_Advanced_Systems/5.3.1_streamlit_app.py
# 학습 포인트: Streamlit으로 API key 기반 prompt-style agent UI를 만듭니다.
# 초보자 읽기: Streamlit 입력창과 버튼이 사용자의 질문을 prompt-style agent 호출로 넘기는 웹 앱 흐름을 확인합니다.
import streamlit as st
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_prompt_agent

load_dotenv()

st.set_page_config(page_title="Prompt-style Agent Web App", layout="wide")
st.title("Prompt-style Agent Web App")

query = st.text_input("prompt-style agent에게 질문하세요:", placeholder="예: multi-agent workflow를 언제 사용하나요?")

if st.button("질문하기"):
    if not query:
        st.warning("질문을 입력해주세요.")
    else:
        with st.spinner("Prompt-style agent 실행 중..."):
            answer = run_prompt_agent(
                agent_name="hands-on-streamlit-agent",
                instructions="You are a Microsoft Foundry instructor. Answer clearly in Korean.",
                user_input=query,
                scenario_name="chapter5.streamlit.agent_app",
            )
        st.write(answer)
