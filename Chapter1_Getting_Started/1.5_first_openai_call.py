# Run: uv run Chapter1_Getting_Started/1.5_first_openai_call.py
# 학습 포인트: Foundry 모델에 첫 요청을 보내고 응답을 확인합니다.
# 초보자 읽기: Foundry 모델에 첫 질문을 보내고 system prompt, user prompt, 모델 응답이 어떤 순서로 출력되는지 확인합니다.
# 1. 필요한 라이브러리를 불러옵니다.
from dotenv import load_dotenv
import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()

print("Microsoft Foundry 프로젝트에 첫 요청을 보냅니다.")

try:
    answer = run_single_turn_prompt(
        "당신은 세상의 모든 것을 유머러스하게 설명하는 과학자입니다.",
        "블랙홀이 무엇인지 초등학생도 이해할 수 있게 설명해줘.",
        scenario_name="chapter1.first_foundry_call",
    )
    print("\n[Foundry 응답]")
    print(answer)
except Exception as exc:
    print(f"오류가 발생했습니다: {exc}")
    print(".env의 FOUNDRY_OPENAI_ENDPOINT, FOUNDRY_API_KEY, FOUNDRY_MODEL_DEPLOYMENT_NAME을 확인하세요.")

