from __future__ import annotations

import os
import time
from typing import TypeVar

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from utils.log_context import get_log_context
from utils.usage_logger import current_timestamp, extract_usage, write_usage_log

DEFAULT_MODEL = "gpt-4.1-mini"
StructuredResult = TypeVar("StructuredResult", bound=BaseModel)


load_dotenv()


def is_llm_configured() -> bool:
    return bool(os.getenv("OPENAI_API_KEY"))


def create_llm(model: str = DEFAULT_MODEL, temperature: float = 0) -> ChatOpenAI:
    if not is_llm_configured():
        raise RuntimeError(
            "OPENAI_API_KEY is not configured. Add it to your .env file."
        )

    return ChatOpenAI(
        model=model,
        temperature=temperature,
    )


def ask_llm(
    prompt: str,
    model: str = DEFAULT_MODEL,
    *,
    node: str = "unknown",
) -> str:
    response = invoke_with_usage_log(
        lambda: create_llm(model=model).invoke(prompt),
        model=model,
        node=node,
        prompt_chars=len(prompt),
        structured=False,
    )
    return response.content


def ask_structured(
    prompt: str,
    schema: type[StructuredResult],
    model: str = DEFAULT_MODEL,
    *,
    node: str = "unknown",
) -> StructuredResult:
    usage_source = {"response": None}

    def invoke() -> StructuredResult:
        llm = create_llm(model=model)
        structured_llm = llm.with_structured_output(schema, include_raw=True)
        response = structured_llm.invoke(prompt)

        if not isinstance(response, dict):
            raise RuntimeError("Structured LLM response did not include raw output.")

        usage_source["response"] = response.get("raw")
        parsing_error = response.get("parsing_error")
        if parsing_error is not None:
            raise RuntimeError(f"Structured output parsing failed: {parsing_error}")

        parsed = response.get("parsed")
        if not isinstance(parsed, schema):
            raise RuntimeError(f"LLM response did not match {schema.__name__}.")

        return parsed

    return invoke_with_usage_log(
        invoke,
        model=model,
        node=node,
        prompt_chars=len(prompt),
        structured=True,
        usage_response_getter=lambda: usage_source["response"],
    )


def invoke_with_usage_log(
    invoke,
    *,
    model: str,
    node: str,
    prompt_chars: int | None,
    structured: bool,
    usage_response_getter=None,
):
    started_at = time.perf_counter()
    response = None
    success = False
    error_type = None
    error_message = None

    try:
        response = invoke()
        success = True
        return response
    except Exception as error:
        error_type = type(error).__name__
        error_message = f"{type(error).__name__}: {error}"
        raise
    finally:
        latency_ms = int((time.perf_counter() - started_at) * 1000)
        usage_override = (
            usage_response_getter() if usage_response_getter is not None else None
        )
        usage_response = usage_override if usage_override is not None else response
        usage = extract_usage(usage_response)
        context = get_log_context()
        write_usage_log(
            {
                "timestamp": current_timestamp(),
                "run_id": context.get("run_id"),
                "experiment": context.get("experiment"),
                "source": context.get("source", "app"),
                "case_id": context.get("case_id"),
                "session_id": context.get("session_id"),
                "turn_index": context.get("turn_index"),
                "node": node,
                "model": model,
                "focus_element": context.get("focus_element"),
                "input_chars": context.get("input_chars"),
                "prompt_chars": context.get("prompt_chars", prompt_chars),
                "state_chars": context.get("state_chars"),
                "input_tokens": usage.get("input_tokens"),
                "output_tokens": usage.get("output_tokens"),
                "total_tokens": usage.get("total_tokens"),
                "latency_ms": latency_ms,
                "parse_success": success if structured else None,
                "success": success,
                "error_type": error_type,
                "error": error_message,
            }
        )
