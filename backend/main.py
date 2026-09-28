import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from hindsight_client import Hindsight

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

HINDSIGHT_URL = os.getenv("HINDSIGHT_URL", "https://api.hindsight.vectorize.io").rstrip("/")
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY") or None
BANK_ID = os.getenv("HINDSIGHT_BANK_ID", "aegis-code-immune")

hindsight = Hindsight(
    base_url=HINDSIGHT_URL,
    api_key=HINDSIGHT_API_KEY,
    timeout=120,
)

app = FastAPI(title="AEGIS — Code Immune System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IncidentRequest(BaseModel):
    service: str = Field(min_length=1, max_length=120)
    incident: str = Field(min_length=5, max_length=10000)


class LearningRequest(BaseModel):
    service: str = Field(min_length=1, max_length=120)
    incident: str = Field(min_length=5, max_length=10000)
    root_cause: str = Field(min_length=3, max_length=4000)
    fix: str = Field(min_length=3, max_length=4000)
    outcome: str = Field(min_length=3, max_length=4000)
    regression_test: str = Field(min_length=3, max_length=4000)


RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "pattern_detected": {"type": "string"},
        "root_cause": {"type": "string"},
        "risk": {"type": "string"},
        "recommended_fix": {"type": "string"},
        "regression_test": {"type": "string"},
        "memory_lesson": {"type": "string"},
        "confidence": {"type": "string"},
    },
    "required": [
        "pattern_detected",
        "root_cause",
        "risk",
        "recommended_fix",
        "regression_test",
        "memory_lesson",
        "confidence",
    ],
}


DEMO_MEMORIES = [
    ("payment-service", "Database connection pool reached its limit during peak traffic. Pool was 50 for roughly 120 concurrent connections. Fix: raise pool to 150 and alert above 85% utilization. Outcome: p95 latency fell from 8.4s to 1.2s."),
    ("payment-service", "A traffic spike caused a retry storm. Clients retried every 200ms with no jitter. Fix: exponential backoff with jitter and a retry budget. Outcome: error rate returned to baseline without database scaling."),
    ("auth-service", "Users were randomly logged out after a deployment because application servers had clock skew over 90 seconds. Fix: NTP synchronization plus a 60-second skew window. Outcome: unexpected logout incidents stopped."),
    ("notification-worker", "Customers received duplicate emails because queue retries were not idempotent. Fix: provider idempotency keys and durable send status. Outcome: duplicate sends stopped."),
    ("image-worker", "Image-processing pods were OOM-killed because full-resolution uploads were decoded simultaneously. Fix: streaming decode and dimension limits before processing. Outcome: memory became stable under burst traffic."),
    ("search-api", "Search latency jumped from 300ms to 5s because an unbounded wildcard query bypassed the intended index path. Fix: reject expensive wildcard patterns and require indexed fields. Outcome: p95 latency returned below 400ms."),
    ("orders-api", "Order-list latency grew with customer history because of N+1 database queries. Fix: batch related data in one query. Outcome: query count fell from hundreds to single digits."),
    ("checkout-service", "A small number of orders were charged twice because payment creation was not idempotent across concurrent requests. Fix: idempotency keys plus unique transaction constraints. Outcome: duplicate charge reports stopped."),
    ("cache-layer", "Redis CPU spiked when a hot key expired and thousands of requests hit the database simultaneously. Fix: request coalescing and stale-while-revalidate caching. Outcome: database load stayed stable."),
    ("upload-api", "Unsafe file access was possible because user filenames were joined to storage paths without canonicalization. Fix: normalize paths, reject traversal segments, and store by generated object IDs. Outcome: traversal attempts were blocked."),
    ("webhook-service", "Invalid webhook signatures were accepted because verification happened after parsing. Fix: verify HMAC over the exact raw request body before parsing. Outcome: invalid events were rejected."),
    ("queue-consumer", "A malformed queue message blocked consumption because poison messages retried forever. Fix: bounded retries plus a dead-letter queue. Outcome: one bad message no longer stalled the worker pool.")
]


def dump(value: Any) -> Any:
    if value is None:
        return None
    if hasattr(value, "model_dump"):
        return value.model_dump(exclude_none=True)
    if isinstance(value, list):
        return [dump(v) for v in value]
    if isinstance(value, dict):
        return {k: dump(v) for k, v in value.items()}
    return value


async def ensure_bank() -> None:
    try:
        await hindsight.acreate_bank(
            bank_id=BANK_ID,
            name="AEGIS Engineering Memory",
            mission=(
                "Remember software failures, causes, fixes, regressions, and outcomes "
                "so future engineering incidents can be diagnosed from accumulated experience."
            ),
        )
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Hindsight connection failed: {exc}") from exc


def evidence_items(response: Any) -> list[dict[str, Any]]:
    return [
        {
            "text": getattr(item, "text", ""),
            "type": getattr(item, "type", ""),
            "context": getattr(item, "context", None),
            "score": getattr(item, "score", None),
        }
        for item in (getattr(response, "results", None) or [])
    ]


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
async def health():
    try:
        await ensure_bank()
        return {"status": "connected", "hindsight_url": HINDSIGHT_URL, "bank_id": BANK_ID}
    except HTTPException as exc:
        return {"status": "error", "detail": exc.detail, "hindsight_url": HINDSIGHT_URL, "bank_id": BANK_ID}


@app.post("/api/demo-seed")
async def demo_seed():
    await ensure_bank()
    for service, lesson in DEMO_MEMORIES:
        await hindsight.aretain(
            bank_id=BANK_ID,
            content=f"Service: {service}
Historical incident: {lesson}",
            context="historical engineering incident",
            tags=["demo", "incident", f"service:{service}"],
        )
    return {"stored": len(DEMO_MEMORIES)}


@app.post("/api/analyze")
async def analyze(body: IncidentRequest):
    await ensure_bank()

    recalled = await hindsight.arecall(
        bank_id=BANK_ID,
        query=(
            f"Current failure in {body.service}: {body.incident}. "
            "Find similar incidents, recurring root causes, successful fixes, "
            "failed approaches, regressions, and observed outcomes."
        ),
        max_tokens=5000,
        budget="mid",
        include_entities=True,
        include_source_facts=True,
    )

    reflection = await hindsight.areflect(
        bank_id=BANK_ID,
        query=(
            "You are AEGIS, a codebase immune-system agent. "
            "Use accumulated engineering experience to diagnose the current failure. "
            "Find repeated failure patterns. Never invent a historical event. "
            "If evidence is weak, say so.

"
            f"SERVICE: {body.service}
"
            f"CURRENT INCIDENT:
{body.incident}

"
            f"RECALLED HINDSIGHT EVIDENCE:
{recalled.to_prompt_string()}"
        ),
        budget="mid",
        response_schema=RESPONSE_SCHEMA,
        include_facts=True,
    )

    structured = getattr(reflection, "structured_output", None) or {
        "pattern_detected": "No structured pattern returned.",
        "root_cause": reflection.text,
        "risk": "Review the evidence before applying changes.",
        "recommended_fix": reflection.text,
        "regression_test": "Add a regression test for the confirmed failure mode.",
        "memory_lesson": "Retain the verified fix and outcome.",
        "confidence": "UNKNOWN",
    }

    evidence = evidence_items(recalled)

    return {
        "analysis": structured,
        "reflection_text": getattr(reflection, "text", ""),
        "evidence": evidence,
        "evidence_count": len(evidence),
        "based_on": dump(getattr(reflection, "based_on", None)),
        "bank_id": BANK_ID,
    }


@app.post("/api/learn")
async def learn(body: LearningRequest):
    await ensure_bank()

    content = (
        f"Service: {body.service}
"
        f"Incident: {body.incident}
"
        f"Confirmed root cause: {body.root_cause}
"
        f"Successful fix: {body.fix}
"
        f"Observed outcome: {body.outcome}
"
        f"Regression protection: {body.regression_test}
"
        f"Verified at: {datetime.now(timezone.utc).isoformat()}"
    )

    result = await hindsight.aretain(
        bank_id=BANK_ID,
        content=content,
        context="verified engineering lesson",
        tags=["learned", "incident", f"service:{body.service}"],
    )

    return {"message": "AEGIS learned the verified resolution.", "retained": dump(result)}


@app.get("/api/memory-profile")
async def memory_profile():
    await ensure_bank()
    reflection = await hindsight.areflect(
        bank_id=BANK_ID,
        query=(
            "Summarize the strongest recurring engineering lessons in memory. "
            "Mention repeated failure patterns, protections that worked, and what AEGIS should watch for next."
        ),
        budget="low",
        include_facts=True,
    )
    return {"summary": reflection.text, "based_on": dump(getattr(reflection, "based_on", None))}


@app.on_event("shutdown")
async def shutdown_event():
    await hindsight.aclose()
