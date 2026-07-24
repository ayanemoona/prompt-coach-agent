
from models.state import PromptState


def update_initial_state(state: PromptState, analysis: dict) -> None:
    update_domain(state, analysis)

    prompt_elements = analysis.get("prompt_elements", {})
    for element_name, element_value in prompt_elements.items():
        if element_name not in state["prompt_elements"]:
            continue

        state["prompt_elements"][element_name]["value"] = element_value.get("value")
        state["prompt_elements"][element_name]["existed_initially"] = bool(
            element_value.get("existed_initially")
        )


def update_current_state(state: PromptState, analysis: dict) -> None:
    update_domain(state, analysis)

    prompt_elements = analysis.get("prompt_elements", {})
    for element_name, element_value in prompt_elements.items():
        if element_name not in state["prompt_elements"]:
            continue

        state["prompt_elements"][element_name]["value"] = element_value.get("value")


def update_domain(state: PromptState, analysis: dict) -> None:
    domain = analysis.get("domain")
    if isinstance(domain, str) and domain.strip():
        state["domain"] = domain.strip()
