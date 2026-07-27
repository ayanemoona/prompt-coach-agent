from .state import PromptState


def create_initial_state() -> PromptState:
    return {
        "original_prompt": None,
        "current_prompt": None,
        "domain": None,
        "prompt_elements": {
            "role": {"value": None, "existed_initially": False},
            "context": {"value": None, "existed_initially": False},
            "goal": {"value": None, "existed_initially": False},
            "constraints": {"value": None, "existed_initially": False},
            "output": {"value": None, "existed_initially": False},
            "examples": {"value": None, "existed_initially": False},
            "reasoning": {"value": None, "existed_initially": False},
            "evaluation": {"value": None, "existed_initially": False},
        },
    }
