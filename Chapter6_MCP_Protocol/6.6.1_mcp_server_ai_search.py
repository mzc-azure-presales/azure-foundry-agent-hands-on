# Run: uv run Chapter6_MCP_Protocol/6.6.1_mcp_server_ai_search.py
# 학습 포인트: Azure AI Search를 MCP 도구 서버와 연결하는 구조를 살펴봅니다.
# 초보자 읽기: FastAPI 서버가 회사 정책 RAG를 /tools/company-policy-rag endpoint로 노출하고 질문과 답변을 서버 로그에 남기는지 봅니다.
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

import _bootstrap  # noqa: F401
from foundry_hands_on.rag import answer_with_local_rag

load_dotenv()

app = FastAPI(title="Foundry RAG MCP-style Server")


class RagRequest(BaseModel):
    question: str


@app.post("/tools/company-policy-rag")
def company_policy_rag(request: RagRequest):
    print("\n[클라이언트 요청]", flush=True)
    print(f"질문: {request.question}", flush=True)

    answer = answer_with_local_rag(
        document_path="Chapter4_Agent_Patterns/company_policy.txt",
        query=request.question,
        scenario_name="chapter6.mcp.rag_tool",
    )

    print("\n[서버 응답]", flush=True)
    print(f"답변: {answer}", flush=True)
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
