# Run: uv run Chapter2_Foundry_Fundamentals/2.2_foundry_responses_smoke_test.py
# 학습 포인트: Responses API 호출이 정상 동작하는지 간단히 검증합니다.
# 초보자 읽기: 공통 client가 Responses API에 최소 질문을 보내고 정상 응답을 받는지 확인하는 연결 테스트입니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()


if __name__ == "__main__":
    answer = run_single_turn_prompt(
        "You are a Microsoft Foundry instructor. Answer in Korean.",
        "OpenAI-compatible endpoint, API key, 모델 배포명이 각각 어떤 역할을 하는지 한 문단으로 설명해줘.",
        scenario_name="chapter2.responses_smoke_test",
    )

    print("Foundry Responses API smoke test result:\n")
    print(answer)
