from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator, TypedDict


class LogContext(TypedDict, total=False):
    source: str
    experiment: str | None
    run_id: str | None
    case_id: str | None
    session_id: str | None
    turn_index: int | None
    input_chars: int | None
    prompt_chars: int | None
    state_chars: int | None
    focus_element: str | None


_log_context: ContextVar[LogContext] = ContextVar(
    "log_context",
    default={"source": "app"},
)


def get_log_context() -> LogContext:
    return dict(_log_context.get())


@contextmanager
def logging_context(**updates: object) -> Iterator[None]:
    current = get_log_context()
    next_context = {**current, **updates}
    token = _log_context.set(next_context)  # type: ignore[arg-type]
    try:
        yield
    finally:
        _log_context.reset(token)
