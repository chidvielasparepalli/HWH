# HWH — Hindsight Learning Agent

AI deal intelligence agent demonstrating persistent memory and learning with Vectorize Hindsight.

## MVP
- Deal Intelligence Agent
- Hindsight retain / recall / reflect
- Groq-compatible LLM
- FastAPI backend
- Lightweight frontend
- Visible learning evidence

## Run
1. Copy .env.example to .env
2. Add GROQ_API_KEY and HINDSIGHT_URL
3. Start Hindsight locally or use Hindsight Cloud
4. pip install -r requirements.txt
5. uvicorn backend.main:app --reload
6. Open frontend/index.html
