from __future__ import annotations

import json

from models.state import PromptState
from prompts.coach_prompt import COACH_PROMPT
from utils.knowledge_loader import load_knowledge
from utils.llm import ask_llm, is_llm_configured
from utils.log_context import logging_context

FOCUS_PRIORITY = (
    "goal",
    "context",
    "output",
    "role",
    "constraints",
    "examples",
    "reasoning",
    "evaluation",
)


def create_coaching_message(state: PromptState) -> str:
    if not is_llm_configured():
        raise RuntimeError("OPENAI_API_KEY is not configured. Coach requires LLM.")

    focus = select_focus_element(state)
    if focus is None:
        return (
            "기본 프롬프트 요소가 모두 채워져 있습니다.\n"
            "`review`를 입력해 현재 프롬프트를 점검하거나, "
            "더 다듬고 싶은 부분을 직접 수정해 주세요."
        )

    knowledge = load_knowledge(focus)
    prompt, state_chars = build_coach_prompt(state, focus, knowledge)
    with logging_context(
        focus_element=focus,
        input_chars=len(state.get("current_prompt") or ""),
        state_chars=state_chars,
    ):
        return ask_llm(prompt, node="coach")


def select_focus_element(state: PromptState) -> str | None:
    for element_name in FOCUS_PRIORITY:
        element = state["prompt_elements"][element_name]
        if element["value"] is None:
            return element_name

    return None


def build_coach_prompt(
    state: PromptState, focus: str, knowledge: str
) -> tuple[str, int]:
    state_json = json.dumps(state, ensure_ascii=False, indent=2)
    return (
        COACH_PROMPT.format(
            focus=focus,
            knowledge=knowledge,
            state=state_json,
        ),
        len(state_json),
    )
