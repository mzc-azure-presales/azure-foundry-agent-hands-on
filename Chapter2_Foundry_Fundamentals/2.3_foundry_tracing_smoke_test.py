# Run: uv run Chapter2_Foundry_Fundamentals/2.3_foundry_tracing_smoke_test.py
# 학습 포인트: 현재 설정에서 OpenTelemetry span이 콘솔 trace로 출력되는 흐름을 확인합니다.
# 초보자 읽기: foundry_span 안에서 모델을 호출하면 콘솔이나 Foundry Trace에 어떤 span 정보가 남는지 봅니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on.tracing import foundry_span

load_dotenv()


if __name__ == "__main__":
    with foundry_span("chapter2.tracing_smoke_test"):
        print("Trace span created successfully.")
        print("현재 hands-on 기본 설정은 콘솔 exporter로 span 구조를 확인합니다.")
        print("Application Insights 연결 문자열을 별도로 설정한 경우에만 Azure Monitor로 전송됩니다.")
