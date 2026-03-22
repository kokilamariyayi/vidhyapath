from backend.language.translator import translate_from_english, detect_language

text = "You're nearing the end of your 12th grade, and it's exciting to think about what's next. Since you're interested in Commerce..."
print("Detected:", detect_language(text))
print("Translated:", translate_from_english(text, "ta"))
