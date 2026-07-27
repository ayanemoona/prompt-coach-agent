from __future__ import annotations

import json

from models.state import PromptState
from prompts.coach_prompt import COACH_PROMPT
from utils.llm import ask_llm, is_llm_configured


def create_coaching_message(state: PromptState) -> str:
    if not is_llm_configured():
        raise RuntimeError("OPENAI_API_KEY is not configured. Coach requires LLM.")

    prompt = build_coach_prompt(state)
    return ask_llm(prompt)


def build_coach_prompt(state: PromptState) -> str:
    state_json = json.dumps(state, ensure_ascii=False, indent=2)
    return COACH_PROMPT.format(state=state_json)
