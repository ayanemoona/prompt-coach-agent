from __future__ import annotations

from collections.abc import Iterable


DOMAIN_KEYWORDS: dict[str, tuple[str, ...]] = {
    "학습": ("공부", "학습", "배우", "강의", "설명", "문제", "풀이", "교육"),
    "취업": ("취업", "면접", "자소서", "이력서", "포트폴리오", "채용", "커리어"),
    "글쓰기": ("글", "작성", "문장", "카피", "블로그", "에세이", "보고서"),
    "분석": ("분석", "비교", "원인", "인사이트", "데이터", "요약"),
    "기획": ("기획", "전략", "로드맵", "PRD", "요구사항", "아이디어"),
    "번역": ("번역", "영어", "한국어", "일본어", "중국어", "translate"),
    "코딩": ("코드", "구현", "파이썬", "python", "자바", "javascript", "알고리즘"),
}


ELEMENT_KEYWORDS: dict[str, tuple[str, ...]] = {
    "role": ("당신은", "전문가", "역할", "coach", "teacher", "개발자", "기획자"),
    "context": ("대상", "수준", "배경", "상황", "현재", "위한", "입문", "초보", "취준생"),
    "goal": ("하고 싶", "해줘", "작성", "만들", "알려", "설명", "목표", "원해", "도와"),
    "constraints": ("반드시", "하지 마", "금지", "조건", "제약", "이내", "이상", "포함"),
    "output": ("형식", "표", "목록", "코드", "json", "markdown", "블록", "섹션"),
    "examples": ("예시", "샘플", "입출력", "case", "example"),
    "reasoning": ("왜", "이유", "단계", "과정", "근거", "추론", "풀이"),
    "evaluation": ("평가", "기준", "체크", "검토", "리뷰", "rubric", "피드백"),
}


def normalize_text(text: str | None) -> str:
    return (text or "").strip()


def contains_any(text: str, keywords: Iterable[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def detect_domain(prompt: str) -> str | None:
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if contains_any(prompt, keywords):
            return domain
    return None


def detect_prompt_elements(prompt: str) -> dict[str, str | None]:
    clean_prompt = normalize_text(prompt)
    detected: dict[str, str | None] = {}

    for element, keywords in ELEMENT_KEYWORDS.items():
        detected[element] = clean_prompt if contains_any(clean_prompt, keywords) else None

    if clean_prompt and detected.get("goal") is None:
        detected["goal"] = clean_prompt

    return detected


def is_vague_value(value: str | None) -> bool:
    if not value:
        return True

    compact = value.strip()
    return len(compact) < 20 or len(compact.split()) < 4
