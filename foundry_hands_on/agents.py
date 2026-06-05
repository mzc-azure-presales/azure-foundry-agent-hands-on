from typing import Any

from .client import run_single_turn_prompt
from .tracing import foundry_span


def run_prompt_agent(
    *,
    agent_name: str,
    instructions: str,
    user_input: str,
    scenario_name: str,
    tools: list[Any] | None = None,
    tool_choice: str | None = None,
    cleanup: bool = True,
) -> str:
    # 실제 Agent Service 생성 없이 system instruction을 agent 역할처럼 사용하는 입문용 경로입니다.
    with foundry_span(scenario_name):
        if tools or tool_choice:
            raise RuntimeError(
                "Agent tools require Foundry Agent Service and Entra ID credentials. "
                "The API-key mode supports prompt-style agent examples without tool attachment."
            )
        print(f"Running prompt-style agent with API key: {agent_name}")
        return run_single_turn_prompt(
            instructions,
            user_input,
            scenario_name=f"{scenario_name}.responses",
            print_usage=False,
        )
