from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

LOG_DIR = Path("logs")
APP_LOG_PATH = LOG_DIR / "app_usage.jsonl"
EVALUATION_LOG_PATH = LOG_DIR / "evaluation_usage.jsonl"

COMMON_FIELDS = (
    "timestamp",
    "source",
    "session_id",
    "turn_index",
    "node",
    "model",
    "focus_element",
    "input_chars",
    "prompt_chars",
    "state_chars",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "latency_ms",
    "parse_success",
    "success",
    "error_type",
    "error",
)

EVALUATION_FIELDS = (
    "run_id",
    "experiment",
    "case_id",
    *COMMON_FIELDS,
)

APP_FIELDS = COMMON_FIELDS


def extract_usage(response: Any) -> dict[str, int | None]:
    if response is None:
        return empty_usage()

    usage_metadata = getattr(response, "usage_metadata", None)
    if isinstance(usage_metadata, dict):
        return {
            "input_tokens": usage_metadata.get("input_tokens"),
            "output_tokens": usage_metadata.get("output_tokens"),
            "total_tokens": usage_metadata.get("total_tokens"),
        }

    token_usage = getattr(response, "response_metadata", {}).get("token_usage")
    if isinstance(token_usage, dict):
        return {
            "input_tokens": token_usage.get("prompt_tokens"),
            "output_tokens": token_usage.get("completion_tokens"),
            "total_tokens": token_usage.get("total_tokens"),
        }

    return empty_usage()


def empty_usage() -> dict[str, None]:
    return {
        "input_tokens": None,
        "output_tokens": None,
        "total_tokens": None,
    }


def write_usage_log(record: dict[str, object]) -> None:
    path, fields = select_log_target(record)
    path.parent.mkdir(exist_ok=True)
    scoped_record = {field: record.get(field) for field in fields}

    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(scoped_record, ensure_ascii=False) + "\n")


def select_log_target(
    record: dict[str, object],
) -> tuple[Path, tuple[str, ...]]:
    if record.get("source") == "evaluation":
        return EVALUATION_LOG_PATH, EVALUATION_FIELDS

    return APP_LOG_PATH, APP_FIELDS


def current_timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
