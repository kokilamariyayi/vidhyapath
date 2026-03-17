"""
Language Detection and Translation Module
Supports Tamil, Hindi, and English.
Uses langdetect for detection and deep_translator (free) for translation.
"""

from langdetect import detect, LangDetectException
from deep_translator import GoogleTranslator
import logging

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi"
}


def detect_language(text: str) -> str:
    """Detect language of input text. Returns language code."""
    try:
        lang = detect(text)
        # langdetect sometimes returns 'zh-cn' etc, normalize
        lang = lang.split("-")[0]
        if lang not in SUPPORTED_LANGUAGES:
            return "en"  # default to English
        return lang
    except LangDetectException:
        return "en"


def translate_to_english(text: str, source_lang: str) -> str:
    """Translate text to English for RAG processing."""
    if source_lang == "en":
        return text
    try:
        translated = GoogleTranslator(source=source_lang, target="en").translate(text)
        return translated
    except Exception as e:
        logger.warning(f"Translation to English failed: {e}")
        return text  # fallback to original


def translate_from_english(text: str, target_lang: str) -> str:
    """Translate English response back to user's language."""
    if target_lang == "en":
        return text
    try:
        # Split long text to handle API limits
        if len(text) > 4500:
            chunks = _split_text(text, 4000)
            translated_chunks = []
            for chunk in chunks:
                translated = GoogleTranslator(source="en", target=target_lang).translate(chunk)
                translated_chunks.append(translated)
            return "\n".join(translated_chunks)
        else:
            translated = GoogleTranslator(source="en", target=target_lang).translate(text)
            return translated
    except Exception as e:
        logger.warning(f"Translation from English failed: {e}")
        return text  # fallback to English


def _split_text(text: str, max_length: int) -> list:
    """Split text into chunks for translation."""
    sentences = text.split(". ")
    chunks = []
    current = ""
    for sentence in sentences:
        if len(current) + len(sentence) < max_length:
            current += sentence + ". "
        else:
            if current:
                chunks.append(current.strip())
            current = sentence + ". "
    if current:
        chunks.append(current.strip())
    return chunks


def process_input(text: str) -> dict:
    """
    Full pipeline: detect language, translate to English if needed.
    Returns dict with original text, detected language, and English version.
    """
    lang = detect_language(text)
    english_text = translate_to_english(text, lang)
    return {
        "original_text": text,
        "detected_language": lang,
        "language_name": SUPPORTED_LANGUAGES.get(lang, "English"),
        "english_text": english_text
    }
