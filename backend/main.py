import os
from datetime import datetime, timezone
from typing import Any

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

HINDSIGHT_URL = os.getenv("HINDSIGHT_URL", "http://localhost:8888").rstrip("/")
BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "deal-intelligence-demo")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

app = FastAPI(title="HWH Hindsight Learning Agent")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Interaction(BaseModel):
    customer: str
    interaction: str

class AdviceRequest(BaseModel):
    customer: str
    query: str

async def hindsight_request(method: str, path: str, payload: dict[str, Any] | None = None):
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.request(method, f"{HINDSIGHT_URL}{path}", json=payload)
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"Hindsight error: {response.text}")
    return response.json()

async def retain(content: str):
    return await hindsight_request(
        "POST", "/v1/memory/retain",
        {
            "bank_id": BANK_ID,
            "content": content,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )

async def recall(query: str):
    return await hindsight_request(
        "POST", "/v1/memory/recall",
        {"bank_id": BANK_ID, "query": query},
    )

async def reflect(query: str):
    return await hindsight_request(
        "POST", "/v1/memory/reflect",
        {"bank_id": BANK_ID, "query": query},
    )

async def llm(prompt: str) -> str:
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is not configured")
    async with httpx.AsyncClient(timeout=60) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            json={
                "model": GROQ_MODEL,
                "temperature": 0.2,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are DealIQ, a business deal intelligence agent. Use memory as evidence. Never invent history.",
                    },
                    {"role": "user", "content": prompt},
                ],
            },
        )
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"LLM error: {response.text}")
    return response.json()["choices"][0]["message"]["content"]

@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "hindsight_url": HINDSIGHT_URL,
        "bank_id": BANK_ID,
        "llm_configured": bool(GROQ_API_KEY),
    }

@app.post("/api/interactions")
async def add_interaction(body: Interaction):
    content = (
        f"Customer: {body.customer}\n"
        f"Interaction: {body.interaction}\n"
        f"Captured at: {datetime.now(timezone.utc).isoformat()}"
    )
    return {"ok": True, "hindsight": await retain(content)}

@app.post("/api/advice")
async def get_advice(body: AdviceRequest):
    memory = await recall(
        f"Customer {body.customer}. Query: {body.query}. "
        "Find objections, stakeholder concerns, pricing history, successful and failed approaches."
    )
    reflection = await reflect(
        f"Customer {body.customer}. What patterns and lessons from memory matter for: {body.query}?"
    )
    answer = await llm(
        f"""Customer: {body.customer}
Current query: {body.query}

Retrieved Hindsight memory:
{memory}

Hindsight reflection:
{reflection}

Return:
1. Direct recommendation.
2. Remembered evidence.
3. What was learned over time.
4. One next action.
Keep it concise."""
    )
    return {"answer": answer, "memory": memory, "reflection": reflection, "bank_id": BANK_ID}

@app.get("/api/demo-seed")
async def demo_seed():
    seeds = [
        "Customer: Acme Corp. CFO rejected the initial annual plan because the price felt too high.",
        "Customer: Acme Corp. VP Engineering preferred a phased rollout and wanted a 30-day pilot.",
        "Customer: Acme Corp. responded positively after the offer was reframed around a smaller pilot before annual commitment.",
        "Customer: Beta Systems objected to security-review effort and required a dedicated compliance contact.",
    ]
    for item in seeds:
        await retain(item)
    return {"ok": True, "stored": len(seeds)}
