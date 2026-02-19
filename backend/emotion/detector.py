"""
Emotion Detector Module - Lightweight keyword-based version
No heavy ML models needed.
"""

HESITATION_KEYWORDS = [
    "confused", "don't know", "not sure", "scared", "worried", "nervous",
    "difficult", "hard", "can't", "cannot", "afraid", "fear", "lost",
    "help", "stuck", "don't understand", "unclear", "uncertain",
    "parents", "pressure", "force", "don't want", "hate", "boring",
    "pata nahi", "dar", "samajh nahi"
]

CONFIDENCE_KEYWORDS = [
    "want to", "interested in", "love", "passionate", "excited", "sure",
    "definitely", "planning", "goal", "dream", "aim", "decided"
]


def detect_emotion(text: str) -> dict:
    text_lower = text.lower()

    hesitation_score = sum(1 for kw in HESITATION_KEYWORDS if kw in text_lower)
    confidence_score = sum(1 for kw in CONFIDENCE_KEYWORDS if kw in text_lower)
    question_count = text.count("?")

    if hesitation_score >= 2:
        emotion = "hesitant"
    elif hesitation_score >= 1 or question_count >= 2:
        emotion = "uncertain"
    elif confidence_score >= 1:
        emotion = "confident"
    else:
        emotion = "neutral"

    return {
        "emotion": emotion,
        "hesitation_keywords_found": hesitation_score,
        "confidence_keywords_found": confidence_score,
        "ml_emotion": emotion,
        "ml_score": 0.9,
        "response_style": _get_response_style(emotion)
    }


def _get_response_style(emotion: str) -> str:
    styles = {
        "hesitant": "empathetic_encouraging",
        "uncertain": "gentle_informative",
        "confident": "direct_detailed",
        "neutral": "friendly_informative",
        "frustrated": "calm_reassuring"
    }
    return styles.get(emotion, "friendly_informative")
