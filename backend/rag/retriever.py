"""
RAG Retriever - Uses TF-IDF search + Groq LLM (free)
No ChromaDB or HuggingFace required.
"""

import os
from groq import Groq
from backend.rag.ingest import search_docs
from backend.prompts.templates import get_prompt_template


class VidyaPathRAG:
    def __init__(self):
        self._client = None
        self._initialized = False

    def initialize(self):
        if self._initialized:
            return
        print("🔄 Initializing Groq client...")
        self._client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self._initialized = True
        print("✅ Groq ready!")

    def get_relevant_context(self, query: str) -> str:
        """Search for relevant docs and return as context string."""
        try:
            docs = search_docs(query, top_k=4)
            if not docs:
                return "No specific data found. Use general knowledge about Indian education system."
            return "\n\n---\n\n".join([doc["content"] for doc in docs])
        except Exception:
            return "Use general knowledge about Indian education system."

    def chat(
        self,
        user_message: str,
        chat_history: list,
        student_profile_str: str,
        response_style: str = "friendly_informative"
    ) -> str:
        self.initialize()

        retrieved_context = self.get_relevant_context(user_message)

        system_template = get_prompt_template(response_style)
        system_prompt = system_template.format(
            student_profile=student_profile_str,
            retrieved_context=retrieved_context
        )

        messages = [{"role": "system", "content": system_prompt}]

        for turn in chat_history[-6:]:
            messages.append({"role": "user", "content": turn["user"]})
            messages.append({"role": "assistant", "content": turn["assistant"]})

        messages.append({"role": "user", "content": user_message})

        response = self._client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.3,
            max_tokens=1024
        )
        return response.choices[0].message.content


rag_pipeline = VidyaPathRAG()
