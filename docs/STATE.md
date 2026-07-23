# PromptState

PromptState는 현재 Prompt의 상태와 분석 결과를 저장하는 객체이다.

- 현재 Prompt
- Prompt 요소 분석 결과
- 도메인 정보

을 관리하며, 사용자가 Prompt를 수정할 때마다 갱신된다.

---

## PromptState

```python
from typing import TypedDict


class PromptElement(TypedDict):
    value: str | None
    confirmed: bool


class PromptState(TypedDict):
    # 최초 입력 Prompt (Reviewer에서 사용)
    original_prompt: str

    # 현재 Prompt
    current_prompt: str

    # Prompt 분야
    # 예) 학습, 취업, 글쓰기, 분석 ...
    domain: str | None

    # Prompt 요소
    prompt_elements: dict[str, PromptElement]
```

---

# 필드 설명

## original_prompt

사용자가 최초 입력한 Prompt이다.

수정되지 않는다.

Reviewer에서

- 최초 Prompt
- 최종 Prompt

를 비교하기 위해 사용한다.

---

## current_prompt

현재 사용자가 수정한 최신 Prompt이다.

Response Analyzer가 Diff를 수행할 때 사용된다.

```text
old_prompt = state.current_prompt
new_prompt = user_input

↓

Diff

↓

state.current_prompt = new_prompt
```

---

## domain

Initial Analyzer가 추출한 Prompt의 분야이다.

예시

- 학습
- 글쓰기
- 취업
- 분석
- 기획
- 번역

Coach는 domain을 참고하여

- 질문 방식
- 예시

를 사용자 상황에 맞게 제공한다.

예)

취업 분야

질문
> 목표를 조금 더 구체적으로 작성해 주세요.

예시
> "3개월 안에 백엔드 개발자로 취업하기 위해 기술 면접을 준비하고 싶어요."

---

## prompt_elements

Prompt를 구조화한 정보이다.

예)

```python
{
    "goal": {
        "value": "취업",
        "confirmed": False
    },
    "context": {
        "value": None,
        "confirmed": False
    }
}
```

---

# PromptState 변경 흐름

```text
사용자 입력

↓

Initial Analyzer

↓

PromptState 생성

↓

Coach

↓

사용자 수정

↓

Response Analyzer

old_prompt = state.current_prompt
new_prompt = user_input

↓

Diff 분석

↓

PromptState 갱신

↓

Coach

...

↓

Reviewer

original_prompt
↓

current_prompt

비교
```

---

# 설계 원칙

- original_prompt는 최초 입력 이후 변경하지 않는다.
- current_prompt만 계속 갱신한다.
- Response Analyzer는 old/new Prompt를 비교하여 Diff를 분석한다.
- domain은 Coach가 사용자에게 적절한 질문과 예시를 생성하는 데 사용한다.
- prompt_elements는 Prompt의 현재 상태를 나타내며 계속 업데이트된다.