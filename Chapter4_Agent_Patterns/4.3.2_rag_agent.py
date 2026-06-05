# Run: uv run Chapter4_Agent_Patterns/4.3.2_rag_agent.py
# 학습 포인트: 로컬 문서 검색 결과를 prompt에 넣어 RAG 응답을 생성합니다.
# 초보자 읽기: 회사 정책 문서에서 관련 문맥을 검색하고, 모델이 그 문맥 안에서만 답하도록 만드는 RAG 흐름을 확인합니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on.rag import answer_with_local_rag

load_dotenv()


if __name__ == "__main__":
    document_path = "Chapter4_Agent_Patterns/company_policy.txt"

    for query in [
        "우리 회사 정규 직원의 연차 휴가는 며칠인가요?",
        "병가를 5일 연속 쓰려면 무엇이 필요한가요?",
    ]:
        print("\n질문:", query)
        answer = answer_with_local_rag(
            document_path=document_path,
            query=query,
            scenario_name="chapter4.local_rag",
        )
        print("Foundry RAG 답변:")
        print(answer)
