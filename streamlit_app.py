from __future__ import annotations

from uuid import uuid4

import streamlit as st

from models.initial_state import create_initial_state
from nodes.analyzer import analyze_prompt
from nodes.coach import create_coaching_message
from nodes.reviewer import review_prompt_progress
from utils.log_context import logging_context


def create_session_id() -> str:
    return f"session_{uuid4().hex[:12]}"


def main() -> None:
    st.set_page_config(
        page_title="Help Prompt Agent",
        page_icon="🧭",
        layout="wide",
    )

    # 상태 State 초기화
    ensure_session_state()

    st.title("Help Prompt Agent")
    st.caption("프롬프트를 대신 완성하지 않고, 질문으로 의도를 정돈합니다.")

    state = st.session_state["state"]

    if state["original_prompt"] is None:
        render_initial_input()
        return

    render_workspace()


def ensure_session_state() -> None:
    if "state" not in st.session_state:
        st.session_state["state"] = create_initial_state()

    if "session_id" not in st.session_state:
        st.session_state["session_id"] = create_session_id()

    if "turn_index" not in st.session_state:
        st.session_state["turn_index"] = 0

    if "coach_message" not in st.session_state:
        st.session_state["coach_message"] = None

    if "review_message" not in st.session_state:
        st.session_state["review_message"] = None


def render_initial_input() -> None:
    st.subheader("처음 프롬프트")
    user_prompt = st.text_area(
        "AI와 하고 싶은 일을 대충 적어도 됩니다.",
        height=180,
        placeholder="예: 코딩 테스트 공부 도와줘",
    )

    if st.button("분석 시작", type="primary"):
        prompt = user_prompt.strip()
        if not prompt:
            st.warning("프롬프트를 입력해 주세요.")
            return

        with st.spinner("프롬프트를 분석하는 중입니다..."):
            st.session_state["turn_index"] = 1
            with logging_context(
                session_id=st.session_state["session_id"],
                turn_index=st.session_state["turn_index"],
            ):
                state = analyze_prompt(st.session_state["state"], prompt)
                st.session_state["state"] = state
                st.session_state["coach_message"] = create_coaching_message(state)
            st.session_state["review_message"] = None
            st.rerun()


def render_workspace() -> None:
    state = st.session_state["state"]

    left, right = st.columns([3, 2], gap="large")

    with left:
        st.subheader("현재 프롬프트")
        edited_prompt = st.text_area(
            "Coach 질문을 참고해서 필요한 부분만 고쳐 주세요.",
            value=state["current_prompt"] or "",
            height=260,
            key="current_prompt_editor",
        )

        col_analyze, col_review, col_reset = st.columns([1, 1, 1])

        with col_analyze:
            if st.button("다시 분석", type="primary"):
                prompt = edited_prompt.strip()
                if not prompt:
                    st.warning("프롬프트가 비어 있습니다.")
                    return

                with st.spinner("수정된 프롬프트를 분석하는 중입니다..."):
                    st.session_state["turn_index"] += 1
                    with logging_context(
                        session_id=st.session_state["session_id"],
                        turn_index=st.session_state["turn_index"],
                    ):
                        next_state = analyze_prompt(state, prompt)
                        st.session_state["state"] = next_state
                        st.session_state["coach_message"] = create_coaching_message(
                            next_state
                        )
                    st.session_state["review_message"] = None
                    st.rerun()

        with col_review:
            if st.button("현재 상태 리뷰"):
                st.session_state["review_message"] = review_prompt_progress(state)

        with col_reset:
            if st.button("처음부터"):
                st.session_state["state"] = create_initial_state()
                st.session_state["session_id"] = create_session_id()
                st.session_state["turn_index"] = 0
                st.session_state["coach_message"] = None
                st.session_state["review_message"] = None
                st.rerun()

    with right:
        st.subheader("Coach")
        coach_message = st.session_state.get("coach_message")
        if coach_message:
            st.markdown(coach_message)
        else:
            st.info("아직 코칭 메시지가 없습니다.")

        review_message = st.session_state.get("review_message")
        if review_message:
            st.divider()
            st.subheader("Review")
            st.markdown(review_message)

    with st.expander("PromptState 보기"):
        st.json(state)


if __name__ == "__main__":
    main()
