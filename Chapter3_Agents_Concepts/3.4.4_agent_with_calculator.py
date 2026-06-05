# Run: uv run Chapter3_Agents_Concepts/3.4.4_agent_with_calculator.py
# 학습 포인트: 계산이 필요한 질문에서 모델 응답과 도구 사용 개념을 비교합니다.
# 초보자 읽기: 계산은 로컬 함수가 먼저 수행하고, 모델은 그 계산 결과를 사람이 이해하기 쉽게 설명하는 역할임을 확인합니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()


def calculator(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")
    if any(char not in allowed for char in expression):
        raise ValueError("Only basic arithmetic expressions are allowed.")
    return str(eval(expression, {"__builtins__": {}}, {}))


if __name__ == "__main__":
    expression = "(12500 * 3) * 1.1"
    tool_result = calculator(expression)
    answer = run_single_turn_prompt(
        "You are a prompt-style assistant explaining local tool results to a learner.",
        f"계산식: {expression}\n도구 결과: {tool_result}\n이 결과를 한국어로 짧게 설명해줘.",
        scenario_name="chapter3.calculator_tool",
    )
    print(answer)
