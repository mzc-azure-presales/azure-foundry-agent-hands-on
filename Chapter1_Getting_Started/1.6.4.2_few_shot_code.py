# Run: uv run Chapter1_Getting_Started/1.6.4.2_few_shot_code.py
# 학습 포인트: few-shot 예시를 제공해 모델이 원하는 출력 패턴을 따르게 합니다.
# 초보자 읽기: 몇 개의 예시를 먼저 보여주면 모델이 같은 패턴을 따라 새 입력을 완성하는 few-shot 흐름을 확인합니다.
# few_shot_prompt_example.py
from dotenv import load_dotenv
import _bootstrap  # noqa: F401
from foundry_hands_on import run_chat_prompt

load_dotenv()

few_shot_prompt = [
    {
        "role": "system",
        "content": "당신은 한국어 단어를 음식, 동물, 물건 세 가지 카테고리로 분류하는 전문가입니다.",
    },
    {
        "role": "user",
        "content": "예시 1: 입력 '바나나' -> 출력 '음식'\n예시 2: 입력 '강아지' -> 출력 '동물'\n예시 3: 입력 '책상' -> 출력 '물건'\n예시 4: 입력 '고양이' -> 출력 ?",
    },
]

print("Foundry 모델에게 few-shot 규칙을 보여주고 질문합니다.")

print("\n[모델에게 전달한 few-shot prompt]")
for index, message in enumerate(few_shot_prompt, start=1):
    print(f"\n--- message {index}: {message['role']} ---")
    print(message["content"])

answer = run_chat_prompt(
    few_shot_prompt,
    scenario_name="chapter1.few_shot",
)
print("\nFoundry 응답:", answer)

