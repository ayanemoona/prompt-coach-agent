from __future__ import annotations

import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

DEFAULT_MODEL = "gpt-4.1-mini"


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
