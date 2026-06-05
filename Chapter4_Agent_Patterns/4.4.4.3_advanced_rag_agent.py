# Run: uv run Chapter4_Agent_Patterns/4.4.4.3_advanced_rag_agent.py
# 학습 포인트: 질문도 embedding한 뒤 chunk vector와 비교해 검색 기반 답변을 구성합니다.
# 초보자 읽기: 질문과 문서 chunk를 모두 embedding한 뒤 cosine similarity로 가까운 chunk를 골라 답변에 넣는 과정을 봅니다.
import math
from pathlib import Path

from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt
from foundry_hands_on.rag import chunk_text, embed_texts

load_dotenv()


def cosine_similarity(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0
    return dot / (left_norm * right_norm)


if __name__ == "__main__":
    document_path = Path("Chapter4_Agent_Patterns/company_policy.txt")
    query = "정규 직원의 연차 규정과 병가 증빙 조건을 함께 알려줘."
    print("질문:", query)

    chunks = chunk_text(document_path.read_text(encoding="utf-8"), chunk_size=500, overlap=80)
    vectors = embed_texts([query, *chunks], scenario_name="chapter4.advanced_rag_agent.embeddings")
    query_vector = vectors[0]
    chunk_vectors = vectors[1:]

    print("\n[질문 embedding vector]")
    print(f"dimension={len(query_vector)}, first_8_values={query_vector[:8]}")

    scored_chunks = sorted(
        [
            (cosine_similarity(query_vector, chunk_vector), chunk)
            for chunk, chunk_vector in zip(chunks, chunk_vectors)
        ],
        reverse=True,
    )
    top_contexts = scored_chunks[:3]

    print("\n[질문 vector와 가장 가까운 chunks]")
    for index, (score, chunk) in enumerate(top_contexts, start=1):
        print(f"\n--- retrieved chunk {index} | cosine_similarity={score:.4f} ---")
        print(chunk)

    context_block = "\n\n---\n\n".join(chunk for _, chunk in top_contexts)
    answer = run_single_turn_prompt(
        "You answer only from the provided context. If the context is insufficient, say so clearly.",
        f"Context:\n{context_block}\n\nQuestion: {query}",
        scenario_name="chapter4.advanced_rag_agent.answer",
    )

    print("\nFoundry RAG 답변:")
    print(answer)
