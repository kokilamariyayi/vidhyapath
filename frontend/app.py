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

import os
API_URL = os.environ.get("API_URL", "http://localhost:8000")

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
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
    background: #3949ab;
    color: white;
    padding: 12px 16px;
    border-radius: 18px 18px 4px 18px;
    margin: 8px 0 8px 60px;
    font-size: 0.95rem;
    line-height: 1.5;
}
.bot-message {
    background: rgba(150, 150, 150, 0.1);
    color: inherit;
    padding: 12px 16px;
    border-radius: 18px 18px 18px 4px;
    margin: 8px 60px 8px 0;
    font-size: 0.95rem;
    line-height: 1.6;
    border: 1px solid rgba(150, 150, 150, 0.2);
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
.emotion-hesitant { background: rgba(230, 81, 0, 0.1); color: #ff9800; border: 1px solid rgba(255, 152, 0, 0.3); }
.emotion-confident { background: rgba(27, 94, 32, 0.1); color: #4caf50; border: 1px solid rgba(76, 175, 80, 0.3); }
.emotion-neutral { background: rgba(13, 71, 161, 0.1); color: #2196f3; border: 1px solid rgba(33, 150, 243, 0.3); }
.emotion-uncertain { background: rgba(136, 14, 79, 0.1); color: #e91e63; border: 1px solid rgba(233, 30, 99, 0.3); }

/* Profile card */
.profile-item {
    background: rgba(57, 73, 171, 0.1);
    border-left: 4px solid #3949ab;
    padding: 8px 12px;
    border-radius: 0 8px 8px 0;
    margin: 4px 0;
    font-size: 0.85rem;
    color: inherit;
}

/* Greeting card */
.greeting-card {
    background: rgba(57, 73, 171, 0.05);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    text-align: center;
    border: 1px solid rgba(57, 73, 171, 0.2);
    color: inherit;
}

/* Language indicator */
.lang-indicator {
    background: rgba(171, 71, 188, 0.1);
    color: #ab47bc;
    border: 1px solid rgba(171, 71, 188, 0.3);
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 0.75rem;
    font-weight: 600;
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
if "app_lang" not in st.session_state:
    st.session_state.app_lang = "en"

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

@st.cache_data(show_spinner=False)
def t(text: str, target_lang: str) -> str:
    """Cacheable translation helper for UI elements."""
    if target_lang == "en":
        return text
    try:
        from deep_translator import GoogleTranslator
        return GoogleTranslator(source="en", target=target_lang).translate(text)
    except Exception:
        return text

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
    st.markdown(f"### 👤 {t('Student Profile', st.session_state.app_lang)}")
    if not profile or not any(profile.values()):
        st.info(t("Profile will be built as you chat!", st.session_state.app_lang))
        return

    items = {
        f"🎓 {t('Grade', st.session_state.app_lang)}": profile.get("grade"),
        f"🎓 {t('Degree', st.session_state.app_lang)}": profile.get("degree"),
        f"📚 {t('Stream', st.session_state.app_lang)}": profile.get("stream"),
        f"📍 {t('Location', st.session_state.app_lang)}": profile.get("location"),
        f"⚧ {t('Gender', st.session_state.app_lang)}": profile.get("gender"),
        f"🏷️ {t('Category', st.session_state.app_lang)}": profile.get("category"),
        f"💰 {t('Income', st.session_state.app_lang)}": profile.get("family_income"),
        f"❤️ {t('Interests', st.session_state.app_lang)}": ", ".join(profile.get("interests", [])) if profile.get("interests") else None,
        f"⚠️ {t('Constraints', st.session_state.app_lang)}": ", ".join(profile.get("constraints", [])) if profile.get("constraints") else None
    }

    for label, value in items.items():
        if value:
            st.markdown(f'<div class="profile-item"><b>{label}:</b> {value}</div>',
                       unsafe_allow_html=True)


# ─── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="vidyapath-header">
    <h1>🎓 VidyaPath</h1>
    <p>{t('AI Career Co-pilot for Students, Job Seekers, Parents, and Entrepreneurs', st.session_state.app_lang)}</p>
    <small>Supports English • தமிழ் (Tamil) • हिंदी (Hindi) • తెలుగు (Telugu) • ಕನ್ನಡ (Kannada) • മലയാളം (Malayalam) • मराठी (Marathi)</small>
</div>
""", unsafe_allow_html=True)

# ─── Built-in Sidebar (Left) ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 🌐 {t('Select Language', 'en')}")
    
    languages = {
        "English": "en",
        "Tamil": "ta",
        "Hindi": "hi",
        "Telugu": "te",
        "Kannada": "kn",
        "Malayalam": "ml",
        "Marathi": "mr"
    }
    
    current_lang_name = next(k for k, v in languages.items() if v == st.session_state.app_lang)
    
    selected_lang_name = st.selectbox(
        "Choose your preferred language:",
        options=list(languages.keys()),
        index=list(languages.keys()).index(current_lang_name),
        label_visibility="collapsed"
    )
    
    if languages[selected_lang_name] != st.session_state.app_lang:
        st.session_state.app_lang = languages[selected_lang_name]
        st.rerun()

    st.markdown("---")
    st.markdown(f"### 💡 {t('Try asking', st.session_state.app_lang)}:")
    
    # Translate quick questions
    base_questions = [
        "What are the best job portals for a fresher?",
        "Are there any schemes for women entrepreneurs?",
        "My son is in 10th grade, what should he study next?",
        "What can I study after 12th?",
        "What government schemes are there for job seekers?"
    ]
    quick_questions = [t(q, st.session_state.app_lang) for q in base_questions]
    for q in quick_questions:
        if st.button(q, key=f"quick_{q}", use_container_width=True):
            st.session_state["quick_input"] = q

    st.markdown("---")
    if st.button(f"🗑️ {t('Clear Chat', st.session_state.app_lang)}", type="primary", use_container_width=True):
        if st.session_state.session_id:
            try:
                requests.delete(f"{API_URL}/session/{st.session_state.session_id}")
            except:
                pass
        st.session_state.messages = []
        st.session_state.session_id = None
        st.session_state.profile = {}
        st.rerun()

# ─── Main Content Area (Center Chat + Right corner Profile) ────────────────────
col_chat, col_profile = st.columns([3, 1])

with col_profile:
    render_profile_sidebar(st.session_state.profile)

with col_chat:
    # Welcome message
    if not st.session_state.messages:
        st.markdown(f"""
        <div class="greeting-card">
            <h3>👋 {t('Namaste! Welcome to VidyaPath', st.session_state.app_lang)}</h3>
            <p>{t('I am your AI career guidance co-pilot. I can help:', st.session_state.app_lang)}</p>
            <p>📚 <b>{t('Students', st.session_state.app_lang)}</b> | 💼 <b>{t('Job Seekers', st.session_state.app_lang)}</b> | 👨‍👩‍👧 <b>{t('Parents', st.session_state.app_lang)}</b> | 👩‍💼 <b>{t('Entrepreneurs', st.session_state.app_lang)}</b></p>
            <p><i>{t('Ask me anything!', st.session_state.app_lang)}</i></p>
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
    user_input = st.chat_input(t("Type your question here...", st.session_state.app_lang))

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
        with st.spinner(f"🤔 {t('VidyaPath is thinking...', st.session_state.app_lang)}"):
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
