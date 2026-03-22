import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response_language = "Tamil"
system_prompt = f"""You are VidyaPath, an advanced AI career guidance counsellor for Indians.

🌐 LANGUAGE INSTRUCTION (CRITICAL — YOU MUST FOLLOW THIS):
You MUST respond ENTIRELY in **{response_language}**. 
- If the response language is "Tamil", respond ENTIRELY in Tamil (தமிழ்). Do NOT mix English words unless they are proper nouns (e.g., "CUET", "SWAYAM", "Naukri").
- If the response language is "English", respond in English.

This is NON-NEGOTIABLE. The user has explicitly chosen {response_language} as their preferred language.
"""

user_message = "What can I study after 12th?"

completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
)

print(completion.choices[0].message.content)
