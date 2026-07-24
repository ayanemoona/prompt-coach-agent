from __future__ import annotations

import json

from models.initial_state import create_initial_state
from models.state import PromptState
from prompts.analyzer_prompt import ANALYZER_PROMPT
from utils.llm import ask_llm, is_llm_configured
from utils.text import normalize_text
from utils.state_updater import update_state


def analyze_initial_prompt(user_prompt: str) -> PromptState:
    # 초기 설정 
    prompt = normalize_text(user_prompt)
    state = create_initial_state()
    state["original_prompt"] = prompt
    state["current_prompt"] = prompt

    if is_llm_configured():
        try:
            analysis = analyze_prompt(prompt)
            update_state(state, analysis)
            return state
        except Exception as error:
            raise RuntimeError("Initial analyzer failed to analyze prompt with LLM.") from error

    raise RuntimeError("OPENAI_API_KEY is not configured. Initial analyzer requires LLM.")


def analyze_prompt(prompt: str) -> dict:
    llm_prompt = ANALYZER_PROMPT.format(user_prompt=prompt)
    response = ask_llm(llm_prompt)
    return json.loads(response)
