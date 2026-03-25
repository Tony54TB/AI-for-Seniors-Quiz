import json
import random
import streamlit as st

# ====================== SENIOR-FRIENDLY STYLING ======================
st.markdown("""
<style>
/* Answer buttons */
.stButton > button {
    font-size: 26px !important;
    padding: 18px 20px !important;
    margin: 12px 0 !important;
    width: 100% !important;
    background-color: #e3f2fd !important;
    border: 2px solid #90caf9 !important;
    border-radius: 12px !important;
    color: #1e3a8a !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Next Question button */
button:has-text("→ Next Question") {
    background-color: #bfdbfe !important;
    border: 2px solid #3b82f6 !important;
    color: #1e40af !important;
    font-size: 20px !important;
    padding: 12px 24px !important;
    width: 280px !important;
    margin: 15px auto 10px auto !important;
    display: block !important;
    border-radius: 10px !important;
}

/* Question and subheader text */
.stMarkdown h3, .stMarkdown p {
    font-size: 24px !important;
    line-height: 1.7 !important;
}

/* Robot title */
.robot-title {
    font-size: 46px !important;
    text-align: center !important;
    margin-bottom: 10px !important;
}

/* Intro text */
.intro-text {
    font-size: 26px !important;
    font-weight: 600 !important;
    color: #2c3e50 !important;
    margin: 15px 0 25px 0 !important;
    text-align: center !important;
}

/* Small footer */
.footer {
    font-size: 14px !important;
    color: #6b7280 !important;
    text-align: center !important;
    margin-top: 40px !important;
    padding-top: 20px !important;
    border-top: 1px solid #e5e7eb !important;
}
</style>
""", unsafe_allow_html=True)

# Load questions
with open("data/questions.json", "r", encoding="utf-8") as f:
    ALL_QUESTIONS = json.load(f)

st.set_page_config(page_title="AI Quiz for Seniors", layout="centered")

# Session state
if "score" not in st.session_state:
    st.session_state.score = 0
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "shuffled" not in st.session_state:
    st.session_state.shuffled = random.sample(ALL_QUESTIONS, len(ALL_QUESTIONS))

# ====================== MAIN UI ======================
st.markdown('<h1 class="robot-title">🤖 AI For Seniors Quiz</h1>', unsafe_allow_html=True)

st.markdown('<p class="intro-text">Test your AI Knowledge</p>', unsafe_allow_html=True)

# Progress bar
progress = st.session_state.question_index / len(st.session_state.shuffled)
st.progress(progress, text=f"Question {st.session_state.question_index + 1} of {len(st.session_state.shuffled)}")

q = st.session_state.shuffled[st.session_state.question_index]

st.subheader(f"Question {st.session_state.question_index + 1}")
st.write(q["question"]) 

# Flag for feedback
if "answered" not in st.session_state:
    st.session_state.answered = False

# Render answer buttons
for opt in q["options"]:
    if st.button(opt, key=f"{st.session_state.question_index}_{opt}", help="Click to choose this answer"):
        st.session_state.answered = True
        st.session_state.selected = opt

        if opt == q["answer"]:
            st.success("✅ Correct! 🎉 Well done!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Not quite. The correct answer is **{q['answer']}**")
            st.info(q.get("explanation", "AI is helpful tech that learns patterns — it doesn't have real feelings or understanding like people do."))

# Show Next Question button
if st.session_state.answered:
    if st.button("→ Next Question", key=f"next_{st.session_state.question_index}"):
        st.session_state.answered = False
        if st.session_state.question_index + 1 < len(st.session_state.shuffled):
            st.session_state.question_index += 1
            st.rerun()
        else:
            # Final screen
            st.balloons()
            st.success("🎉 Well done! You've completed the AI Quiz!")

            final_score = min(st.session_state.score, len(st.session_state.shuffled))
            st.markdown(f"""
            <h2 style="text-align: center; color: #27ae60;">
                Your score: {final_score} out of {len(st.session_state.shuffled)}
            </h2>
            """, unsafe_allow_html=True)

            if final_score == len(st.session_state.shuffled):
                st.markdown("**Perfect! You're officially AI-savvy!** 🌟", unsafe_allow_html=True)
            elif final_score >= 7:
                st.markdown("**Excellent work!** You're really getting the hang of this.", unsafe_allow_html=True)
            else:
                st.markdown("**Great effort!** Every question helps you learn more about AI.", unsafe_allow_html=True)

            if st.button("Play again", key="play_again_final"):
                st.session_state.score = 0
                st.session_state.question_index = 0
                st.session_state.answered = False
                st.session_state.selected = None
                st.session_state.shuffled = random.sample(ALL_QUESTIONS, len(ALL_QUESTIONS))
                st.rerun()

# Footer
st.markdown('<p class="footer">Made by Tony at ToneBone Media for Senior Citizen familiarity with AI</p>', unsafe_allow_html=True)