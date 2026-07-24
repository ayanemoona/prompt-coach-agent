from __future__ import annotations

import json
from copy import deepcopy

from models.state import PromptState
from prompts.analyzer_prompt import (
    ANALYZER_PROMPT,
    CURRENT_ANALYSIS_MODE,
    CURRENT_OUTPUT_SCHEMA,
    INITIAL_ANALYSIS_MODE,
    INITIAL_OUTPUT_SCHEMA,
)
from utils.llm import ask_llm, is_llm_configured
from utils.state_updater import update_current_state, update_initial_state


def analyze_prompt(state: PromptState, user_input: str) -> PromptState:
    if state["original_prompt"] is None:
        return analyze_initial_prompt(state, user_input)

    return analyze_user_revision(state, user_input)


def analyze_initial_prompt(state: PromptState, user_prompt: str) -> PromptState:
    next_state: PromptState = deepcopy(state)
    next_state["original_prompt"] = user_prompt
    next_state["current_prompt"] = user_prompt

    if is_llm_configured():
        try:
            analysis = run_analysis(
                INITIAL_ANALYSIS_MODE,
                INITIAL_OUTPUT_SCHEMA,
                user_prompt,
            )
            update_initial_state(next_state, analysis)
            return next_state
        except Exception as error:
            raise RuntimeError("Initial analyzer failed to analyze prompt with LLM.") from error

    raise RuntimeError("OPENAI_API_KEY is not configured. Analyzer requires LLM.")


def analyze_user_revision(state: PromptState, user_input: str) -> PromptState:
    next_state: PromptState = deepcopy(state)
    next_state["current_prompt"] = user_input

    if is_llm_configured():
        try:
            analysis = run_analysis(
                CURRENT_ANALYSIS_MODE,
                CURRENT_OUTPUT_SCHEMA,
                user_input,
            )
            update_current_state(next_state, analysis)
            return next_state
        except Exception as error:
            raise RuntimeError("Response analyzer failed to analyze prompt with LLM.") from error

    raise RuntimeError("OPENAI_API_KEY is not configured. Analyzer requires LLM.")


def run_analysis(analysis_mode: str, output_schema: str, user_prompt: str) -> dict:
    llm_prompt = (
        ANALYZER_PROMPT
        .replace("{analysis_mode}", analysis_mode)
        .replace("{output_schema}", output_schema)
        .replace("{user_prompt}", user_prompt)
    )
    response = ask_llm(llm_prompt)
    return json.loads(response)
