# Project Architecture

## Overview

이 프로젝트는 사용자가 Prompt를 스스로 개선하도록 돕는 교육용 Prompt Engineering Coach이다.

Prompt를 대신 작성해주는 것이 아니라,

- 현재 Prompt를 분석하고
- 부족한 부분을 질문하며
- 사용자가 직접 수정하도록 코칭한다.

모든 코칭은 PromptState를 기반으로 이루어진다.

---

# Architecture

```text
                 User Prompt
                      │
                      ▼
             Initial Analyzer
                      │
          Extract Prompt Elements
          Detect Domain
                      │
                      ▼
                PromptState
                      │
                      ▼
                   Coach
                      │
          질문 + 분야별 예시 제공
                      │
                      ▼
              User edits Prompt
                      │
                      ▼
            Response Analyzer
      (Diff + PromptState Update)
                      │
                      ▼
                PromptState
                      │
                      ▼
                   Coach
                (반복 코칭)
                      │
                      ▼
                  Reviewer
```

---

# Components

## 1. Initial Analyzer

### 역할

사용자가 입력한 Prompt를 최초 분석한다.

### 입력

- User Prompt

### 출력

- PromptState 생성

### 수행 작업

- Prompt 요소 추출
- Domain 추출
- PromptState 초기화

예)

```text
Prompt

↓

Goal
Role
Context
Output Format
...

↓

PromptState 생성
```

---

## 2. PromptState

Prompt의 현재 상태를 저장한다.

관리하는 정보

- original_prompt
- current_prompt
- domain
- prompt_elements

PromptState는 프로젝트 전체에서 단 하나의 Source of Truth이다.

---

## 3. Coach

### 역할

PromptState를 기반으로

- 무엇이 부족한지 판단하고
- 사용자에게 질문하며
- 개선 방향을 안내한다.

### 입력

PromptState

### 출력

- 질문
- 설명
- 분야별 예시

예)

```text
질문

목표를 조금 더 구체적으로 작성해 주세요.

예시

3개월 안에 백엔드 개발자로 취업하기 위해
기술 면접을 준비하고 싶어요.
```

Coach는 Prompt를 대신 작성하지 않는다.

---

## 4. User

Coach의 질문을 참고하여 Prompt를 직접 수정한다.

---

## 5. Response Analyzer

### 역할

수정 전 Prompt와 수정 후 Prompt를 비교하여

PromptState를 업데이트한다.

### 입력

- state.current_prompt
- user_input

### 처리 과정

```text
old_prompt

↓

new_prompt

↓

Diff

↓

LLM 분석

↓

PromptState Update
```

### 수행 작업

- Diff 분석
- Prompt 요소 업데이트
- current_prompt 갱신

---

## 6. Reviewer

모든 코칭이 끝난 후

최초 Prompt와 최종 Prompt를 비교하여

- 얼마나 개선되었는지
- 어떤 부분이 좋아졌는지
- 앞으로 어떤 부분을 더 개선하면 좋은지

학습 피드백을 제공한다.

입력

- original_prompt
- current_prompt

---

# Prompt Editing Flow

```text
Initial Prompt

↓

PromptState 생성

↓

Coach

↓

사용자 수정

↓

Response Analyzer

↓

PromptState Update

↓

Coach

↓

사용자 수정

↓

...

↓

Reviewer
```

---

# PromptState Update Flow

```text
state.current_prompt
        │
        ▼
old_prompt

+

user_input
(new_prompt)

↓

Diff

↓

Prompt 요소 재분석

↓

PromptState Update

↓

state.current_prompt = new_prompt
```

---

# Domain-based Coaching

Initial Analyzer는 Prompt의 분야를 추출한다.

예)

- 학습
- 취업
- 글쓰기
- 분석
- 기획
- 번역

Coach는 Domain을 활용하여

- 질문
- 예시

를 사용자 상황에 맞게 생성한다.

예)

취업

> 목표를 조금 더 구체적으로 작성해 주세요.

예시

> "3개월 안에 백엔드 개발자로 취업하기 위해 기술 면접을 준비하고 싶어요."

---

# Design Principles

- Prompt는 사용자가 직접 수정한다.
- Coach는 질문과 피드백만 제공한다.
- PromptState는 현재 Prompt의 단일 진실(Source of Truth)이다.
- original_prompt는 변경하지 않는다.
- current_prompt만 계속 갱신한다.
- Response Analyzer는 Diff 기반으로 PromptState를 업데이트한다.
- Reviewer는 최초 Prompt와 최종 Prompt를 비교하여 학습 피드백을 제공한다.