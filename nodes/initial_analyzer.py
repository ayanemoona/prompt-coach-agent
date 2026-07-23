from __future__ import annotations

import json

from models.initial_state import create_initial_state
from models.state import PromptState
from prompts.analyzer_prompt import ANALYZER_PROMPT
from utils.llm import ask_llm, is_llm_configured
from utils.text import normalize_text


def analyze_initial_prompt(user_prompt: str) -> PromptState:
    # 초기 설정 
    prompt = normalize_text(user_prompt)
    state = create_initial_state()
    state["original_prompt"] = prompt
    state["current_prompt"] = prompt

    if is_llm_configured():
        try:
            analysis = analyze_prompt_with_llm(prompt)
            apply_analysis_to_state(state, analysis)
            return state
        except Exception:
            pass

    apply_rule_based_analysis(state, prompt)
    return state


def analyze_prompt_with_llm(prompt: str) -> dict:
    llm_prompt = ANALYZER_PROMPT.format(user_prompt=prompt)
    response = ask_llm(llm_prompt)
    return json.loads(response)


def apply_analysis_to_state(state: PromptState, analysis: dict) -> None:
    state["domain"] = analysis.get("domain")

    prompt_elements = analysis.get("prompt_elements", {})
    for element_name, element_value in prompt_elements.items():
        if element_name not in state["prompt_elements"]:
            continue

        state["prompt_elements"][element_name]["value"] = element_value.get("value")
        state["prompt_elements"][element_name]["confirmed"] = bool(
            element_value.get("confirmed")
        )


def apply_rule_based_analysis(state: PromptState, prompt: str) -> None:
    state["domain"] = detect_domain(prompt)

    detected_elements = detect_prompt_elements(prompt)
    for element_name, value in detected_elements.items():
        if element_name in state["prompt_elements"]:
            state["prompt_elements"][element_name]["value"] = value
            state["prompt_elements"][element_name]["confirmed"] = value is not None
