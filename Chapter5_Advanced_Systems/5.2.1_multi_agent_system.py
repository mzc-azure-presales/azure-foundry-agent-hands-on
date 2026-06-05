# Run: uv run Chapter5_Advanced_Systems/5.2.1_multi_agent_system.py
# 학습 포인트: 여러 에이전트 역할을 나누어 초안 작성과 검토를 수행합니다.
# 초보자 읽기: 연구 에이전트의 출력이 작성 에이전트의 입력으로 이어지며 두 역할이 순차적으로 협업하는 구조를 봅니다.
from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_prompt_agent, run_single_turn_prompt

load_dotenv()


if __name__ == "__main__":
    topic = "2026년 엔터프라이즈 AI 에이전트 트렌드"

    research = run_prompt_agent(
        agent_name="hands-on-research-agent",
        instructions="You are a senior research analyst. Produce concise Korean research notes with risks and opportunities.",
        user_input=f"{topic}에 대한 핵심 동향을 조사 보고서 형식으로 정리해줘.",
        scenario_name="chapter5.multi_agent.researcher",
    )

    draft = run_single_turn_prompt(
        "You are a technical content strategist writing for Korean enterprise developers.",
        f"다음 연구 노트를 바탕으로 5문단 블로그 초안을 작성해줘.\n\n{research}",
        scenario_name="chapter5.multi_agent.writer",
    )

    print("## 연구원 결과\n")
    print(research)
    print("\n## 작성자 결과\n")
    print(draft)
