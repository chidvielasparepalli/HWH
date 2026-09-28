# AEGIS — Code Immune System

Your codebase learns from every failure.

AEGIS is a Hindsight Hackathon prototype that turns past bugs, root causes, fixes, regressions, and outcomes into long-term engineering memory.

## Core loop

incident -> Hindsight recall -> Hindsight reflection -> learned pattern -> fix -> regression protection -> Hindsight retain

## Demo

1. Put your Hindsight Cloud URL and API key in .env.
2. Start the app.
3. Click Load 12 historical failures.
4. Analyze the payment-service sample incident.
5. See the recurring pattern and historical evidence.
6. Enter the verified resolution.
7. Click Teach AEGIS.
8. Re-run a similar incident. The new memory becomes part of the evidence.

## Run

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn backend.main:app --reload

Open http://127.0.0.1:8000

## Environment

HINDSIGHT_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=your_hindsight_key
HINDSIGHT_BANK_ID=aegis-code-immune

Never commit .env.

## Why Hindsight is central

Retain stores verified engineering experience.
Recall finds related historical failures.
Reflect synthesizes lessons from accumulated evidence.

The UI exposes evidence returned from Hindsight so the memory layer is visible in the demo.
