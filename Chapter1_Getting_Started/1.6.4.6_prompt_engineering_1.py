# Run: uv run Chapter1_Getting_Started/1.6.4.6_prompt_engineering_1.py
# 학습 포인트: 대상과 톤을 지정해 광고 문구 생성 결과를 제어합니다.
# 초보자 읽기: 역할과 금지 조건을 prompt에 넣으면 광고 문구의 톤과 표현이 어떻게 제한되는지 확인합니다.
# prompt_engineering_test.py
from dotenv import load_dotenv
import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()

answer = run_single_turn_prompt(
    "당신은 간결한 제품 카피라이터입니다.",
    "친환경 텀블러를 20대 직장인에게 소개하는 한 문단 광고 문구를 작성하세요. 과장 표현은 피하세요.",
    scenario_name="chapter1.prompt_engineering.basic",
)

print("응답:")
print(answer)

