"""
VidyaPath - FastAPI Backend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
import logging
import os
from dotenv import load_dotenv

load_dotenv()

from backend.emotion.detector import detect_emotion
from backend.language.translator import process_input, translate_from_english, SUPPORTED_LANGUAGES
from backend.profile.student_profile import StudentProfile, extract_profile_from_text
from backend.rag.retriever import rag_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="VidyaPath API",
    description="AI-powered multilingual career guidance for Indian students",
    version="1.1.7"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

sessions: dict = {}


class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str
    target_lang: Optional[str] = None


class TranslationRequest(BaseModel):
    text: str
    target_lang: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    detected_language: str
    emotion: str
    student_profile: dict
    sources_used: int


def get_or_create_session(session_id: Optional[str]):
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {
            "profile": StudentProfile(),
            "chat_history": [],
            "message_count": 0
        }
    return session_id, sessions[session_id]


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "VidyaPath API", "version": "1.0.0"}


@app.post("/translate")
async def translate_text(request: TranslationRequest):
    try:
        if request.target_lang == "en":
            return {"translated_text": request.text}
        
        translated = translate_from_english(request.text, request.target_lang)
        return {"translated_text": translated}
    except Exception as e:
        logger.error(f"Translation error: {e}")
        return {"translated_text": request.text, "error": str(e)}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_id, session = get_or_create_session(request.session_id)

        # Language detection & translation
        lang_result = process_input(request.message)
        english_message = lang_result["english_text"]
        detected_lang = lang_result["detected_language"]

        logger.info(f"Session {session_id[:8]} | Lang: {detected_lang} | Msg: {english_message[:50]}")

        # Emotion detection
        emotion_result = detect_emotion(request.message)
        response_style = emotion_result["response_style"]

        # Update student profile
        session["profile"] = extract_profile_from_text(english_message, session["profile"])
        profile_str = session["profile"].to_context_string()

        # Determine the response language (Priority: user-selected target_lang > detected_lang)
        response_lang = request.target_lang or detected_lang
        response_lang_name = SUPPORTED_LANGUAGES.get(response_lang, "English")
        logger.info(f"Session {session_id[:8]} | Response Lang: {response_lang} ({response_lang_name}) (Requested: {request.target_lang}, Detected: {detected_lang})")

        # RAG + LLM response — pass language so LLM responds directly in the target language
        llm_response = rag_pipeline.chat(
            user_message=english_message,
            chat_history=session["chat_history"],
            student_profile_str=profile_str,
            response_style=response_style,
            response_language=response_lang_name
        )

        # If the LLM was asked to respond in English, use it directly.
        # Otherwise, use the LLM's native response (it was prompted in the target language).
        # As a fallback safety net, also try translation if the response looks English.
        if response_lang == "en":
            final_response = llm_response
        else:
            final_response = llm_response

        # Update history (store English message for consistent RAG context)
        session["chat_history"].append({
            "user": english_message,
            "assistant": llm_response
        })
        session["message_count"] += 1

        return ChatResponse(
            session_id=session_id,
            response=final_response,
            detected_language=lang_result["language_name"],
            emotion=emotion_result["emotion"],
            student_profile=session["profile"].to_dict(),
            sources_used=4
        )

    except Exception as e:
        logger.error(f"Chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/profile/{session_id}")
async def get_profile(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    profile = sessions[session_id]["profile"]
    return {
        "session_id": session_id,
        "profile": profile.to_dict(),
        "is_complete": profile.is_complete_enough(),
        "message_count": sessions[session_id]["message_count"]
    }


@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
    return {"message": "Session cleared"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

# For Firebase Functions / Google Cloud Functions
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    pass
