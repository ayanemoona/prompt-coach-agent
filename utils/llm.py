from __future__ import annotations

import os
import time
from typing import TypeVar

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

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
    source: str = "app",
    experiment: str | None = None,
    run_id: str | None = None,
    case_id: str | None = None,
    session_id: str | None = None,
    turn_index: int | None = None,
    input_chars: int | None = None,
    prompt_chars: int | None = None,
    state_chars: int | None = None,
    focus_element: str | None = None,
) -> str:
    response = invoke_with_usage_log(
        lambda: create_llm(model=model).invoke(prompt),
        model=model,
        node=node,
        source=source,
        experiment=experiment,
        run_id=run_id,
        case_id=case_id,
        session_id=session_id,
        turn_index=turn_index,
        input_chars=input_chars,
        prompt_chars=prompt_chars if prompt_chars is not None else len(prompt),
        state_chars=state_chars,
        focus_element=focus_element,
        structured=False,
    )
    return response.content


def ask_structured(
    prompt: str,
    schema: type[StructuredResult],
    model: str = DEFAULT_MODEL,
    *,
    node: str = "unknown",
    source: str = "app",
    experiment: str | None = None,
    run_id: str | None = None,
    case_id: str | None = None,
    session_id: str | None = None,
    turn_index: int | None = None,
    input_chars: int | None = None,
    prompt_chars: int | None = None,
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
        source=source,
        experiment=experiment,
        run_id=run_id,
        case_id=case_id,
        session_id=session_id,
        turn_index=turn_index,
        input_chars=input_chars,
        prompt_chars=prompt_chars if prompt_chars is not None else len(prompt),
        state_chars=None,
        focus_element=None,
        structured=True,
        usage_response_getter=lambda: usage_source["response"],
    )


def invoke_with_usage_log(
    invoke,
    *,
    model: str,
    node: str,
    source: str,
    experiment: str | None,
    run_id: str | None,
    case_id: str | None,
    session_id: str | None,
    turn_index: int | None,
    input_chars: int | None,
    prompt_chars: int | None,
    state_chars: int | None,
    focus_element: str | None,
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
        write_usage_log(
            {
                "timestamp": current_timestamp(),
                "run_id": run_id,
                "experiment": experiment,
                "source": source,
                "case_id": case_id,
                "session_id": session_id,
                "turn_index": turn_index,
                "node": node,
                "model": model,
                "focus_element": focus_element,
                "input_chars": input_chars,
                "prompt_chars": prompt_chars,
                "state_chars": state_chars,
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
