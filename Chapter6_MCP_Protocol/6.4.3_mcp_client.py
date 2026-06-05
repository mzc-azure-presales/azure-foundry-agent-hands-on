# Run: uv run Chapter6_MCP_Protocol/6.4.3_mcp_client.py
# 학습 포인트: MCP 스타일 서버에 HTTP 요청을 보내 도구 호출 흐름을 확인합니다.
# 초보자 읽기: 먼저 Flask 서버를 켠 뒤 이 클라이언트가 /session과 /chat에 HTTP 요청을 보내는 순서를 확인합니다.
import requests
from dotenv import load_dotenv

import _bootstrap  # noqa: F401

load_dotenv()

BASE_URL = "http://127.0.0.1:5000"


def run_client() -> None:
    try:
        response = requests.post(f"{BASE_URL}/session", timeout=10)
        response.raise_for_status()
        session_id = response.json()["session_id"]
        print(f"세션 ID: {session_id}")

        response = requests.post(
            f"{BASE_URL}/chat",
            json={"session_id": session_id, "message": "안녕하세요! 아이폰 17에 대해서 설명해주세요"},
            timeout=60,
        )
        response.raise_for_status()
        print("AI 응답:", response.json()["response"])
    except requests.RequestException as exc:
        raise SystemExit(
            "MCP Flask 서버에 연결할 수 없습니다. 먼저 `python Chapter6_MCP_Protocol/6.4.2_mcp_flask_server.py`를 실행하세요."
        ) from exc


if __name__ == "__main__":
    run_client()
