from __future__ import annotations

import os
from typing import TypeVar

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

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


def ask_llm(prompt: str, model: str = DEFAULT_MODEL) -> str:
    llm = create_llm(model=model)
    response = llm.invoke(prompt)
    return response.content


def ask_structured(
    prompt: str,
    schema: type[StructuredResult],
    model: str = DEFAULT_MODEL,
) -> StructuredResult:
    llm = create_llm(model=model)
    structured_llm = llm.with_structured_output(schema)
    response = structured_llm.invoke(prompt)

    if not isinstance(response, schema):
        raise RuntimeError(f"LLM response did not match {schema.__name__}.")

    return response
