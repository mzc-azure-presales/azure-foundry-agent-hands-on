# Run: uv run Chapter4_Agent_Patterns/4.4.4.2_advanced_rag_index.py
# 학습 포인트: 문서를 청크로 나누고 임베딩 인덱스를 만드는 준비 단계를 수행합니다.
# 초보자 읽기: 문서를 겹치는 chunk로 나누고 embedding vector를 만들어 검색 인덱스의 재료가 준비되는 과정을 봅니다.
from pathlib import Path

from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on.rag import chunk_text, embed_texts

load_dotenv()


if __name__ == "__main__":
    document_path = Path("Chapter4_Agent_Patterns/company_policy.txt")
    chunks = chunk_text(document_path.read_text(encoding="utf-8"), chunk_size=500, overlap=80)
    vectors = embed_texts(chunks, scenario_name="chapter4.ai_search_index.embeddings")

    print(f"Prepared {len(chunks)} chunks with {len(vectors)} Foundry embedding vectors.")
    print("\n[생성된 chunks]")
    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- chunk {index} ---")
        print(chunk)

    print("\n[생성된 embedding vectors 미리보기]")
    for index, vector in enumerate(vectors, start=1):
        preview = vector[:8]
        print(f"vector {index}: dimension={len(vector)}, first_8_values={preview}")

    print("다음 단계: Azure AI Search 인덱스의 vector 필드에 chunks/vectors를 업로드합니다.")
    print("실습에서는 포털에서 생성한 인덱스 스키마와 AZURE_SEARCH_* 환경 변수를 확인하세요.")
