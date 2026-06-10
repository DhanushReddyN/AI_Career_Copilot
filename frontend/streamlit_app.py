import os
import streamlit as st
import requests

# Reads from environment variable (set in Streamlit Cloud secrets or .env)
# Falls back to localhost for local development
FASTAPI_URL = os.environ.get("FASTAPI_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="AI Career Copilot",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Session State Initialization
# -----------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "resume_uploaded" not in st.session_state:
    st.session_state.resume_uploaded = False

if "jd_uploaded" not in st.session_state:
    st.session_state.jd_uploaded = False

if "resume_analysis" not in st.session_state:
    st.session_state.resume_analysis = ""

if "skill_gap" not in st.session_state:
    st.session_state.skill_gap = ""

if "roadmap" not in st.session_state:
    st.session_state.roadmap = ""

if "questions" not in st.session_state:
    st.session_state.questions = ""

if "interview_prep" not in st.session_state:
    st.session_state.interview_prep = ""

# Helper to clear all analysis results whenever a new file is uploaded
def clear_analysis_results():
    st.session_state.resume_analysis = ""
    st.session_state.skill_gap = ""
    st.session_state.roadmap = ""
    st.session_state.questions = ""
    st.session_state.interview_prep = ""
    st.session_state.chat_history = []

def show_api_error(response):
    """Show a user-friendly error message, with special handling for rate limits."""
    try:
        detail = response.json().get("detail", response.text)
    except Exception:
        detail = response.text

    if "rate_limit_exceeded" in detail or "Rate limit" in detail or "tokens per" in detail:
        st.warning(
            "⚠️ **Groq API daily token limit reached.**\n\n"
            "The free Groq plan allows 100,000 tokens/day. All fallback models are also exhausted.\n\n"
            "**Options:**\n"
            "- Wait a few minutes and try again (limit resets daily)\n"
            "- Upgrade at https://console.groq.com/settings/billing"
        )
    elif "All Groq models" in detail:
        st.warning(
            "⚠️ **All AI models are rate-limited right now.**\n\n"
            "Please wait a few minutes and try again."
        )
    else:
        st.error(f"❌ Error: {detail}")

# -----------------------------
# Title
# -----------------------------

st.title("🚀 AI Career Copilot")

st.caption(
    "Intelligent Resume Analyzer & Career Assistant using RAG and AI Agents"
)

st.write(
    """
Upload Resume and Job Description,
then analyze your career readiness.
"""
)

st.subheader("📊 Career Readiness Dashboard")

col1, col2, col3, col4 = st.columns(4)

score = "N/A"
readiness = "Unknown"

try:
    response = requests.get(
        f"{FASTAPI_URL}/match-score"
    )

    result = response.json()

    score = result.get("match_score", "N/A")

    if isinstance(score, (int, float)):

        if score >= 80:
            readiness = "High"

        elif score >= 60:
            readiness = "Medium"

        else:
            readiness = "Low"

except:
    pass

with col1:
    st.metric("Match Score", f"{score}%")

with col2:
    st.metric("AI Features", "5")

with col3:
    st.metric("Readiness", readiness)

with col4:
    st.metric("Documents", "2")

# ==========================
# SIDEBAR
# ==========================
with st.sidebar:

    st.header("📂 Documents")

    resume_file = st.file_uploader(
        "Upload Resume PDF",
        type=["pdf"],
        key="resume_uploader"
    )

    if resume_file is not None:

        if st.button("Upload Resume"):

            with st.spinner("Uploading Resume..."):

                # Seek to start so bytes aren't empty on re-uploads
                resume_file.seek(0)

                files = {
                    "file": (
                        resume_file.name,
                        resume_file.read(),
                        "application/pdf"
                    )
                }

                response = requests.post(
                    f"{FASTAPI_URL}/upload-resume",
                    files=files
                )

                if response.status_code == 200:
                    st.success(response.json()["message"])
                    st.session_state.resume_uploaded = True
                    # ✅ Clear stale analysis results from the previous resume
                    clear_analysis_results()
                else:
                    st.error(f"Upload failed: {response.text}")

    st.divider()

    jd_file = st.file_uploader(
        "Upload JD PDF",
        type=["pdf"],
        key="jd_uploader"
    )

    if jd_file is not None:

        if st.button("Upload JD"):

            with st.spinner("Uploading JD..."):

                # Seek to start so bytes aren't empty on re-uploads
                jd_file.seek(0)

                files = {
                    "file": (
                        jd_file.name,
                        jd_file.read(),
                        "application/pdf"
                    )
                }

                response = requests.post(
                    f"{FASTAPI_URL}/upload-jd",
                    files=files
                )

                if response.status_code == 200:
                    st.success(response.json()["message"])
                    st.session_state.jd_uploaded = True
                    # ✅ Clear stale analysis results from the previous JD
                    clear_analysis_results()
                else:
                    st.error(f"Upload failed: {response.text}")

    # Profile completion progress
    st.divider()
    progress = 0
    if st.session_state.resume_uploaded:
        progress += 50
    if st.session_state.jd_uploaded:
        progress += 50
    st.progress(progress)
    st.caption(f"Profile Completion: {progress}%")

    if st.session_state.resume_uploaded:
        st.success("✅ Resume uploaded")
    if st.session_state.jd_uploaded:
        st.success("✅ JD uploaded")

# -----------------------------
# Action Tabs
# -----------------------------

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📄 Resume Analysis",
        "🎯 Skill Gap",
        "🛣️ Roadmap",
        "❓ Questions",
        "🎤 Interview Prep"
    ]
)

with tab1:

    if not st.session_state.resume_uploaded:
        st.info("📌 Please upload a resume first.")
    elif st.button("Analyze Resume"):

        with st.spinner("Analyzing Resume..."):

            response = requests.get(
                f"{FASTAPI_URL}/analyze-resume"
            )

            if response.status_code == 200:
                result = response.json()
                st.session_state.resume_analysis = result["analysis"]
            else:
                show_api_error(response)

    if st.session_state.resume_analysis:

        st.write(st.session_state.resume_analysis)

        st.download_button(
            "📥 Download Analysis",
            st.session_state.resume_analysis,
            file_name="resume_analysis.txt"
        )

with tab2:

    if not (st.session_state.resume_uploaded and st.session_state.jd_uploaded):
        st.info("📌 Please upload both a resume and a JD first.")
    elif st.button("Find Skill Gap"):

        with st.spinner("Finding Skill Gaps..."):

            response = requests.get(
                f"{FASTAPI_URL}/skill-gap"
            )

            if response.status_code == 200:
                result = response.json()
                st.session_state.skill_gap = result["analysis"]
            else:
                show_api_error(response)

    if st.session_state.skill_gap:

        st.write(st.session_state.skill_gap)

        st.download_button(
            "📥 Download Skill Gap Report",
            st.session_state.skill_gap,
            file_name="skill_gap_report.txt"
        )

with tab3:

    if not (st.session_state.resume_uploaded and st.session_state.jd_uploaded):
        st.info("📌 Please upload both a resume and a JD first.")
    elif st.button("Generate Roadmap"):

        with st.spinner("Generating Roadmap..."):

            response = requests.get(
                f"{FASTAPI_URL}/learning-roadmap"
            )

            if response.status_code == 200:
                result = response.json()
                st.session_state.roadmap = result["roadmap"]
            else:
                show_api_error(response)

    if st.session_state.roadmap:

        st.write(st.session_state.roadmap)

        st.download_button(
            "📥 Download Learning Roadmap",
            st.session_state.roadmap,
            file_name="learning_roadmap.txt"
        )

with tab4:

    if not st.session_state.resume_uploaded:
        st.info("📌 Please upload a resume first.")
    elif st.button("Generate Questions"):

        with st.spinner("Generating Questions..."):

            response = requests.get(
                f"{FASTAPI_URL}/interview-questions"
            )

            if response.status_code == 200:
                result = response.json()
                st.session_state.questions = result["questions"]
            else:
                show_api_error(response)

    if st.session_state.questions:

        st.write(st.session_state.questions)

        st.download_button(
            "📥 Download Interview Questions",
            st.session_state.questions,
            file_name="interview_questions.txt"
        )

with tab5:

    if not st.session_state.resume_uploaded:
        st.info("📌 Please upload a resume first.")
    elif st.button("Generate Interview Prep"):

        with st.spinner("Preparing Interview Kit..."):

            response = requests.get(
                f"{FASTAPI_URL}/interview-prep"
            )

            if response.status_code == 200:
                result = response.json()
                st.session_state.interview_prep = result["interview_prep"]
            else:
                show_api_error(response)

    if st.session_state.interview_prep:

        st.write(st.session_state.interview_prep)

        st.download_button(
            "📥 Download Interview Prep",
            st.session_state.interview_prep,
            file_name="interview_prep.txt"
        )

# -----------------------------
# Career Coach Chat
# -----------------------------

st.divider()

st.header("🤖 Career Coach")

# Display previous messages
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat Input
user_query = st.chat_input(
    "Ask your AI Career Coach..."
)

if user_query:

    if not st.session_state.resume_uploaded:
        st.warning("⚠️ Please upload a resume before chatting with the Career Coach.")
    else:
        # Show user message
        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": user_query
            }
        )

        with st.chat_message("user"):
            st.write(user_query)

        # Build conversation history
        history_text = ""
        recent_history = st.session_state.chat_history[-6:]

        for msg in recent_history:
            history_text += (
                f"{msg['role']}: "
                f"{msg['content']}\n"
            )

        # Get AI response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                try:
                    response = requests.post(
                        f"{FASTAPI_URL}/career-agent",
                        json={
                            "question": user_query,
                            "history": history_text
                        },
                        timeout=120  # Long timeout for large LLM responses
                    )

                    # Always try to parse JSON — the route now guarantees a body
                    if response.status_code == 200:
                        result = response.json()
                        answer = result.get("response", "No response received.")
                    else:
                        # Try to extract detail from error JSON
                        try:
                            detail = response.json().get("detail", response.text)
                        except Exception:
                            detail = response.text or f"HTTP {response.status_code}"

                        if "rate_limit" in detail.lower() or "429" in detail:
                            answer = (
                                "⚠️ The AI model hit its daily token limit. "
                                "Please wait a few minutes and try again."
                            )
                        else:
                            answer = f"❌ Server error: {detail}"

                except requests.exceptions.Timeout:
                    answer = "⏱️ The request timed out. The model may be busy — please try again."
                except requests.exceptions.ConnectionError:
                    answer = "❌ Cannot connect to the server. Make sure the FastAPI backend is running."
                except Exception as e:
                    answer = f"❌ Unexpected error: {str(e)}"

                st.write(answer)

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )