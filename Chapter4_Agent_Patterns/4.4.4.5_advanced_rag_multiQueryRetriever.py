# Run: uv run Chapter4_Agent_Patterns/4.4.4.5_advanced_rag_multiQueryRetriever.py
# 학습 포인트: 사용자 질문을 여러 검색 질의로 확장해 검색 품질을 높입니다.
# 초보자 읽기: 막연한 질문을 여러 검색 질의로 바꾼 뒤 그중 하나로 RAG 답변을 만드는 query rewrite 흐름을 확인합니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt
from foundry_hands_on.rag import answer_with_local_rag

load_dotenv()


if __name__ == "__main__":
    original_query = "휴가 규정 알려줘"
    rewritten = run_single_turn_prompt(
        "You rewrite vague Korean search queries into three specific enterprise policy search queries. Return one query per line.",
        original_query,
        scenario_name="chapter4.multi_query.rewrite",
        print_usage=False,
    )

    queries = [line.strip("- 0123456789.\t") for line in rewritten.splitlines() if line.strip()]
    print("생성된 검색 쿼리:")
    for query in queries:
        print("-", query)

    best_query = queries[0] if queries else original_query
    answer = answer_with_local_rag(
        document_path="Chapter4_Agent_Patterns/company_policy.txt",
        query=best_query,
        scenario_name="chapter4.multi_query.answer",
    )
    print("\nFoundry RAG 답변:")
    print(answer)
