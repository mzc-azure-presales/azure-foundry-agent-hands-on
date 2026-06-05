import os
import sys
from contextlib import contextmanager
from typing import Iterator

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor


_tracing_configured = False


def configure_console_tracing() -> None:
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter(out=sys.stdout)))
    try:
        trace.set_tracer_provider(provider)
    except Exception:
        pass


def configure_foundry_tracing() -> None:
    # Application Insights 연결이 있으면 Azure Monitor로, 없으면 콘솔로 trace를 보냅니다.
    global _tracing_configured
    if _tracing_configured:
        return

    os.environ.setdefault("AZURE_EXPERIMENTAL_ENABLE_GENAI_TRACING", "true")
    os.environ.setdefault(
        "AZURE_TRACING_GEN_AI_CONTENT_RECORDING_ENABLED",
        "false",
    )
    connection_string = (
        os.getenv("FOUNDRY_APPLICATIONINSIGHTS_CONNECTION_STRING")
        or os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    )
    if connection_string:
        try:
            from azure.monitor.opentelemetry import configure_azure_monitor

            configure_azure_monitor(connection_string=connection_string)
            print("Application Insights trace exporter를 설정했습니다.")
        except Exception as exc:
            print("Application Insights trace exporter 설정에 실패해 콘솔 trace로 계속 진행합니다.")
            print(f"Trace exporter 오류: {exc}")
            configure_console_tracing()
    else:
        configure_console_tracing()

    _tracing_configured = True


@contextmanager
def foundry_span(name: str) -> Iterator[None]:
    # with foundry_span("name") 형태로 각 실습 실행 구간을 trace span으로 감쌉니다.
    configure_foundry_tracing()
    tracer = trace.get_tracer("azure-foundry-agent-hands-on")
    with tracer.start_as_current_span(name):
        yield
