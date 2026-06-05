# Run: uv run Chapter7_Frontier_of_AI/7.4.1_reflection_loop.py
# 학습 포인트: 초안 생성 후 자기 검토를 통해 응답을 개선하는 reflection loop를 구현합니다.
# 초보자 읽기: 첫 호출이 주장 글 초고를 만들고, 두 번째 호출이 그 초고의 약점을 찾아 더 강한 최종본으로 고치는 과정을 봅니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()


if __name__ == "__main__":
    topic = "AI가 인간의 창의성을 대체할 수 있다는 주장"

    draft = run_single_turn_prompt(
        "You write short argumentative Korean essays.",
        f"{topic}에 대한 짧은 주장 글을 작성해.",
        scenario_name="chapter7.reflection.draft",
    )

    final = run_single_turn_prompt(
        "You are a critical editor. Find weaknesses, then produce a stronger final version in Korean.",
        f"주제: {topic}\n\n초고:\n{draft}",
        scenario_name="chapter7.reflection.critic",
    )

    print("## 초고\n")
    print(draft)
    print("\n## 비평 후 최종본\n")
    print(final)
