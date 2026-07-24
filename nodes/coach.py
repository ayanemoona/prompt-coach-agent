from __future__ import annotations

from models.state import PromptState


ELEMENT_LABELS = {
    "role": "역할",
    "context": "맥락",
    "goal": "목표",
    "constraints": "제약 조건",
    "output": "출력 형식",
    "examples": "예시",
    "reasoning": "사고 과정",
    "evaluation": "평가 기준",
}

ELEMENT_PRIORITY = (
    "goal",
    "context",
    "output",
    "role",
    "constraints",
    "examples",
    "reasoning",
    "evaluation",
)

QUESTIONS = {
    "goal": "이 프롬프트로 최종적으로 얻고 싶은 결과를 한 문장으로 더 구체화해 주세요.",
    "context": "이 요청을 처리할 때 알아야 할 대상, 배경, 현재 수준을 추가해 주세요.",
    "output": "답변이 어떤 형태로 나오면 좋은지 정해 주세요. 예: 표, 단계별 목록, 코드 블록, 보고서 형식",
    "role": "AI가 어떤 역할로 답해야 하는지 정해 주세요. 예: 코딩 테스트 교육 전문가, 채용 면접관, 글쓰기 코치",
    "constraints": "반드시 지켜야 할 조건이나 피해야 할 방식을 추가해 주세요.",
    "examples": "원하는 답변 스타일이나 참고할 예시가 있다면 하나 추가해 주세요.",
    "reasoning": "답변에 이유, 판단 과정, 단계별 풀이가 필요한지 정해 주세요.",
    "evaluation": "좋은 답변인지 판단할 기준을 추가해 주세요.",
}


def is_vague_value(value: str | None) -> bool:
    if not value:
        return True

    compact = value.strip()
    return len(compact) < 20 or len(compact.split()) < 4


def create_coaching_message(state: PromptState) -> str:
    target = select_next_element(state)
    if target is None:
        return (
            "현재 프롬프트는 기본 요소가 꽤 잘 채워져 있습니다.\n"
            "이제 더 구체적인 상황이나 금지 조건을 추가하면 품질을 더 올릴 수 있어요.\n"
            "리뷰를 원하면 `review`를 입력하세요."
        )

    element = state["prompt_elements"][target]
    label = ELEMENT_LABELS[target]
    domain = state.get("domain") or "일반"

    if element["value"] is None:
        status = "아직 비어 있습니다"
    elif is_vague_value(element["value"]):
        status = "있지만 아직 짧거나 모호합니다"
    else:
        status = "더 확인이 필요합니다"

    return (
        f"[{domain} 프롬프트 코칭]\n"
        f"- 다음으로 볼 요소: {label}\n"
        f"- 현재 상태: {status}\n\n"
        f"질문: {QUESTIONS[target]}\n\n"
        "수정한 프롬프트 전체를 다시 입력해 주세요. "
        "끝내려면 `review`를 입력하면 됩니다."
    )


def select_next_element(state: PromptState) -> str | None:
    for element_name in ELEMENT_PRIORITY:
        element = state["prompt_elements"][element_name]
        if element["value"] is None:
            return element_name
        if element_name in {"goal", "context", "output"} and is_vague_value(element["value"]):
            return element_name

    return None
