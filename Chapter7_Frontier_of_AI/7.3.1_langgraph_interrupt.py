# Run: uv run Chapter7_Frontier_of_AI/7.3.1_langgraph_interrupt.py
# 학습 포인트: 사람의 승인이나 수정이 끼어드는 human-in-the-loop 흐름을 연습합니다.
# 초보자 읽기: 준비된 초고를 읽고 사람이 피드백을 입력하면 그 피드백이 최종 결과에 반영되는 human-in-the-loop 흐름을 체험합니다.
import os

from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()


SAMPLE_DRAFT = """2026년 AI 에이전트 기술의 핵심 트렌드는 세 가지로 볼 수 있습니다.

1. 도구를 사용하는 에이전트
AI는 단순히 답변을 생성하는 수준을 넘어 검색, 계산, 업무 시스템 호출 같은 외부 도구를 사용합니다.

2. 사람과 함께 일하는 에이전트
중요한 결정은 AI가 혼자 확정하지 않고, 사람이 승인하거나 수정한 뒤 다음 단계로 진행합니다.

3. 관찰 가능한 에이전트
운영 환경에서는 어떤 prompt가 실행되었고, 어떤 도구가 호출되었고, 어디서 실패했는지 trace로 확인해야 합니다.

실무적으로는 에이전트를 만들 때 자동화 범위, 사람 승인 지점, 로그와 trace 기준을 함께 설계해야 합니다.
"""


def _use_model_editor() -> bool:
    return os.getenv("CHAPTER7_USE_MODEL_EDITOR", "false").lower() in {"1", "true", "yes", "y"}


def _apply_feedback_locally(draft: str, feedback: str) -> str:
    cleaned_feedback = feedback.strip() or "초보자도 이해하기 쉽게 더 간결하게 정리"
    return f"""{draft.strip()}

[사람 피드백 반영]
- 요청한 피드백: {cleaned_feedback}
- 최종본에서는 핵심 용어를 쉽게 풀어 쓰고, 사람이 승인하는 지점을 명확히 강조합니다.

[최종 정리]
AI 에이전트 실습에서 중요한 점은 모델이 혼자 모든 일을 끝내는 것이 아닙니다. 먼저 초안을 만들고, 사람이 방향을 확인한 뒤, 그 피드백을 다음 단계에 반영합니다. 이 파일은 그 흐름을 빠르게 보여주는 human-in-the-loop 예제입니다.
"""


def _print_feedback_examples() -> None:
    print("피드백 예시:")
    print("- 초보자가 이해하기 쉽게 핵심만 짧게 정리해줘")
    print("- 각 트렌드마다 실무 예시를 하나씩 추가해줘")
    print("- 마지막에 핵심 요약 3줄을 추가해줘")
    print("- 너무 딱딱하니 교육생에게 설명하듯 자연스럽게 바꿔줘")
    print("그냥 Enter를 누르면 기본 피드백을 사용합니다.")


if __name__ == "__main__":
    print("빠른 실습을 위해 준비된 초고를 사용합니다. 모델 편집을 쓰려면 CHAPTER7_USE_MODEL_EDITOR=true로 설정하세요.")
    draft = SAMPLE_DRAFT

    print("검토할 초고입니다. 확인 후 피드백을 입력해주세요.")
    print("--------------------------------------------------")
    print(draft)
    print("--------------------------------------------------")
    _print_feedback_examples()
    feedback = input("피드백 입력 > ")

    if _use_model_editor():
        final_post = run_single_turn_prompt(
            "You are an editor agent. Apply the human feedback and produce the final Korean post.",
            f"초고:\n{draft}\n\n피드백:\n{feedback}",
            scenario_name="chapter7.human_loop.editor",
        )
    else:
        final_post = _apply_feedback_locally(draft, feedback)

    print("\n최종 결과물:\n")
    print(final_post)
