# Run: uv run python check_env.py
# 목적: 실습 시작 전에 .env 설정이 제대로 잡혔는지 한 번에 검수합니다.
# 정책: MS Foundry 핵심 설정은 '필수'(없으면 실패), 8장 확장용 등 그 외 설정은
#       '선택'(없으면 경고)으로 구분해 보고합니다. 필수 항목이 하나라도 실패하면
#       종료 코드 1로 끝나므로, 사전 점검이나 CI에서 그대로 활용할 수 있습니다.
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Windows 콘솔(cp949 등)에서도 한글이 깨지거나 오류로 멈추지 않도록 출력을 UTF-8로 맞춥니다.
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except (AttributeError, ValueError):
    pass

# 저장소 루트의 .env를 읽습니다(이미 환경 변수로 설정된 값도 함께 인식합니다).
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_PATH)

# 이름에 아래 토큰이 들어간 변수는 비밀 값으로 보고 마스킹합니다.
SECRET_HINTS = ("KEY", "SECRET", "PASSWORD", "CONNECTION_STRING")

# (status, section, label, detail) - status in {"PASS", "WARN", "FAIL"}
checks: list[tuple[str, str, str, str]] = []


def _first_set(names: list[str]) -> tuple[str | None, str | None]:
    """별칭 목록에서 먼저 채워진 (값, 변수이름)을 반환합니다."""
    for name in names:
        raw = os.getenv(name)
        if raw and raw.strip():
            return raw.strip(), name
    return None, None


def _is_placeholder(value: str) -> bool:
    """`.env.example`의 <...> 자리표시자를 그대로 둔 경우를 감지합니다."""
    return "<" in value and ">" in value


def _display(name: str | None, value: str) -> str:
    """비밀 값은 길이만, 일반 값은 그대로 보여 줍니다."""
    if name and any(marker in name for marker in SECRET_HINTS):
        return f"설정됨 (길이 {len(value)}자)"
    return value


def _record(status: str, section: str, label: str, detail: str) -> None:
    checks.append((status, section, label, detail))


def require(section: str, label: str, names: list[str], validate=None) -> None:
    value, used = _first_set(names)
    if value is None:
        _record("FAIL", section, label, f"{names[0]} 미설정 (필수)")
        return
    if _is_placeholder(value):
        _record("FAIL", section, label, f"{used}가 자리표시자({value}) 그대로입니다. 실제 값으로 채우세요.")
        return
    problem = validate(value) if validate else None
    if problem:
        _record("FAIL", section, label, f"{used}: {problem}")
        return
    alias = "" if used == names[0] else f" (별칭 {used})"
    _record("PASS", section, label, f"{names[0]}{alias} = {_display(used, value)}")


def with_default(section: str, label: str, names: list[str], default: str, validate=None) -> None:
    value, used = _first_set(names)
    if value is None:
        _record("PASS", section, label, f"{names[0]} 미설정 - 기본값 '{default}' 사용")
        return
    problem = validate(value) if validate else None
    if problem:
        # 값을 넣었는데 형식이 틀린 경우는 기본값으로 가려지지 않으므로 실패로 봅니다.
        _record("FAIL", section, label, f"{used}: {problem}")
        return
    _record("PASS", section, label, f"{used} = {_display(used, value)}")


def optional(section: str, label: str, names: list[str], hint: str, validate=None) -> None:
    value, used = _first_set(names)
    if value is None:
        _record("WARN", section, label, f"{names[0]} 미설정 - {hint}")
        return
    if _is_placeholder(value):
        _record("WARN", section, label, f"{used}가 자리표시자({value}) 그대로입니다 - {hint}")
        return
    problem = validate(value) if validate else None
    if problem:
        _record("WARN", section, label, f"{used}: {problem}")
        return
    _record("PASS", section, label, f"{used} = {_display(used, value)}")


# --- validators: 문제가 있으면 메시지 문자열, 없으면 None ---


def v_url(value: str) -> str | None:
    if not value.startswith(("http://", "https://")):
        return "URL은 https:// 형식이어야 합니다."
    return None


def v_endpoint_type(value: str) -> str | None:
    if value.lower() not in {"azure_openai", "foundry"}:
        return f"azure_openai 또는 foundry 여야 합니다 (현재 '{value}')."
    return None


def v_reasoning(value: str) -> str | None:
    allowed = {"minimal", "low", "medium", "high", "none", "off", "false", "0", ""}
    if value.lower() not in allowed:
        return f"minimal/low/medium/high 또는 none/off 여야 합니다 (현재 '{value}')."
    return None


def v_search_endpoint(value: str) -> str | None:
    if not value.startswith("https://"):
        return "https:// 형식이어야 합니다."
    if not value.rstrip("/").endswith(".search.windows.net"):
        return "Azure AI Search endpoint는 .search.windows.net 으로 끝나야 합니다."
    return None


# === 검사 정의 ===

# 1) MS Foundry 핵심 설정 (필수: 없으면 실패) - 1장~7장 기본 모델/임베딩 호출에 필요
S_REQUIRED = "[필수] MS Foundry 핵심 설정"
require(S_REQUIRED, "Foundry endpoint", ["FOUNDRY_OPENAI_ENDPOINT", "AZURE_OPENAI_ENDPOINT"], v_url)
require(S_REQUIRED, "Foundry API key", ["FOUNDRY_API_KEY", "AZURE_OPENAI_API_KEY", "OPENAI_API_KEY"])
require(S_REQUIRED, "Chat 모델 배포", ["FOUNDRY_MODEL_DEPLOYMENT_NAME", "MODEL_DEPLOYMENT_NAME", "AZURE_OPENAI_DEPLOYMENT_NAME"])
require(S_REQUIRED, "Embedding 모델 배포", ["FOUNDRY_EMBEDDING_DEPLOYMENT_NAME", "AZURE_TEXT_EMBEDDING_MODEL"])

# 2) 기본값이 있어 없어도 동작하는 Foundry 설정 (값을 넣었다면 형식만 검증)
S_DEFAULT = "[기본값] 없어도 동작하는 Foundry 설정"
with_default(S_DEFAULT, "API version", ["FOUNDRY_OPENAI_API_VERSION", "AZURE_OPENAI_API_VERSION"], "2025-04-01-preview")
with_default(S_DEFAULT, "Endpoint type", ["FOUNDRY_OPENAI_ENDPOINT_TYPE", "AZURE_OPENAI_ENDPOINT_TYPE"], "azure_openai", v_endpoint_type)
with_default(S_DEFAULT, "Reasoning effort", ["FOUNDRY_REASONING_EFFORT"], "low", v_reasoning)

# 3) MS Foundry 이외 / 8장 확장용 설정 (선택: 없으면 경고)
S_OPTIONAL = "[선택] 8장 확장용 설정 (없으면 경고)"
optional(S_OPTIONAL, "Project endpoint", ["FOUNDRY_PROJECT_ENDPOINT"], "8장 Agent Service(8.1~8.4)에서 필요", v_url)
optional(S_OPTIONAL, "Project resource ID", ["FOUNDRY_PROJECT_RESOURCE_ID"], "8장 Agent Service에서 필요")
optional(S_OPTIONAL, "Azure AI Search endpoint", ["AZURE_SEARCH_ENDPOINT"], "8.1/8.2 RAG에서 필요", v_search_endpoint)
optional(S_OPTIONAL, "Azure AI Search API key", ["AZURE_SEARCH_API_KEY"], "8.1/8.2 RAG에서 필요")
optional(S_OPTIONAL, "Knowledge base 이름", ["FOUNDRY_KNOWLEDGE_BASE_NAME"], "8.2 Knowledge base 실습에서 필요")
optional(
    S_OPTIONAL,
    "Application Insights 연결 문자열",
    ["FOUNDRY_APPLICATIONINSIGHTS_CONNECTION_STRING", "APPLICATIONINSIGHTS_CONNECTION_STRING"],
    "트레이싱/8.4 모니터링에서 필요(없으면 콘솔 trace로 동작)",
)


# === 출력 ===
MARK = {"PASS": "[ OK ]", "WARN": "[경고]", "FAIL": "[실패]"}
LINE = "=" * 64


def main() -> int:
    print(LINE)
    print(" .env 설정 검수  (MS Foundry 핵심 = 필수 / 그 외 = 선택)")
    print(LINE)
    if not ENV_PATH.exists():
        print(f"\n알림: {ENV_PATH.name} 파일을 찾지 못했습니다. `.env.example`을 복사해 `.env`를 만든 뒤 값을 채우세요.")
        print("      (환경 변수로 직접 설정한 값이 있다면 그 값으로 검사합니다.)")

    for section in (S_REQUIRED, S_DEFAULT, S_OPTIONAL):
        print(f"\n{section}")
        for status, sec, label, detail in checks:
            if sec == section:
                print(f"  {MARK[status]} {label}: {detail}")

    fails = sum(1 for status, *_ in checks if status == "FAIL")
    warns = sum(1 for status, *_ in checks if status == "WARN")

    print("\n" + "-" * 64)
    print(f"요약: 실패 {fails}건, 경고 {warns}건")
    if fails:
        print("결과: 실패 - 위의 [실패] 항목(필수 설정)을 채운 뒤 다시 실행하세요.")
    elif warns:
        print("결과: 통과 - 필수 설정은 모두 정상입니다. [경고]는 8장 확장 실습을 할 때만 채우면 됩니다.")
    else:
        print("결과: 통과 - 모든 설정이 정상입니다.")
    print(LINE)

    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
