from typing import TypedDict


class PromptElement(TypedDict):
    value: str | None
    existed_initially: bool


class PromptState(TypedDict):

    # 사용자가 처음 입력한 원본
    original_prompt: str | None

    # 화면에서 계속 수정되는 Prompt
    current_prompt: str | None

    domain: str | None

    # 8개 요소
    prompt_elements: dict[str, PromptElement]
