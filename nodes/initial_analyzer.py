from __future__ import annotations

from models.initial_state import create_initial_state
from models.state import PromptState
from utils.parser import detect_domain, detect_prompt_elements, normalize_text


def analyze_initial_prompt(user_prompt: str) -> PromptState:
    prompt = normalize_text(user_prompt)
    state = create_initial_state()

    state["original_prompt"] = prompt
    state["current_prompt"] = prompt
    state["domain"] = detect_domain(prompt)

    detected_elements = detect_prompt_elements(prompt)
    for element_name, value in detected_elements.items():
        if element_name in state["prompt_elements"]:
            state["prompt_elements"][element_name]["value"] = value
            state["prompt_elements"][element_name]["confirmed"] = value is not None

    return state
