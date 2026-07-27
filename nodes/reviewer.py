from __future__ import annotations

from models.state import PromptState


def review_prompt_progress(state: PromptState) -> str:
    original_prompt = state.get("original_prompt") or ""
    current_prompt = state.get("current_prompt") or ""

    present_elements = [
        name
        for name, element in state["prompt_elements"].items()
        if element["value"] is not None
    ]
    added_elements = [
        name
        for name, element in state["prompt_elements"].items()
        if element["value"] is not None and not element["existed_initially"]
    ]
    missing = [
        name
        for name, element in state["prompt_elements"].items()
        if element["value"] is None
    ]

    return (
        "[프롬프트 리뷰]\n"
        f"- 감지된 분야: {state.get('domain') or '일반'}\n"
        f"- 현재 채워진 요소: {len(present_elements)}/8 "
        f"({', '.join(present_elements) if present_elements else '없음'})\n"
        f"- 코칭 중 추가된 요소: {', '.join(added_elements) if added_elements else '없음'}\n"
        f"- 아직 부족한 요소: {', '.join(missing) if missing else '없음'}\n"
        f"- 길이 변화: {len(original_prompt)}자 -> {len(current_prompt)}자\n\n"
        "좋아진 점:\n"
        "- 프롬프트를 요소 단위로 점검할 수 있는 상태가 되었습니다.\n\n"
        "다음 개선 방향:\n"
        "- 가장 중요한 목표, 맥락, 출력 형식을 먼저 선명하게 만든 뒤 세부 제약을 추가하세요."
    )
