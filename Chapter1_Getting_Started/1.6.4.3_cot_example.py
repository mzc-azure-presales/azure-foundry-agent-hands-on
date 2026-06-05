# Run: uv run Chapter1_Getting_Started/1.6.4.3_cot_example.py
# 학습 포인트: 복잡한 문제를 단계적으로 풀도록 요청하는 프롬프트 방식을 확인합니다.
# 초보자 읽기: 어려운 문제를 바로 답하게 하지 않고 단계별로 풀어 쓰게 했을 때 최종 답변 구조가 어떻게 달라지는지 봅니다.
#cot_example.py
from dotenv import load_dotenv
import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()

question = "철수는 사과 12개 중 3개를 먹고, 남은 것의 절반을 친구에게 줬습니다. 철수에게 남은 사과는 몇 개인가요?"

answer = run_single_turn_prompt(
    "당신은 수학 튜터입니다. 풀이 과정을 간결하게 단계별로 설명하고 마지막 줄에 정답만 다시 쓰세요.",
    question,
    scenario_name="chapter1.step_by_step_reasoning",
)

print("질문:", question)
print("\nFoundry 응답:")
print(answer)
