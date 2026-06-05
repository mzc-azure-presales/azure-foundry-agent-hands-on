# Run: uv run Chapter1_Getting_Started/1.6.3.1_role_assignment.py
# 학습 포인트: system prompt로 모델의 역할과 응답 스타일을 제어합니다.
# 초보자 읽기: system prompt에 준 역할이 과학 선생님 응답처럼 말투와 설명 방식을 어떻게 바꾸는지 봅니다.
#role_assignment.py
from dotenv import load_dotenv
import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

def explain_gravity_with_foundry() -> None:
    load_dotenv()
    user_message = "중력이란 무엇인가요?"

    print("--- Foundry에 질문 전송 ---")
    print(f"질문: {user_message}\n")

    try:
        answer = run_single_turn_prompt(
            "당신은 초등학생을 위한 과학 선생님입니다. 모든 설명을 간단하고 재미있는 비유로 해주세요.",
            user_message,
            scenario_name="chapter1.role_assignment",
        )
        print("--- Foundry 응답 ---")
        print(answer)
    except Exception as exc:
        print(f"오류가 발생했습니다: {exc}")

if __name__ == "__main__":
    explain_gravity_with_foundry()
