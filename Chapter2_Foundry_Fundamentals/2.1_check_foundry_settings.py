# Run: uv run Chapter2_Foundry_Fundamentals/2.1_check_foundry_settings.py
# 학습 포인트: .env 설정과 Foundry 모델 연결 정보를 점검합니다.
# 초보자 읽기: .env에서 endpoint, API key, 모델 배포명, reasoning 설정이 제대로 읽혔는지 먼저 확인합니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on.config import get_settings

load_dotenv()


if __name__ == "__main__":
    settings = get_settings()

    print("Foundry settings loaded successfully.\n")
    print(f"OpenAI endpoint: {settings.openai_endpoint}")
    print(f"Endpoint type: {settings.openai_endpoint_type}")
    print(f"API version: {settings.openai_api_version}")
    print(f"API key: {'set' if settings.api_key else '(not set)'}")
    print(f"Model deployment: {settings.model_deployment_name}")
    print(f"Embedding deployment: {settings.embedding_deployment_name or '(not set)'}")
    print(f"Reasoning effort: {settings.reasoning_effort or '(disabled)'}")
    print("Tracing: console output by default; Azure Monitor only when an Application Insights connection string is set")
