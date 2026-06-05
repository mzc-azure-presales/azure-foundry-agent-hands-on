# Run: uv run Chapter4_Agent_Patterns/4.2.1_multi_tool_agent.py
# 학습 포인트: 사용자 요청을 보고 필요한 도구 결과를 모은 뒤, 모델이 최종 답변으로 종합하는 기본 패턴을 익힙니다.
# 초보자 읽기: 계산기와 정책 조회 결과를 먼저 만든 뒤 모델이 두 도구 결과를 종합해 최종 답변으로 정리하는 과정을 봅니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()


def local_calculator(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")
    if any(char not in allowed for char in expression):
        raise ValueError("Only arithmetic characters are allowed.")
    return str(eval(expression, {"__builtins__": {}}, {}))


def local_policy_lookup(keyword: str) -> str:
    policy = {
        "연차": "정규 직원은 연 15일의 유급 연차 휴가를 사용할 수 있습니다.",
        "병가": "병가가 3일을 초과하면 진단서 제출이 필요합니다.",
    }
    return policy.get(keyword, "관련 정책을 찾지 못했습니다.")


if __name__ == "__main__":
    user_request = "계산 결과와 연차 규정을 함께 알려줘."

    print("[학습 목표]")
    print("에이전트는 모델 혼자 답하는 프로그램이 아니라, 필요한 도구 결과를 함께 사용해 답하는 구조입니다.")
    print("이 예제는 실제 tool calling API가 아니라, 로컬 도구 결과를 모델 입력에 넣는 가장 단순한 형태입니다.\n")

    print("[사용자 요청]")
    print(user_request)

    print("\n[사용 가능한 도구 후보]")
    print("1. local_calculator: 숫자 계산이 필요할 때 사용")
    print("2. local_policy_lookup: 회사 정책 키워드를 찾을 때 사용")

    calc_result = local_calculator("(48 + 12) / 3")
    policy_result = local_policy_lookup("연차")

    print("\n[로컬 도구 실행 결과]")
    print(f"local_calculator 결과: {calc_result}")
    print(f"local_policy_lookup 결과: {policy_result}")

    answer = run_single_turn_prompt(
        "You are a prompt-style multi-tool agent. Use the supplied tool results to answer the user request in Korean.",
        (
            f"사용자 요청: {user_request}\n"
            f"Calculator result: {calc_result}\n"
            f"Policy lookup result: {policy_result}\n\n"
            "어떤 도구 결과가 어떤 부분에 쓰였는지도 짧게 설명해줘."
        ),
        scenario_name="chapter4.multi_tool_pattern",
    )

    print("\n[모델이 도구 결과를 종합한 최종 답변]")
    print(answer)
