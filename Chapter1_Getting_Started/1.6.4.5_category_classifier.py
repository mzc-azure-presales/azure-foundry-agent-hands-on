# Run: uv run Chapter1_Getting_Started/1.6.4.5_category_classifier.py
# 학습 포인트: few-shot 예시로 간단한 카테고리 분류기를 만듭니다.
# 초보자 읽기: 카테고리 예시를 보고 모델이 새 문장을 어떤 분류로 판단하는지 출력 결과를 비교합니다.
# few_shot_classifier.py
from dotenv import load_dotenv
import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()

system_prompt = "당신은 입력 단어를 기술, 스포츠, 음식, 여행 중 하나로만 분류합니다. 설명 없이 카테고리만 출력하세요."
user_prompt = "예시 1: 입력 '축구' -> 출력 '스포츠'\n예시 2: 입력 '파스타' -> 출력 '음식'\n예시 3: 입력 'Azure OpenAI' -> 출력 '기술'\n입력: 제주도"

answer = run_single_turn_prompt(
    system_prompt,
    user_prompt,
    scenario_name="chapter1.category_classifier",
)

print("\n분류 결과:", answer)

