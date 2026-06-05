# Run: uv run Chapter6_MCP_Protocol/6.6.2_mcp_client_ai_search.py
# 학습 포인트: AI Search MCP 도구를 클라이언트에서 호출하고 응답을 확인합니다.
# 초보자 읽기: 먼저 RAG 도구 서버를 켠 뒤 이 클라이언트가 회사 정책 질문을 POST로 보내고 도구 응답을 받는지 확인합니다.
import requests

import _bootstrap  # noqa: F401

BASE_URL = "http://127.0.0.1:8000"


def run_client() -> None:
    print("RAG 도구 서버에 회사 정책 질문을 보냅니다.")
    try:
        response = requests.post(
            f"{BASE_URL}/tools/company-policy-rag",
            json={"question": "우리 회사 연차 휴가 규정에 대해 알려줘."},
            timeout=60,
        )
        response.raise_for_status()
        print("도구 응답:")
        print(response.json()["answer"])
    except requests.RequestException as exc:
        raise SystemExit(
            "RAG 도구 서버에 연결할 수 없습니다. 먼저 `python Chapter6_MCP_Protocol/6.6.1_mcp_server_ai_search.py`를 실행하세요."
        ) from exc


if __name__ == "__main__":
    run_client()
