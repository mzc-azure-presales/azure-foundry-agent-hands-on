import os
from dataclasses import dataclass

from dotenv import load_dotenv


def get_model_deployment_name() -> str:
    # 여러 실습 환경에서 쓰는 배포명 변수 이름을 같은 의미로 받아들입니다.
    load_dotenv(override=False)
    model_deployment_name = (
        os.getenv("FOUNDRY_MODEL_DEPLOYMENT_NAME")
        or os.getenv("MODEL_DEPLOYMENT_NAME")
        or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    )
    if not model_deployment_name:
        raise RuntimeError(
            "FOUNDRY_MODEL_DEPLOYMENT_NAME is required. See README.md for the .env template."
        )
    return model_deployment_name


@dataclass(frozen=True)
class FoundrySettings:
    # 각 챕터가 직접 os.getenv를 반복하지 않도록 Foundry 연결 정보를 한 곳에 모읍니다.
    openai_endpoint: str
    api_key: str
    openai_api_version: str
    openai_endpoint_type: str
    project_endpoint: str | None
    model_deployment_name: str
    embedding_deployment_name: str | None
    reasoning_effort: str | None


def get_reasoning_effort() -> str | None:
    load_dotenv(override=False)
    value = os.getenv("FOUNDRY_REASONING_EFFORT", "low").strip().lower()
    if value in {"", "0", "false", "none", "off"}:
        return None
    allowed = {"minimal", "low", "medium", "high"}
    if value not in allowed:
        raise RuntimeError(
            "FOUNDRY_REASONING_EFFORT must be one of: "
            + ", ".join(sorted(allowed))
            + ", or none/off to disable."
        )
    return value


def get_reasoning_kwargs() -> dict[str, dict[str, str]]:
    reasoning_effort = get_reasoning_effort()
    if not reasoning_effort:
        return {}
    return {"reasoning": {"effort": reasoning_effort}}


def get_settings() -> FoundrySettings:
    # 기본 실습은 API key 기반 OpenAI-compatible endpoint 호출을 사용합니다.
    load_dotenv(override=False)

    openai_endpoint = (
        os.getenv("FOUNDRY_OPENAI_ENDPOINT")
        or os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    api_key = (
        os.getenv("FOUNDRY_API_KEY")
        or os.getenv("AZURE_OPENAI_API_KEY")
        or os.getenv("OPENAI_API_KEY")
    )
    openai_api_version = (
        os.getenv("FOUNDRY_OPENAI_API_VERSION")
        or os.getenv("AZURE_OPENAI_API_VERSION")
        or "2025-04-01-preview"
    )
    openai_endpoint_type = (
        os.getenv("FOUNDRY_OPENAI_ENDPOINT_TYPE")
        or os.getenv("AZURE_OPENAI_ENDPOINT_TYPE")
        or "azure_openai"
    ).lower()
    model_deployment_name = get_model_deployment_name()
    embedding_deployment_name = (
        os.getenv("FOUNDRY_EMBEDDING_DEPLOYMENT_NAME")
        or os.getenv("AZURE_TEXT_EMBEDDING_MODEL")
    )

    missing = []
    if not openai_endpoint:
        missing.append("FOUNDRY_OPENAI_ENDPOINT")
    if not api_key:
        missing.append("FOUNDRY_API_KEY")
    if not model_deployment_name:
        missing.append("FOUNDRY_MODEL_DEPLOYMENT_NAME")

    if missing:
        raise RuntimeError(
            "Missing required Foundry environment variables: "
            + ", ".join(missing)
            + ". See README.md for the .env template."
        )

    # 위 missing 검사를 통과했으므로 endpoint와 api_key는 None이 아닙니다(타입 좁히기).
    assert openai_endpoint is not None and api_key is not None
    return FoundrySettings(
        openai_endpoint=openai_endpoint,
        api_key=api_key,
        openai_api_version=openai_api_version,
        openai_endpoint_type=openai_endpoint_type,
        project_endpoint=project_endpoint,
        model_deployment_name=model_deployment_name,
        embedding_deployment_name=embedding_deployment_name,
        reasoning_effort=get_reasoning_effort(),
    )


def get_project_endpoint() -> str:
    # 8장처럼 실제 Foundry 프로젝트 리소스를 다루는 선택 실습에서만 필요합니다.
    load_dotenv(override=False)
    project_endpoint = os.getenv("FOUNDRY_PROJECT_ENDPOINT")
    if not project_endpoint:
        raise RuntimeError(
            "FOUNDRY_PROJECT_ENDPOINT is required for Foundry Agent Service examples. "
            "Use the project endpoint in the form https://<resource>.services.ai.azure.com/api/projects/<project>."
        )
    return project_endpoint
