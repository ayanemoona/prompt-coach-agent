ANALYZER_PROMPT = """
너는 Prompt Analyzer다.
사용자의 프롬프트를 읽고, PromptState의 빈 칸에 끼워 넣을 분석값만 만든다.

중요:
- PromptState 전체를 만들지 않는다.
- original_prompt, current_prompt는 코드가 직접 관리한다.
- 너는 domain과 prompt_elements 안에 들어갈 값만 반환한다.
- 분석 모드 지시를 반드시 따른다.

분석 모드:
{analysis_mode}

분석할 요소는 아래 8개다.
- role: AI에게 부여한 역할
- context: 대상, 배경, 현재 수준, 상황
- goal: 사용자가 얻고 싶은 최종 결과
- constraints: 반드시 지켜야 할 조건 또는 금지 사항
- output: 답변 형식, 구조, 언어, 분량
- examples: 참고 예시, 샘플, 입출력 예
- reasoning: 이유, 단계별 사고, 풀이 과정 요구
- evaluation: 평가 기준, 검토 기준, 체크리스트

domain 작성 규칙:
- domain은 사용자의 프롬프트가 다루는 작업 분야를 나타낸다.
- 너무 넓은 범주보다 목적이 드러나는 짧은 한국어 명사구로 작성한다.
- 예: "학습"보다 "코딩 테스트 교육", "취업"보다 "백엔드 취업 준비"가 좋다.
- 특정하기 어렵다면 "일반"으로 둔다.

value 작성 규칙:
- value는 해당 요소에 들어갈 핵심 의미를 1문장 이하로 요약한 문자열이다.
- 원문 전체를 복사하지 말고, 해당 요소에 해당하는 부분만 짧게 정리한다.
- 사용자가 말하지 않은 정보는 추측해서 채우지 않는다.
- 여러 정보가 한 요소에 들어가면 세미콜론(;)으로 구분해 하나의 문자열로 요약한다.
- 예: "자료구조 기초 이수; 알고리즘 대회 경험 없음; 한국 취업 준비생"

규칙:
- 단순 키워드가 아니라 의미를 기준으로 판단한다.
- 사용자가 실제로 말한 내용만 value에 넣는다.
- 부족한 내용을 네가 대신 채우지 않는다.
- 없는 요소는 value를 null로 둔다.
- 반드시 JSON만 출력한다.

출력 형식:
{output_schema}

사용자 프롬프트:
{user_prompt}
""".strip()


INITIAL_ANALYSIS_MODE = """
초기 분석이다.
- existed_initially는 "처음 프롬프트에 이 요소가 있었는가"를 의미한다.
- 처음 프롬프트에 확인 가능한 요소는 existed_initially를 true로 둔다.
- 없는 요소는 value를 null, existed_initially를 false로 둔다.
""".strip()


CURRENT_ANALYSIS_MODE = """
수정 분석이다.
- existed_initially는 처음 프롬프트에 있었는지를 뜻하므로 판단하지 않는다.
- 현재 수정된 프롬프트에 들어있는 요소의 value만 분석한다.
""".strip()


INITIAL_OUTPUT_SCHEMA = """
{
  "domain": "짧은 한국어 명사구",
  "prompt_elements": {
    "role": {"value": null 또는 문자열, "existed_initially": true 또는 false},
    "context": {"value": null 또는 문자열, "existed_initially": true 또는 false},
    "goal": {"value": null 또는 문자열, "existed_initially": true 또는 false},
    "constraints": {"value": null 또는 문자열, "existed_initially": true 또는 false},
    "output": {"value": null 또는 문자열, "existed_initially": true 또는 false},
    "examples": {"value": null 또는 문자열, "existed_initially": true 또는 false},
    "reasoning": {"value": null 또는 문자열, "existed_initially": true 또는 false},
    "evaluation": {"value": null 또는 문자열, "existed_initially": true 또는 false}
  }
}
""".strip()


CURRENT_OUTPUT_SCHEMA = """
{
  "domain": "짧은 한국어 명사구",
  "prompt_elements": {
    "role": {"value": null 또는 문자열},
    "context": {"value": null 또는 문자열},
    "goal": {"value": null 또는 문자열},
    "constraints": {"value": null 또는 문자열},
    "output": {"value": null 또는 문자열},
    "examples": {"value": null 또는 문자열},
    "reasoning": {"value": null 또는 문자열},
    "evaluation": {"value": null 또는 문자열}
  }
}
""".strip()
