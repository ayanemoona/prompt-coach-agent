from __future__ import annotations

from copy import deepcopy
from typing import TypeAlias

from models.analysis import CurrentAnalysis, InitialAnalysis
from models.state import PromptState
from prompts.analyzer_prompt import (
    ANALYZER_PROMPT,
    CURRENT_ANALYSIS_MODE,
    CURRENT_OUTPUT_SCHEMA,
    INITIAL_ANALYSIS_MODE,
    INITIAL_OUTPUT_SCHEMA,
)
from utils.llm import ask_structured, is_llm_configured
from utils.state_updater import update_current_state, update_initial_state

AnalysisSchema: TypeAlias = type[InitialAnalysis] | type[CurrentAnalysis]


def analyze_prompt(
    state: PromptState,
    user_input: str,
    *,
    session_id: str | None = None,
    turn_index: int | None = None,
) -> PromptState:
    if state["original_prompt"] is None:
        return analyze_initial_prompt(
            state,
            user_input,
            session_id=session_id,
            turn_index=turn_index,
        )

    return analyze_user_revision(
        state,
        user_input,
        session_id=session_id,
        turn_index=turn_index,
    )


def analyze_initial_prompt(
    state: PromptState,
    user_prompt: str,
    *,
    session_id: str | None = None,
    turn_index: int | None = None,
) -> PromptState:
    next_state: PromptState = deepcopy(state)
    next_state["original_prompt"] = user_prompt
    next_state["current_prompt"] = user_prompt

    if is_llm_configured():
        try:
            analysis = run_analysis(
                INITIAL_ANALYSIS_MODE,
                INITIAL_OUTPUT_SCHEMA,
                user_prompt,
                InitialAnalysis,
                node="analyzer.initial",
                session_id=session_id,
                turn_index=turn_index,
            )
            update_initial_state(next_state, analysis)
            return next_state
        except Exception as error:
            raise RuntimeError(
                "Initial analyzer failed to analyze prompt with LLM."
            ) from error

    raise RuntimeError("OPENAI_API_KEY is not configured. Analyzer requires LLM.")


def analyze_user_revision(
    state: PromptState,
    user_input: str,
    *,
    session_id: str | None = None,
    turn_index: int | None = None,
) -> PromptState:
    next_state: PromptState = deepcopy(state)
    next_state["current_prompt"] = user_input

    if is_llm_configured():
        try:
            analysis = run_analysis(
                CURRENT_ANALYSIS_MODE,
                CURRENT_OUTPUT_SCHEMA,
                user_input,
                CurrentAnalysis,
                node="analyzer.revision",
                session_id=session_id,
                turn_index=turn_index,
            )
            update_current_state(next_state, analysis)
            return next_state
        except Exception as error:
            raise RuntimeError(
                "Response analyzer failed to analyze prompt with LLM."
            ) from error

    raise RuntimeError("OPENAI_API_KEY is not configured. Analyzer requires LLM.")


def run_analysis(
    analysis_mode: str,
    output_schema: str,
    user_prompt: str,
    schema: AnalysisSchema,
    *,
    node: str,
    session_id: str | None = None,
    turn_index: int | None = None,
) -> dict:
    llm_prompt = (
        ANALYZER_PROMPT.replace("{analysis_mode}", analysis_mode)
        .replace("{output_schema}", output_schema)
        .replace("{user_prompt}", user_prompt)
    )
    response = ask_structured(
        llm_prompt,
        schema,
        node=node,
        session_id=session_id,
        turn_index=turn_index,
        input_chars=len(user_prompt),
        prompt_chars=len(llm_prompt),
    )
    return response.model_dump()
