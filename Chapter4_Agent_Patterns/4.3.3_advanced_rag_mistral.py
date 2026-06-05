# Run: uv run Chapter4_Agent_Patterns/4.3.3_advanced_rag_mistral.py
# 학습 포인트: PDF에서 텍스트를 추출하고 구조화 context로 바꿔 RAG 입력에 사용합니다.
# 초보자 읽기: PDF 내용을 페이지 단위 context로 만들어 모델에게 넘기고, 답변이 어느 페이지 근거를 쓰는지 확인합니다.
from pathlib import Path

from dotenv import load_dotenv
from pypdf import PdfReader

import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()


def extract_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append(f"[page {page_number}]\n{text.strip()}")
    return "\n\n".join(pages).strip()


def build_extracted_document(pdf_path: Path) -> dict[str, object]:
    extracted_text = extract_pdf_text(pdf_path)
    return {
        "source": str(pdf_path),
        "extraction_method": "pypdf local text extraction",
        "extracted_text": extracted_text,
        "structure_hint": {
            "document_type": "company policy",
            "expected_sections": ["연차 휴가 규정", "병가 규정", "재택 근무 규정"],
            "instruction": "Use headings and line breaks from extracted_text as lightweight document structure.",
        },
    }


if __name__ == "__main__":
    pdf_path = Path("Chapter4_Agent_Patterns/company_policy.pdf")
    extracted_document = build_extracted_document(pdf_path)

    print("고급 문서 이해 RAG 실습")
    print("4.3.2는 원문 텍스트를 청크로 나누어 검색합니다.")
    print("4.3.3은 PDF 파일을 읽어 추출한 텍스트를 구조화 context로 사용합니다.\n")
    print(f"[PDF 파일] {pdf_path}")
    print("\n[PDF에서 추출한 텍스트]")
    print(extracted_document["extracted_text"])
    print("\n[모델에게 전달할 구조화 context]")
    print(extracted_document)

    question = "정규 직원과 계약직/인턴의 휴가 규정 차이를 표 기반으로 설명하고, 병가 5일 연속 사용 시 필요한 서류도 알려줘."
    context = f"Extracted document structure:\n{extracted_document}"

    answer = run_single_turn_prompt(
        "You answer only from the extracted PDF content. Cite the section names or page markers you used.",
        f"Context:\n{context}\n\nQuestion: {question}",
        scenario_name="chapter4.document_ai_rag",
    )

    print("\n질문:", question)
    print("\nFoundry 문서 이해 RAG 답변:")
    print(answer)
