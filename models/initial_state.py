from .state import PromptState


def create_initial_state() -> PromptState:
    return {
        "original_prompt": None,
        "current_prompt": None,
        "domain": None,

        "prompt_elements": {

            "role": {
                "value": None,
                "confirmed": False
            },

            "context": {
                "value": None,
                "confirmed": False
            },

            "goal": {
                "value": None,
                "confirmed": False
            },

            "constraints": {
                "value": None,
                "confirmed": False
            },

            "output": {
                "value": None,
                "confirmed": False
            },

            "examples": {
                "value": None,
                "confirmed": False
            },

            "reasoning": {
                "value": None,
                "confirmed": False
            },

            "evaluation": {
                "value": None,
                "confirmed": False
            }
        }
    }