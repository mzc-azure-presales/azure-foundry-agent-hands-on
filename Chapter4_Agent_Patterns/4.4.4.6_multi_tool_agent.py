# Run: uv run Chapter4_Agent_Patterns/4.4.4.6_multi_tool_agent.py
# 학습 포인트: AI가 도구 사용 계획을 세우고 calculator, RAG, human review, specialist handoff 계획을 실행합니다.
# 초보자 읽기: 모델이 JSON으로 도구 사용 계획을 만들고, 코드가 RAG, 계산기, 사람 검토, 전문가 위임 계획 도구를 실행하는 흐름을 봅니다.
import json

from dotenv import load_dotenv

import _bootstrap  # noqa: F401
from foundry_hands_on import run_single_turn_prompt
from foundry_hands_on.rag import retrieve_local_context

load_dotenv()


def calculator_tool(expression: str) -> str:
    allowed = set("0123456789+-*/(). ")
    if any(char not in allowed for char in expression):
        raise ValueError("Only arithmetic characters are allowed.")
    return str(eval(expression, {"__builtins__": {}}, {}))


def rag_search_tool(query: str) -> str:
    contexts = retrieve_local_context(
        document_path="Chapter4_Agent_Patterns/company_policy.txt",
        query=query,
        top_k=2,
        scenario_name="chapter4.multi_tool_router.rag",
    )
    return "\n\n---\n\n".join(contexts)


def human_review_tool(reason: str) -> str:
    return f"사람 검토 필요: {reason}"


def specialist_handoff_tool(target_agent: str, task: str) -> str:
    return (
        f"전문가 위임 계획: '{target_agent}' 역할에게 '{task}'를 넘기도록 설계합니다. "
        "현재 API key 실습에서는 실제 원격 호출 대신 prompt 단계 분리 또는 MCP 도구 서버로 확장할 수 있습니다."
    )


def plan_tools_with_agent(user_request: str) -> list[dict[str, str]]:
    available_tools = [
        {
            "tool": "RAG search",
            "when_to_use": "회사 정책, 휴가, 병가, 재택 근무처럼 문서 근거가 필요한 질문",
        },
        {
            "tool": "calculator",
            "when_to_use": "숫자 계산, 예산 계산, 산술 결과가 필요한 질문",
        },
        {
            "tool": "human review",
            "when_to_use": "정책 해석이 애매하거나 승인/예외 판단이 필요한 질문",
        },
        {
            "tool": "specialist handoff plan",
            "when_to_use": "전문 HR 에이전트 같은 별도 역할에게 위임하는 구조를 설계해야 하는 질문",
        },
    ]
    raw_plan = run_single_turn_prompt(
        "You are a tool-routing planner. Select the tools needed for the user request. Return only valid JSON, no markdown.",
        (
            f"Available tools:\n{available_tools}\n\n"
            f"User request:\n{user_request}\n\n"
            "Return JSON with this exact shape: "
            "[{\"tool\": \"RAG search\", \"reason\": \"...\", \"tool_input\": \"...\"}]"
        ),
        scenario_name="chapter4.multi_tool_router.plan",
        print_usage=False,
    )
    try:
        plan = json.loads(raw_plan)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Tool routing planner returned invalid JSON: {raw_plan}") from exc

    if not isinstance(plan, list):
        raise RuntimeError(f"Tool routing planner must return a JSON list: {raw_plan}")
    return plan


def execute_tool_step(step: dict[str, str], user_request: str) -> dict[str, str]:
    tool = step.get("tool", "")
    reason = step.get("reason", "")
    tool_input = step.get("tool_input") or user_request

    if tool == "RAG search":
        result = rag_search_tool(tool_input)
    elif tool == "calculator":
        result = calculator_tool(tool_input)
    elif tool == "human review":
        result = human_review_tool(tool_input)
    elif tool == "specialist handoff plan":
        result = specialist_handoff_tool("HR policy specialist", tool_input)
    else:
        result = f"지원하지 않는 도구입니다: {tool}"

    return {
        "tool": tool,
        "reason": reason,
        "tool_input": tool_input,
        "result": result,
    }


def route_tools(user_request: str) -> list[dict[str, str]]:
    tool_plan = plan_tools_with_agent(user_request)
    print("\n[AI가 판단한 도구 사용 계획]")
    print(json.dumps(tool_plan, ensure_ascii=False, indent=2))
    return [execute_tool_step(step, user_request) for step in tool_plan]


if __name__ == "__main__":
    user_request = "직원 휴가 규정을 확인한 뒤, 결과가 애매하면 HR 전문 에이전트에게 handoff하는 흐름을 설계해줘."
    print("사용자 요청:", user_request)

    tool_results = route_tools(user_request)
    print("\n[라우터가 선택하고 실행한 도구]")
    for index, tool_result in enumerate(tool_results, start=1):
        print(f"\n--- tool {index}: {tool_result['tool']} ---")
        print("선택 이유:", tool_result["reason"])
        print("도구 입력:", tool_result["tool_input"])
        print("도구 결과:")
        print(tool_result["result"])

    answer = run_single_turn_prompt(
        "You are a prompt-style multi-tool orchestrator. Summarize the executed tool results into a practical workflow. Answer in Korean.",
        f"User request:\n{user_request}\n\nExecuted tool results:\n{tool_results}",
        scenario_name="chapter4.multi_tool_router.final_answer",
    )

    print("\n[최종 에이전트 응답]")
    print(answer)
