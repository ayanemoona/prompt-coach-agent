from __future__ import annotations

import json
from copy import deepcopy

from models.state import PromptState
from prompts.analyzer_prompt import RESPONSE_ANALYZER_PROMPT
from utils.llm import ask_llm, is_llm_configured
from utils.state_updater import update_current_state
from utils.text import normalize_text


def analyze_user_revision(state: PromptState, user_input: str) -> PromptState:
    new_prompt = normalize_text(user_input)
    next_state: PromptState = deepcopy(state)
    next_state["current_prompt"] = new_prompt

    if is_llm_configured():
        try:
            analysis = analyze_revision(new_prompt)
            update_current_state(next_state, analysis)
            return next_state
        except Exception as error:
            raise RuntimeError("Response analyzer failed to analyze prompt with LLM.") from error

    raise RuntimeError("OPENAI_API_KEY is not configured. Response analyzer requires LLM.")


def analyze_revision(prompt: str) -> dict:
    llm_prompt = RESPONSE_ANALYZER_PROMPT.format(user_prompt=prompt)
    response = ask_llm(llm_prompt)
    return json.loads(response)
