#!/bin/bash
# VidyaPath Quick Setup Script

echo "🎓 Setting up VidyaPath..."

# Check Python
python3 --version || { echo "❌ Python 3.10+ required"; exit 1; }

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check for .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Groq API key"
    echo "   Get a FREE key at: https://console.groq.com"
    echo ""
    read -p "Press Enter after you've added your key..."
fi

# Ingest data
echo "🗄️  Ingesting data into ChromaDB..."
python -m backend.rag.ingest

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start VidyaPath:"
echo "  Terminal 1: uvicorn backend.main:app --reload --port 8000"
echo "  Terminal 2: streamlit run frontend/app.py"
echo ""
echo "Then open: http://localhost:8501"
