"""
VidyaPath - Streamlit Frontend
Emotion-aware multilingual career guidance chatbot UI.
"""

import streamlit as st
import requests
import json
from datetime import datetime

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VidyaPath - Career Guidance",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://localhost:8000"

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Main background */
.main { background-color: #f0f4f8; }

/* Header */
.vidyapath-header {
    background: linear-gradient(135deg, #1a237e 0%, #283593 50%, #3949ab 100%);
    padding: 20px 30px;
    border-radius: 12px;
    color: white;
    margin-bottom: 20px;
    text-align: center;
}
.vidyapath-header h1 { margin: 0; font-size: 2rem; }
.vidyapath-header p { margin: 5px 0 0; opacity: 0.85; font-size: 1rem; }

/* Chat messages */
.user-message {
    background: #1a237e;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px 60px;
    font-size: 0.95rem;
    line-height: 1.5;
}
.bot-message {
    background: white;
    color: #1a1a2e;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 60px 8px 0;
    font-size: 0.95rem;
    line-height: 1.6;
    border: 1px solid #e0e7ff;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* Emotion badge */
.emotion-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
    margin-left: 8px;
}
.emotion-hesitant { background: #fff3e0; color: #e65100; }
.emotion-confident { background: #e8f5e9; color: #1b5e20; }
.emotion-neutral { background: #e3f2fd; color: #0d47a1; }
.emotion-uncertain { background: #fce4ec; color: #880e4f; }

/* Profile card */
.profile-item {
    background: #e8eaf6;
    border-left: 4px solid #3949ab;
    padding: 8px 12px;
    border-radius: 0 8px 8px 0;
    margin: 4px 0;
    font-size: 0.85rem;
}

/* Greeting card */
.greeting-card {
    background: linear-gradient(135deg, #e8eaf6, #c5cae9);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    text-align: center;
    border: 1px solid #9fa8da;
}

/* Language indicator */
.lang-indicator {
    background: #f3e5f5;
    color: #6a1b9a;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.75rem;
    font-weight: 600;
}

/* Quick question buttons */
.stButton button {
    background: #e8eaf6;
    color: #1a237e;
    border: 1px solid #9fa8da;
    border-radius: 20px;
    font-size: 0.8rem;
    padding: 4px 12px;
    transition: all 0.2s;
}
.stButton button:hover {
    background: #1a237e;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ─────────────────────────────────────────────────────────
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "profile" not in st.session_state:
    st.session_state.profile = {}
if "last_emotion" not in st.session_state:
    st.session_state.last_emotion = "neutral"


# ─── Helper Functions ──────────────────────────────────────────────────────────
def send_message(user_input: str):
    """Send message to backend and return response."""
    try:
        payload = {
            "session_id": st.session_state.session_id,
            "message": user_input
        }
        response = requests.post(f"{API_URL}/chat", json=payload, timeout=60)
        if response.status_code == 200:
            data = response.json()
            st.session_state.session_id = data["session_id"]
            st.session_state.profile = data["student_profile"]
            st.session_state.last_emotion = data["emotion"]
            return data
        else:
            return {"error": f"Server error: {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to backend. Make sure the FastAPI server is running on port 8000."}
    except Exception as e:
        return {"error": str(e)}


def get_emotion_badge(emotion: str) -> str:
    badges = {
        "hesitant": '<span class="emotion-badge emotion-hesitant">🤔 Hesitant</span>',
        "uncertain": '<span class="emotion-badge emotion-uncertain">❓ Uncertain</span>',
        "confident": '<span class="emotion-badge emotion-confident">✨ Confident</span>',
        "neutral": '<span class="emotion-badge emotion-neutral">💬 Neutral</span>',
        "frustrated": '<span class="emotion-badge emotion-hesitant">😤 Frustrated</span>'
    }
    return badges.get(emotion, "")


def render_profile_sidebar(profile: dict):
    """Render student profile in sidebar."""
    st.markdown("### 👤 Student Profile")
    if not profile or not any(profile.values()):
        st.info("Profile will be built as you chat!")
        return

    items = {
        "🎓 Grade": profile.get("grade"),
        "📚 Stream": profile.get("stream"),
        "📍 Location": profile.get("location"),
        "⚧ Gender": profile.get("gender"),
        "🏷️ Category": profile.get("category"),
        "💰 Income": profile.get("family_income"),
        "❤️ Interests": ", ".join(profile.get("interests", [])) or None,
        "⚠️ Constraints": ", ".join(profile.get("constraints", [])) or None
    }

    for label, value in items.items():
        if value:
            st.markdown(f'<div class="profile-item"><b>{label}:</b> {value}</div>',
                       unsafe_allow_html=True)


# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="vidyapath-header">
    <h1>🎓 VidyaPath</h1>
    <p>AI-Powered Career Guidance for Students in Grades 8–12</p>
    <small>Supports English • हिंदी (Hindi) • தமிழ் (Tamil)</small>
</div>
""", unsafe_allow_html=True)

# ─── Layout: Chat + Sidebar ────────────────────────────────────────────────────
col_chat, col_sidebar = st.columns([3, 1])

with col_sidebar:
    render_profile_sidebar(st.session_state.profile)

    st.markdown("---")
    st.markdown("### 🌐 Language")
    st.info("Just type in Tamil, Hindi, or English — VidyaPath will detect and respond in your language!")

    st.markdown("---")
    st.markdown("### 💡 Try asking:")
    quick_questions = [
        "What can I do after Class 10?",
        "Which stream is best for becoming a doctor?",
        "Are there scholarships for girls?",
        "Tell me about ITI courses",
        "10வது பிறகு என்ன படிக்கலாம்?",
        "मुझे कौन सी stream चुननी चाहिए?"
    ]
    for q in quick_questions:
        if st.button(q, key=f"quick_{q}", use_container_width=True):
            st.session_state["quick_input"] = q

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        if st.session_state.session_id:
            try:
                requests.delete(f"{API_URL}/session/{st.session_state.session_id}")
            except:
                pass
        st.session_state.messages = []
        st.session_state.session_id = None
        st.session_state.profile = {}
        st.rerun()

with col_chat:
    # Welcome message
    if not st.session_state.messages:
        st.markdown("""
        <div class="greeting-card">
            <h3>👋 Namaste! Welcome to VidyaPath</h3>
            <p>I'm your AI career guidance co-pilot. I can help you with:</p>
            <p>📚 Academic streams after 10th | 🛠️ Vocational & ITI courses | 💰 Scholarships & government schemes | 🗺️ Career pathways</p>
            <p><i>Ask me anything in English, Hindi, or Tamil!</i></p>
        </div>
        """, unsafe_allow_html=True)

    # Chat history display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                lang_badge = f'<span class="lang-indicator">🌐 {msg.get("lang", "English")}</span>' if msg.get("lang") != "English" else ""
                st.markdown(
                    f'<div class="user-message">👤 {msg["content"]} {lang_badge}</div>',
                    unsafe_allow_html=True
                )
            else:
                emotion_badge = get_emotion_badge(msg.get("emotion", "neutral"))
                st.markdown(
                    f'<div class="bot-message">🎓 {msg["content"]}{emotion_badge}</div>',
                    unsafe_allow_html=True
                )

    # Input area
    st.markdown("---")
    user_input = st.chat_input("Type your question here... (English, हिंदी, or தமிழ்)")

    # Handle quick question buttons
    if "quick_input" in st.session_state:
        user_input = st.session_state.pop("quick_input")

    if user_input:
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "lang": "detecting..."
        })

        # Show spinner while processing
        with st.spinner("🤔 VidyaPath is thinking..."):
            result = send_message(user_input)

        if "error" in result:
            st.error(f"❌ {result['error']}")
            st.session_state.messages.pop()
        else:
            # Update user message with detected language
            st.session_state.messages[-1]["lang"] = result["detected_language"]

            # Add bot response
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["response"],
                "emotion": result["emotion"],
                "sources": result["sources_used"]
            })

        st.rerun()
