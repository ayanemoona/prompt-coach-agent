from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

LOG_PATH = Path("logs") / "llm_usage.jsonl"


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
    LOG_PATH.parent.mkdir(exist_ok=True)
    with LOG_PATH.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")


def current_timestamp() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
