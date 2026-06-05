# Run: uv run Chapter6_MCP_Protocol/6.4.2_mcp_flask_server.py
# 학습 포인트: Flask(파이썬 기반의 웹프레임워크)로 간단한 MCP 스타일 도구 서버를 실행합니다.
# 초보자 읽기: Flask 서버가 세션을 만들고 /chat 요청마다 대화 기록을 메모리에 쌓아 응답하는 서버 흐름을 봅니다.
import uuid

from dotenv import load_dotenv
from flask import Flask, jsonify, request

import _bootstrap  # noqa: F401
from foundry_hands_on import run_chat_prompt

load_dotenv()

app = Flask(__name__)
contexts: dict[str, list[dict[str, str]]] = {}


@app.route("/session", methods=["POST"])
def create_session():
    session_id = str(uuid.uuid4())
    contexts[session_id] = [
        {
            "role": "system",
            "content": "You are a Foundry-backed MCP-style chat server. Answer in Korean.",
        }
    ]
    print(f"\n[새 세션 생성] session_id={session_id}", flush=True)
    return jsonify({"session_id": session_id})


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    session_id = data["session_id"]
    user_message = data["message"]

    if session_id not in contexts:
        return jsonify({"error": "Invalid session"}), 400

    print("\n[클라이언트 요청]", flush=True)
    print(f"session_id: {session_id}", flush=True)
    print(f"질문: {user_message}", flush=True)

    contexts[session_id].append({"role": "user", "content": user_message})
    answer = run_chat_prompt(
        contexts[session_id],
        scenario_name="chapter6.mcp.flask_server",
        print_usage=False,
    )
    contexts[session_id].append({"role": "assistant", "content": answer})

    print("\n[서버 응답]", flush=True)
    print(f"답변: {answer}", flush=True)
    return jsonify({"response": answer})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
