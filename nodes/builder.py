from __future__ import annotations

from models.state import PromptState


def render_current_prompt(state: PromptState) -> str:
    return state.get("current_prompt") or ""
