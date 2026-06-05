# Run: uv run Chapter3_Agents_Concepts/3.4.5_stateful_agent.py
# 학습 포인트: 대화 상태를 누적해 stateful agent처럼 동작시키는 방식을 봅니다.
# 초보자 읽기: messages 리스트에 대화가 누적되면서 2턴 질문에서 이전에 말한 이름과 일정을 기억하는지 확인합니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_threaded_prompt

load_dotenv()


if __name__ == "__main__":
    messages = [
        {
            "role": "system",
            "content": "You are a stateful Foundry assistant. Remember details from earlier turns and answer in Korean.",
        }
    ]

    first = "내 이름은 민수이고 다음 주에 Foundry Agent 교육을 진행해."
    print("사용자:", first)
    print(run_threaded_prompt(messages, first, scenario_name="chapter3.stateful.first"))

    input("\n1턴 응답을 확인했습니다. Enter 키를 누르면 이전 대화를 기억하는지 2턴 질문을 보냅니다...")

    second = "내 이름과 다음 일정이 뭐였는지 기억해?"
    print("\n사용자:", second)
    print(run_threaded_prompt(messages, second, scenario_name="chapter3.stateful.second"))
