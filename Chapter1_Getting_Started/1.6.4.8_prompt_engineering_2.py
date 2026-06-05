# Run: uv run Chapter1_Getting_Started/1.6.4.8_prompt_engineering_2.py
# 학습 포인트: 길이, 형식, 금지 조건 같은 제약을 prompt에 반영합니다.
# 초보자 읽기: few-shot 예시와 뉴스 앵커 역할을 함께 주면 민감한 주제를 균형 있게 설명하도록 유도할 수 있는지 봅니다.
# prompt_optimization_2.py
from dotenv import load_dotenv
import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()

answer = run_single_turn_prompt(
    "당신은 중립적 뉴스 앵커입니다. 민감한 주제는 균형 잡힌 근거 중심으로 설명하세요.",
    "예시1: 기후 변화 -> 과학적 증거 기반 설명\n예시2: AI 윤리 -> 편향 문제 강조\n예시3: 정치 이슈 -> 균형 잡힌 쟁점 정리\n주제: 생성형 AI 규제",
    scenario_name="chapter1.prompt_engineering.optimized",
)

print("최적화된 응답:")
print(answer)

