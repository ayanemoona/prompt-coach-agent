
from models.state import PromptState


def update_state(state: PromptState, analysis: dict) -> None:
    state["domain"] = analysis.get("domain")

    prompt_elements = analysis.get("prompt_elements", {})
    for element_name, element_value in prompt_elements.items():
        if element_name not in state["prompt_elements"]:
            continue

        state["prompt_elements"][element_name]["value"] = element_value.get("value")
        state["prompt_elements"][element_name]["confirmed"] = bool(
            element_value.get("confirmed")
        )
