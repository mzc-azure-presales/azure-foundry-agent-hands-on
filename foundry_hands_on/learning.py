from pathlib import Path
import inspect


_printed_paths: set[Path] = set()


def _find_script_path() -> Path | None:
    # _bootstrap에서 호출되어도 실제 실행 중인 챕터 파일을 찾아 학습 목표를 읽습니다.
    for frame_info in inspect.stack()[1:]:
        path = Path(frame_info.filename).resolve()
        if path.name == "_bootstrap.py" or path.name == "learning.py":
            continue
        if path.suffix == ".py" and path.exists():
            return path
    return None


def _read_header_value(script_path: Path, prefix: str) -> str | None:
    try:
        lines = script_path.read_text(encoding="utf-8-sig").splitlines()
    except OSError:
        return None

    for line in lines[:20]:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped.removeprefix(prefix).strip()
    return None


def _beginner_explanation(learning_point: str) -> str:
    # 학습 포인트의 키워드를 보고 초보자용 쉬운 설명 한 줄을 자동으로 붙입니다.
    text = learning_point.lower()
    if "streamlit" in text:
        return "터미널 예제를 웹 화면으로 감싸서 사용자가 직접 입력하고 결과를 볼 수 있게 만드는 단계입니다."
    if "handoff" in text:
        return "한 에이전트가 모든 일을 하지 않고, 다른 에이전트나 역할에 일을 넘기는 구조를 보는 단계입니다."
    if "knowledge bases" in text or "knowledge base" in text:
        return "Foundry 포털에서 만든 지식 베이스를 agent에 연결해 embedding 코드를 직접 작성하지 않고 검색 기반 답변을 만드는 단계입니다."
    if "mcp" in text or "서버" in text or "endpoint" in text:
        return "모델 기능이나 검색 기능을 별도 서버로 분리해 다른 프로그램이 HTTP 요청으로 부르는 구조를 보는 단계입니다."
    if "monitor" in text or "모니터링" in text or "메트릭" in text:
        return "Foundry 포털에서 agent 실행 횟수, 토큰 사용량, 평가 상태 같은 운영 신호를 읽는 단계입니다."
    if "rag" in text or "문서" in text or "pdf" in text or "embedding" in text or "chunk" in text or "vector" in text:
        return "모델이 기억만으로 답하지 않고, 문서에서 관련 내용을 찾은 뒤 그 근거로 답하게 만드는 단계입니다."
    if "tool" in text or "도구" in text or "계산" in text or "calculator" in text:
        return "모델이 직접 하기 어려운 계산, 검색, 조회를 로컬 함수나 외부 기능에 맡기고 결과를 활용하는 단계입니다."
    if "trace" in text or "opentelemetry" in text or "관찰" in text:
        return "요청이 어떤 흐름으로 실행됐는지 기록을 남겨 문제 원인과 실행 시간을 확인하는 단계입니다."
    if "guardrail" in text or "분류" in text or "제한" in text:
        return "모델이 위험하거나 근거 없는 답을 하지 않도록 입력과 출력을 검사하는 안전장치를 보는 단계입니다."
    if "reflection" in text or "자기 검토" in text:
        return "모델이 초안을 만든 뒤 스스로 다시 검토해서 더 나은 답변으로 고치는 흐름을 보는 단계입니다."
    if "stateful" in text or "멀티턴" in text or "대화" in text or "messages" in text:
        return "이전 대화를 함께 보내서 모델이 앞의 맥락을 기억하는 것처럼 동작하게 만드는 단계입니다."
    if "few-shot" in text:
        return "정답 예시 몇 개를 먼저 보여줘서 모델이 같은 형식과 규칙을 따라 답하게 만드는 단계입니다."
    if "system prompt" in text or "역할" in text or "prompt" in text:
        return "모델에게 역할, 말투, 출력 형식 같은 지시를 주면 응답이 어떻게 달라지는지 보는 단계입니다."
    if "responses api" in text or "첫 요청" in text or "foundry 모델" in text:
        return "Foundry 모델에 요청을 보내고 응답을 받는 가장 기본 실행 흐름을 확인하는 단계입니다."
    if ".env" in text or "설정" in text:
        return "실습에 필요한 endpoint, API key, 모델 배포명 같은 환경 설정이 제대로 들어왔는지 확인하는 단계입니다."
    return "이 파일의 입력, 중간 처리, 최종 출력을 차례로 보면서 학습 목표가 코드에서 어디에 나타나는지 확인하는 단계입니다."


def print_script_learning_goal() -> None:
    # 각 실습 파일 시작 시 Run 명령, 학습 목표, 관찰 포인트를 한 번만 출력합니다.
    script_path = _find_script_path()
    if not script_path:
        return

    if script_path in _printed_paths:
        return
    _printed_paths.add(script_path)

    run_command = _read_header_value(script_path, "# Run:")
    learning_point = _read_header_value(script_path, "# 학습 포인트:")
    if not learning_point:
        return

    print("\n" + "=" * 72)
    print(f"실습 파일: {script_path.name}")
    if run_command:
        print(f"실행 명령: {run_command}")
    print("학습 목표:")
    print(f"- {learning_point}")
    print("쉽게 말하면:")
    print(f"- {_beginner_explanation(learning_point)}")
    print("관찰 포인트:")
    print("- 이 파일이 어떤 입력을 준비하는지 확인합니다.")
    print("- 어떤 로컬 도구, RAG, 에이전트 역할, 서버 endpoint를 사용하는지 확인합니다.")
    print("- 마지막 출력이 학습 목표와 어떻게 연결되는지 확인합니다.")
    print("=" * 72 + "\n")
