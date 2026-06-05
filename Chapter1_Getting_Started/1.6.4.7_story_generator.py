# Run: uv run Chapter1_Getting_Started/1.6.4.7_story_generator.py
# 학습 포인트: 창의적 생성 prompt로 짧은 이야기를 만들어 봅니다.
# 초보자 읽기: 역할과 주제만으로 모델이 짧은 창작 이야기를 어떻게 구성하는지 관찰합니다.
# story_generator.py
from dotenv import load_dotenv
import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt

load_dotenv()

answer = run_single_turn_prompt(
    "당신은 어린이를 위한 짧은 이야기를 쓰는 작가입니다.",
    "우주 정거장에서 길을 잃은 작은 로봇이 친구를 찾는 이야기를 5문장으로 써주세요.",
    scenario_name="chapter1.story_generator",
)

print(answer)

