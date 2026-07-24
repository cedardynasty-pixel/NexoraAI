import streamlit as st
from style import inject_css, hero, section_title
from auth import is_logged_in, require_login_notice, current_user
import db
import gemini_client as gc

inject_css()

if not is_logged_in():
    require_login_notice()
    st.stop()

hero("AI Study Tools", "Generate notes, worksheets, study plans and flashcards, powered by Gemini.")

api_key = db.get_setting("gemini_api_key") or st.secrets.get("GEMINI_API_KEY", "")

if not api_key:
    st.warning(
        "The AI Study Tools aren't set up yet. Ask an admin to add a Gemini API key "
        "in the Admin panel's Settings tab."
    )
    st.stop()

user = db.get_user(current_user())
grade = user["grade"] or "Grade 9"

tab_notes, tab_worksheet, tab_plan, tab_flashcards = st.tabs(
    ["📝 Notes", "📋 Worksheet", "🗓️ Study Plan", "🃏 Flashcards"]
)

# ---------------- NOTES ----------------
with tab_notes:
    section_title("Generate Study Notes")
    topic = st.text_input("Topic", key="notes_topic", placeholder="e.g. Photosynthesis")
    if st.button("Generate Notes", key="gen_notes"):
        if not topic.strip():
            st.error("Please enter a topic.")
        else:
            with st.spinner("Generating notes..."):
                try:
                    notes = gc.generate_notes(topic.strip(), grade, api_key)
                    st.markdown(notes)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

# ---------------- WORKSHEET ----------------
with tab_worksheet:
    section_title("Generate a Practice Worksheet")
    w_topic = st.text_input("Topic", key="worksheet_topic", placeholder="e.g. Linear Equations")
    num_q = st.slider("Number of questions", 3, 20, 10)
    if st.button("Generate Worksheet", key="gen_worksheet"):
        if not w_topic.strip():
            st.error("Please enter a topic.")
        else:
            with st.spinner("Generating worksheet..."):
                try:
                    worksheet = gc.generate_worksheet(w_topic.strip(), grade, num_q, api_key)
                    st.markdown(worksheet)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

# ---------------- STUDY PLAN ----------------
with tab_plan:
    section_title("Generate a Study Plan")
    subject = st.text_input("Subject", key="plan_subject", placeholder="e.g. Science")
    duration = st.selectbox("Duration", ["1 week", "2 weeks", "1 month", "3 months"])
    goal = st.text_area("Goal", key="plan_goal", placeholder="e.g. Prepare for the mid-term exam")
    if st.button("Generate Study Plan", key="gen_plan"):
        if not subject.strip() or not goal.strip():
            st.error("Please fill in the subject and goal.")
        else:
            with st.spinner("Building your study plan..."):
                try:
                    plan = gc.generate_study_plan(subject.strip(), grade, duration, goal.strip(), api_key)
                    st.markdown(plan)
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

# ---------------- FLASHCARDS ----------------
with tab_flashcards:
    section_title("Generate Flashcards")
    f_topic = st.text_input("Topic", key="flashcards_topic", placeholder="e.g. World War II")
    count = st.slider("Number of flashcards", 3, 20, 8, key="flashcards_count")
    if st.button("Generate Flashcards", key="gen_flashcards"):
        if not f_topic.strip():
            st.error("Please enter a topic.")
        else:
            with st.spinner("Generating flashcards..."):
                try:
                    cards = gc.generate_flashcards(f_topic.strip(), grade, count, api_key)
                    st.session_state["flashcards"] = cards
                    st.session_state["flashcard_index"] = 0
                except Exception as e:
                    st.error(f"Something went wrong: {e}")

    if st.session_state.get("flashcards"):
        cards = st.session_state["flashcards"]
        idx = st.session_state.get("flashcard_index", 0)
        idx = max(0, min(idx, len(cards) - 1))
        card = cards[idx]

        st.markdown(f"**Card {idx + 1} of {len(cards)}**")
        st.markdown(
            f"""<div class="nexora-card"><h3>Q: {card.get('question', '')}</h3></div>""",
            unsafe_allow_html=True,
        )
        if st.toggle("Show answer", key=f"show_answer_{idx}"):
            st.info(card.get("answer", ""))

        nav_cols = st.columns(2)
        with nav_cols[0]:
            if st.button("⬅️ Previous", disabled=idx == 0):
                st.session_state["flashcard_index"] = idx - 1
                st.rerun()
        with nav_cols[1]:
            if st.button("Next ➡️", disabled=idx == len(cards) - 1):
                st.session_state["flashcard_index"] = idx + 1
                st.rerun()
