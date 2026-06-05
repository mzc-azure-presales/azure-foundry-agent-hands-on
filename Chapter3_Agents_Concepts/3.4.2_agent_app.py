# Run: uv run Chapter3_Agents_Concepts/3.4.2_agent_app.py
# 학습 포인트: prompt 기반 에이전트의 기본 입력, 지시, 응답 흐름을 이해합니다.
# 초보자 읽기: agent 이름, 역할 지시문, 사용자 질문을 나누어 전달하는 prompt-style agent의 기본 모양을 봅니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_prompt_agent

load_dotenv()


if __name__ == "__main__":
    answer = run_prompt_agent(
        agent_name="hands-on-weather-agent",
        instructions=(
            "You are a prompt-style AI assistant for a Foundry hands-on class. "
            "Explain what tool you would need for live weather, and provide a cautious answer in Korean."
        ),
        user_input="현재 과천 날씨를 알려줘. 실시간 도구가 없다면 어떤 연결이 필요한지도 설명해줘.",
        scenario_name="chapter3.basic_agent",
    )
    print("Prompt-style agent 결과:")
    print(answer)
