# Run: uv run Chapter1_Getting_Started/1.6.4.4_mulit_turn.py
# 학습 포인트: 이전 대화 기록을 messages에 누적해 멀티턴 맥락을 유지합니다.
# 초보자 읽기: 같은 messages 리스트에 1턴 답변을 저장한 뒤 2턴 질문에서 이전 여행 계획을 다시 활용하는 흐름을 봅니다.
# multi_turn.py
from dotenv import load_dotenv
import _bootstrap  # noqa: F401
from foundry_hands_on import run_threaded_prompt


def print_conversation_history(messages: list[dict[str, str]]) -> None:
    print("\n[현재까지 누적된 대화 기록]")
    for index, message in enumerate(messages, start=1):
        print(f"{index}. {message['role']}: {message['content']}")


def create_travel_plan_chatbot() -> None:
    load_dotenv()
    messages = [
        {
            "role": "system",
            "content": "당신은 여행 가이드입니다. 사용자의 질문을 기반으로 맞춤형 계획을 세우세요. 모든 응답은 사용자 친화적인 JSON 형식이어야 합니다.",
        }
    ]

    print("멀티턴 대화 예제: 같은 messages 리스트에 대화 기록을 계속 누적합니다.")
    print_conversation_history(messages)

    first = "파리로 여행 갈 계획인데, 예산이 1000유로예요."
    print("\n[1단계 요청]")
    print(f"사용자: {first}")
    answer_1 = run_threaded_prompt(
        messages,
        first,
        scenario_name="chapter1.multi_turn.first",
    )
    print(f"\nFoundry (1단계): {answer_1}")
    print_conversation_history(messages)

    second = "그 계획에 음식 추천을 추가해 주세요."
    print("\n[2단계 요청]")
    print("2단계 요청은 1단계 사용자 질문과 Foundry 응답을 함께 기억한 상태로 전달됩니다.")
    print(f"\n사용자: {second}")
    answer_2 = run_threaded_prompt(
        messages,
        second,
        scenario_name="chapter1.multi_turn.second",
    )
    print(f"\nFoundry (2단계): {answer_2}")
    print_conversation_history(messages)

if __name__ == "__main__":
    create_travel_plan_chatbot()

