# 🎓 VidyaPath — Emotion-Aware Multilingual Career Guidance Chatbot

> An advanced AI-powered career co-pilot for Indian students in Grades 8–12. Built with RAG, emotion detection, and multilingual support — all using **100% free tools**.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![LangChain](https://img.shields.io/badge/LangChain-0.2.x-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.112-teal)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🌟 What Makes This Different

| Feature | Basic Chatbot | VidyaPath |
|---|---|---|
| LLM Usage | Raw GPT-3 wrapper | RAG over real NSDC/scholarship data |
| Memory | None | Multi-turn conversation memory |
| Emotion Detection | None | Detects hesitation → adapts tone |
| Language Support | English only | Tamil 🇮🇳, Hindi 🇮🇳, English |
| Recommendations | None | Profile-based pathway mapping |
| Architecture | Single `app.py` | FastAPI + modular components |
| Data | None | Real NSDC, ITI, scholarship data |

---

## 🏗️ Architecture

```
User (Streamlit UI)
       ↓
FastAPI Backend (/chat endpoint)
       ↓
  ┌─────────────────────┐
  │  Language Detector  │ ← langdetect (auto-detects Tamil/Hindi/English)
  │  + Translator       │ ← deep-translator (Google Translate, free)
  └──────────┬──────────┘
             ↓
  ┌─────────────────────┐
  │  Emotion Detector   │ ← HuggingFace zero-shot + keyword rules
  │                     │ ← Routes to empathetic/direct/gentle prompts
  └──────────┬──────────┘
             ↓
  ┌─────────────────────┐
  │  Student Profile    │ ← Extracts grade, stream, location, interests
  │  Accumulator        │ ← Builds context across conversation turns
  └──────────┬──────────┘
             ↓
  ┌─────────────────────┐
  │  RAG Pipeline       │ ← ChromaDB + HuggingFace MiniLM embeddings
  │                     │ ← Retrieves: scholarships, ITI, streams, schemes
  └──────────┬──────────┘
             ↓
  ┌─────────────────────┐
  │  Groq LLM           │ ← Llama 3.3 70B (FREE, fast)
  │  (Llama 3.3 70B)    │ ← Emotion-aware prompt templates
  └─────────────────────┘
       ↓
  Translate response back → User's language
```

---

## 📁 Project Structure

```
vidyapath/
├── backend/
│   ├── main.py                    # FastAPI app with /chat, /profile endpoints
│   ├── rag/
│   │   ├── ingest.py              # Embed all data into ChromaDB
│   │   └── retriever.py           # LangChain RAG + Groq LLM
│   ├── emotion/
│   │   └── detector.py            # Emotion classification (hesitant/confident/etc.)
│   ├── language/
│   │   └── translator.py          # Language detect + translate pipeline
│   ├── profile/
│   │   └── student_profile.py     # Profile builder from conversation
│   └── prompts/
│       └── templates.py           # Emotion-aware prompt templates
├── frontend/
│   └── app.py                     # Streamlit chat UI
├── data/
│   ├── scholarships.json          # 7 real central + state scholarships
│   ├── vocational_pathways.json   # 6 ITI/NSDC/Polytechnic pathways
│   ├── govt_schemes.json          # 6 government schemes (PMKVY, YASASVI etc.)
│   └── academic_streams.json      # 5 academic streams with career paths
├── .env.example                   # Environment template
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Free [Groq API key](https://console.groq.com) (takes 2 minutes to get)

### Step 1: Clone & Setup
```bash
git clone https://github.com/yourusername/vidyapath.git
cd vidyapath

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Key
```bash
cp .env.example .env
# Edit .env and add your Groq API key
```

### Step 3: Ingest Data into Vector Store
```bash
python -m backend.rag.ingest
```
This embeds all scholarship, vocational, scheme, and stream data into ChromaDB locally. Takes ~2 minutes on first run.

### Step 4: Start the Backend
```bash
uvicorn backend.main:app --reload --port 8000
```

### Step 5: Start the Frontend (new terminal)
```bash
streamlit run frontend/app.py
```

Open **http://localhost:8501** — you're live! 🎉

---

## 💡 Example Conversations

**English:**
> "I'm in Class 10 and confused about which stream to pick. I love biology but also like computers."

**Tamil:**
> "நான் 10ஆம் வகுப்பு படிக்கிறேன். என்ன படிக்கலாம்?"

**Hindi:**
> "मैं कक्षा 10 में हूँ, ITI के बारे में बताओ"

---

## 🔑 Key Concepts Demonstrated

1. **RAG (Retrieval-Augmented Generation)** — Real data grounded responses, no hallucination
2. **Emotion-Aware AI** — 5 emotion states → 5 different prompt templates
3. **Multilingual NLP** — Auto-detect + translate → process → translate back
4. **Student Profile Accumulation** — Builds context across turns using regex + NER
5. **Explainable Recommendations** — Every recommendation includes a "why"
6. **Clean Architecture** — FastAPI backend + Streamlit frontend, modular design

---

## 🛠️ Tech Stack (All Free)

| Component | Tool |
|---|---|
| LLM | Groq API — Llama 3.3 70B (free tier) |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` (local) |
| Vector Store | ChromaDB (local) |
| RAG Framework | LangChain |
| Emotion Detection | HuggingFace Transformers |
| Translation | deep-translator (Google Translate wrapper) |
| Language Detection | langdetect |
| Backend | FastAPI + Uvicorn |
| Frontend | Streamlit |
| Hosting | Streamlit Community Cloud (free) |

---

## 📊 Data Sources

All data is compiled from publicly available sources:
- [National Scholarship Portal](https://scholarships.gov.in)
- [NSDC Skill India](https://nsdcindia.org)
- [PM Kaushal Vikas Yojana](https://pmkvyofficial.org)
- [AICTE Scholarships](https://www.aicte-india.org)
- State government education portals

---

## 🤝 Contributing

Contributions welcome! Areas to improve:
- Add more states' specific schemes
- Add more vernacular languages (Telugu, Kannada, Marathi)
- Improve emotion detection with fine-tuned Indian language models
- Add a recommendation dashboard with visualizations

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built with ❤️ to bridge the career guidance gap for students in underserved regions of India.*
