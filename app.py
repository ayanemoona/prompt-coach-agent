from models.initial_state import create_initial_state
from nodes.analyzer import analyze_prompt
from nodes.coach import create_coaching_message
from nodes.reviewer import review_prompt_progress

EXIT_COMMANDS = {"exit", "quit", "q", "종료"}
REVIEW_COMMANDS = {"review", "리뷰", "done", "완료"}


def main() -> None:
    print("Help Prompt Agent")
    print("프롬프트를 입력하면 부족한 요소를 하나씩 질문합니다.")
    print("종료: exit / 리뷰: review")
    print()

    user_prompt = input("처음 프롬프트를 입력하세요: ").strip()
    if not user_prompt:
        print("프롬프트가 비어 있어 종료합니다.")
        return

    state = create_initial_state()
    state = analyze_prompt(state, user_prompt)

    while True:
        print()
        print(create_coaching_message(state))
        print()

        user_input = input("수정한 프롬프트 전체 입력: ").strip()
        normalized = user_input.lower()

        if normalized in EXIT_COMMANDS:
            print("종료합니다.")
            return

        if normalized in REVIEW_COMMANDS:
            print()
            print(review_prompt_progress(state))
            return

        if not user_input:
            print("빈 입력은 반영하지 않습니다.")
            continue

        state = analyze_prompt(state, user_input)


if __name__ == "__main__":
    main()
