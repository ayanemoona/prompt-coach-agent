from __future__ import annotations

from copy import deepcopy

from models.state import PromptState
from utils.parser import detect_domain, detect_prompt_elements, normalize_text


def analyze_user_revision(state: PromptState, user_input: str) -> PromptState:
    new_prompt = normalize_text(user_input)
    next_state: PromptState = deepcopy(state)

    next_state["current_prompt"] = new_prompt
    next_state["domain"] = detect_domain(new_prompt) or state.get("domain")

    detected_elements = detect_prompt_elements(new_prompt)
    for element_name, value in detected_elements.items():
        if element_name in next_state["prompt_elements"]:
            next_state["prompt_elements"][element_name]["value"] = value
            next_state["prompt_elements"][element_name]["confirmed"] = value is not None

    return next_state
