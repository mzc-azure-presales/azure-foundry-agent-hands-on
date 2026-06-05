# 6시간 Microsoft Foundry Hands-on 시나리오

## 전체 이야기

이 교육은 하나의 사내 정책 Q&A 에이전트를 점진적으로 성숙시키는 흐름입니다. 처음에는 Foundry 프로젝트의 모델을 직접 호출하고, 이후 prompt-style agent, RAG, multi-agent UI, MCP 스타일 도구 서버, trace와 guardrails, 실제 Foundry Agent 생성까지 붙여 운영 가능한 에이전트 시스템으로 확장합니다.

강의는 오전 9시에 시작합니다. 기존 6시간 hands-on 흐름을 기준으로 하되, 매 1시간 학습 후 15분 휴식과 1시간 점심 시간을 포함해 오후 4시 5분까지 운영합니다.

## 진행 흐름

| 시간 | 구분 | 챕터 | 핵심 강의 내용 | 실행 파일 |
| --- | --- | --- | --- | --- |
| 09:00-09:20 | Hands-on | 준비 | Foundry 프로젝트, uv 환경(`uv sync`), `.env` 설정 준비 | `.env.example`, `pyproject.toml` |
| 09:20-10:00 | Hands-on | 1장 | Responses API 첫 호출, 역할 지시문, multi-turn 프롬프트 패턴 | `1.5_first_openai_call.py`, `1.6.4.4_mulit_turn.py` |
| 10:00-10:15 | 휴식 | - | 1시간 학습 후 15분 휴식 | - |
| 10:15-10:45 | Hands-on | 2장 | 공통 설정 검증, OpenAI-compatible client | `2.1_check_foundry_settings.py`, `2.2_foundry_responses_smoke_test.py`, `2.3_foundry_tracing_smoke_test.py` |
| 10:45-11:15 | Hands-on | 3장 | 역할 지시문 기반 prompt-style agent와 대화 상태 유지 구조 | `3.4.2_agent_app.py`, `3.4.5_stateful_agent.py` |
| 11:15-11:30 | 휴식 | - | 1시간 학습 후 15분 휴식 | - |
| 11:30-12:20 | Hands-on | 4장 | 로컬 도구 호출, 문서 기반 RAG, specialist handoff plan을 포함한 multi-tool routing | `4.2.1_multi_tool_agent.py`, `4.3.2_rag_agent.py`, 선택: `4.4.4.6_multi_tool_agent.py` |
| 12:20-13:20 | 점심 | - | 점심 시간 1시간 | - |
| 13:20-13:50 | Hands-on | 5장 | 여러 역할의 agent 순차 협업과 Streamlit UI 연결 | `5.2.1_multi_agent_system.py`, `5.3.1_streamlit_app.py` |
| 13:50-14:20 | Hands-on | 6장 | RAG 기능을 독립 HTTP 도구 서버로 분리하고 클라이언트에서 호출 | `6.6.1_mcp_server_ai_search.py`, `6.6.2_mcp_client_ai_search.py` |
| 14:20-14:35 | 휴식 | - | 1시간 학습 후 15분 휴식 | - |
| 14:35-15:05 | Hands-on | 7장 | guardrails, human review, reflection loop를 통한 운영 통제 패턴 | `7.3.1_langgraph_interrupt.py`, `7.4.1_reflection_loop.py`, `7.6.1_guardrails.py` |
| 15:05-15:55 | Hands-on | 8장 | Foundry Agent Service agent 생성, Search tool, Knowledge base, MCPTool, monitoring 연결 | `8.1_create_and_run_foundry_agent.py`, `8.2_create_foundry_agent_with_knowledge_base.py`, `8.3_create_foundry_agent_with_mcp.py`, `8.4_foundry_agent_monitoring.py` |
| 15:55-16:45 | 정리 | 전체 | 실행 결과, trace, 포털 monitoring 결과의 운영 관점 해석 | 전체 실행 로그와 Foundry 포털 확인 |

## 시간 운영 원칙

- 각 1시간 학습 단위 뒤에는 15분 휴식을 둡니다.
- 점심 시간은 12:20부터 13:20까지 1시간으로 운영합니다.
- 8장은 실제 Azure 리소스와 포털 확인 시간이 필요하므로 마지막 50분을 배정합니다.
- 시간이 부족하면 각 장의 선택 파일보다 필수 실행 파일을 우선합니다.
- 서버/클라이언트가 필요한 6장은 터미널을 2개 열어 진행하고, 실습 후 서버를 종료합니다.
- 15:55 이후에는 새 코드를 실행하기보다 오류, trace, 포털 화면, 학습 질문을 정리합니다.

## 강의자가 강조할 연결점

- 1장: 모델 호출은 모든 에이전트의 가장 작은 단위입니다.
- 2장: 공통 Foundry 실행 계층은 이후 모든 챕터의 기반입니다.
- 3장: prompt-style agent는 역할 지시문과 상태 관리의 필요성을 보여줍니다.
- 4장: RAG와 도구는 모델이 모르는 지식과 계산을 보완합니다.
- 5장: 복잡한 업무는 역할 분리와 UI로 확장합니다.
- 6장: 에이전트 기능은 API와 MCP 스타일 도구 서버로 분리되어야 재사용됩니다.
- 7장: 운영 시스템은 guardrails, human review, reflection 없이 완성되지 않습니다.
- 8장: 실제 Foundry Agent Service agent를 생성하고 RAG/Search tool, Knowledge base retrieve, MCPTool 코드 연결, 포털 모니터링을 확인합니다.

## 의도적으로 실패시키는 포인트

- `.env`에서 `FOUNDRY_OPENAI_ENDPOINT` 또는 `FOUNDRY_API_KEY`를 비워 인증/설정 오류를 확인합니다.
- 프롬프트 인젝션 문구를 넣어 guardrail이 차단하는지 확인합니다.
- RAG 질문을 문서에 없는 내용으로 바꿔 근거 부족 응답을 확인합니다.

## 최종 산출물

교육이 끝나면 학습자는 다음 구성을 이해하고 실행할 수 있어야 합니다.

- Foundry 프로젝트 기반 모델 호출
- 문서 기반 RAG 응답
- MCP 스타일 도구 서버
- Streamlit UI
- guardrails, human review, reflection 적용
- Foundry Agent Service 에이전트 생성, 정리, 포털 모니터링
- Knowledge base retrieve와 MCPTool 연결 구조
