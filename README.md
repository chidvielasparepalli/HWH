# AEGIS — Code Immune System

> Your codebase learns from every failure.

AEGIS is a Hindsight Hackathon prototype for technical teams. It builds long-term engineering memory from previous incidents, root causes, fixes, regressions, and outcomes.

## 1. What AEGIS does

Instead of treating every production failure as a brand-new problem, AEGIS asks:

> Have we seen this failure pattern before, what did we learn, and what protection should exist now?

Core loop:

New Incident
→ Hindsight Recall
→ Historical Evidence
→ Hindsight Reflect
→ Failure Pattern + Root Cause
→ Recommended Fix
→ Regression Protection
→ Verified Resolution
→ Hindsight Retain
→ Future incidents become smarter

## 2. Why Hindsight is central

AEGIS uses all three core Hindsight operations:

- Retain: stores verified engineering experiences and outcomes.
- Recall: finds related failures and previously successful fixes.
- Reflect: reasons over accumulated memory and produces a learned diagnosis.

Hindsight is the memory and learning layer, not a decorative integration. The UI exposes retrieved evidence so judges can see exactly why the agent reached its conclusion.

## 3. Tech stack

Frontend
- HTML
- CSS
- Vanilla JavaScript
- Responsive dark command-center UI

Backend
- Python
- FastAPI
- Pydantic
- Uvicorn

Memory
- Vectorize Hindsight Cloud
- Hindsight Python client

## 4. Repository structure

  HWH/
  ├── backend/
  │   ├── __init__.py
  │   └── main.py
  ├── frontend/
  │   ├── index.html
  │   ├── styles.css
  │   └── app.js
  ├── .env.example
  ├── .gitignore
  ├── requirements.txt
  └── README.md

## 5. Prerequisites

Install:

1. Git
   Check with: git --version

2. Python 3.10 or newer
   Check with: python --version
   On Windows, py --version also works.

3. Internet access
   The application connects to Hindsight Cloud at:
   ```text
https://api.hindsight.vectorize.io
```

You do not need HydraDB or RocketRide to run the current MVP.

## 6. Clone the repository

Open PowerShell, Command Prompt, or a terminal:

```bash
git clone https://github.com/chidvielasparepalli/HWH.git
cd HWH
```

Verify:

```bash
git status
```

## 7. Create a virtual environment

Windows PowerShell:

  python -m venv .venv
  .venv\Scripts\Activate.ps1

If PowerShell blocks activation, use Command Prompt:

  .venv\Scripts\activate

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

After activation, the terminal should show .venv or a similar environment marker.

## 8. Install dependencies

Run:

```bash
pip install -r requirements.txt
```

Optional verification:

```bash
pip show hindsight-client
```

## 9. Configure Hindsight Cloud

Create the local environment file.

Windows:
```powershell
copy .env.example .env
```

macOS / Linux:
```bash
cp .env.example .env
```

Open .env and set:

```dotenv
HINDSIGHT_URL=https://api.hindsight.vectorize.io
HINDSIGHT_API_KEY=YOUR_HINDSIGHT_API_KEY
HINDSIGHT_BANK_ID=aegis-code-immune
```

Use the Hindsight API key provided to your team.

IMPORTANT SECURITY RULE:
Never commit .env to GitHub. The repository already ignores .env through .gitignore.

Before pushing code, run:

```bash
git status
```

.env should not appear as an untracked file.

## 10. Start the application

From the HWH project root:

```bash
uvicorn backend.main:app --reload
```

Successful startup should show a local address similar to:

```text
http://127.0.0.1:8000
```

Keep this terminal running.

## 11. Open the application

Open:

  ```text
http://127.0.0.1:8000
```

The dashboard should load.

The top-right connection indicator should become:

  Hindsight connected

That confirms the backend reached Hindsight Cloud and initialized the AEGIS memory bank.

## 12. First-time demo setup

Click:

  Load 12 historical failures

AEGIS writes synthetic engineering memories into Hindsight. The dataset contains examples covering:

- database connection exhaustion
- retry storms
- authentication clock skew
- duplicate notifications
- out-of-memory image processing
- expensive search queries
- N+1 database queries
- duplicate payment creation
- cache stampedes
- path traversal protection
- webhook signature verification
- poison queue messages

These memories exist to make the learning loop visible during the hackathon demo.

## 13. Main demo

Step 1 — Load memory
Click Load 12 historical failures and wait for confirmation.

Step 2 — Submit a new incident

Service:
  payment-service

Incident:
  Payment requests are timing out during a traffic spike. Database connection pool is at 100%, p95 latency is 8.9 seconds, and errors started after traffic doubled.

Step 3 — Run diagnosis
Click Run AEGIS diagnosis.

Step 4 — Watch the result
The UI shows:
- root cause
- risk
- recommended fix
- regression test
- evidence retrieved from Hindsight

## 14. What happens internally

Browser
→ FastAPI
→ Hindsight Recall
→ Historical engineering memories
→ Hindsight Reflect
→ Structured AEGIS diagnosis
→ Browser

The recall query searches for similar incidents, recurring root causes, successful fixes, failed approaches, regressions, and outcomes.

The reflection step reasons over that accumulated evidence and returns structured engineering guidance.

## 15. Teach AEGIS

After solving an incident, use the learning section.

Enter:

Confirmed root cause:
  Connection pool exhaustion caused the timeout.

Successful fix:
  Increased the database pool from 50 to 150 and added an alert at 85% pool utilization.

Observed outcome:
  p95 latency dropped from 8.9 seconds to 1.3 seconds and timeout errors returned to baseline.

Regression protection:
  Added a load test for pool saturation and a production alert when pool utilization remains above 85%.

Click Teach AEGIS what really happened.

That verified engineering experience is retained in Hindsight.

## 16. Prove that it learned

Run the same or a similar incident again.

The memory set now includes:
- previous historical incidents
- the newly verified resolution
- the observed outcome
- the new regression protection

The important story is:

Past failure
→ Past fix
→ Past outcome
→ Hindsight Retain
→ New incident
→ Hindsight Recall
→ Better diagnosis

## 17. Show what the codebase learned

Click Show what AEGIS has learned.

AEGIS asks Hindsight to reflect over the accumulated engineering memory and returns a higher-level summary of recurring failure patterns, protections that worked, and lessons the system should watch for next.

## 18. Architecture

  Browser
     ↓
  AEGIS Dashboard
     ↓
  FastAPI backend
     ↓
  ┌──────────┬───────────┐
  ↓          ↓           ↓
Retain     Recall     Reflect
  └──────────┬───────────┘
             ↓
      Hindsight Cloud
             ↓
   Engineering knowledge

## 19. API endpoints

GET /api/health
Checks the Hindsight connection and memory bank.

POST /api/demo-seed
Adds the 12 synthetic historical incidents.

POST /api/analyze
Runs Hindsight recall, Hindsight reflection, and structured engineering diagnosis.

POST /api/learn
Stores a verified resolution and outcome back into Hindsight.

GET /api/memory-profile
Reflects over the accumulated engineering memory.

## 20. Useful commands

Start server:
  uvicorn backend.main:app --reload

Use another port:
```bash
uvicorn backend.main:app --reload --port 8080
```

Check Git state:
  git status

Upgrade dependencies:
```bash
pip install -r requirements.txt --upgrade
```

Deactivate the virtual environment:
```bash
deactivate
```

## 21. Troubleshooting

### Python not found

Check:
```bash
python --version
```
```powershell
py --version
```

If py works on Windows, create the environment with:
  py -m venv .venv

### PowerShell blocks activation

Use Command Prompt and run:
  .venv\Scripts\activate

### Missing module

Make sure the virtual environment is active, then run:
  pip install -r requirements.txt

### Hindsight connection failed

Check:
1. HINDSIGHT_URL is correct.
2. HINDSIGHT_API_KEY is present in .env.
3. Internet access works.
4. The key is valid.
5. The backend was restarted after editing .env.

### CSS or JavaScript is missing

Start the site through FastAPI:
  uvicorn backend.main:app --reload

Then open:
  ```text
http://127.0.0.1:8000
```

Do not open frontend/index.html directly with a file URL for the full application flow.

### No evidence appears

First click Load 12 historical failures and wait for completion. Then run the diagnosis again.

## 22. Judge demo sequence

Use this order for a fast live demonstration:

1. Explain the problem:
   Production failures often repeat, but most assistants treat every incident like the first incident.

2. Introduce AEGIS:
   AEGIS builds long-term engineering memory using Hindsight.

3. Load 12 historical failures.

4. Submit the payment-service incident.

5. Run AEGIS diagnosis.

6. Point to the historical evidence retrieved from Hindsight.

7. Show the recommended fix and regression test.

8. Enter the verified resolution and click Teach AEGIS.

9. Re-run the incident.

10. Show that the new verified experience is now part of the agent's memory.

11. Open Show what AEGIS has learned.

Suggested closing statement:

> AEGIS does not just remember what happened. It remembers what fixed it, what happened afterward, and uses that experience the next time the codebase fails.

## 23. Security

Never place secrets directly in backend/main.py, frontend/app.js, frontend/index.html, or README files.

Use .env:
  HINDSIGHT_API_KEY=...

The repository ignores .env.

If a key is ever committed accidentally, revoke it immediately and replace it.

## 24. Git workflow

Pull latest changes:
```bash
git pull origin main
```

Review changes:
  git status

Stage:
```bash
git add .
```

Commit:
```bash
git commit -m "Update AEGIS"
```

Push:
```bash
git push origin main
```

Before pushing, make sure .env is not included.

## 25. Current MVP scope

AEGIS intentionally focuses on one technical problem:

> Learning from software failures.

It is not trying to become a complete observability platform, ticketing platform, CI/CD platform, or incident-management suite.

The hackathon value is the learning loop:

Engineering experience
+ Long-term memory
+ Reflection
= Smarter future diagnosis

## Hackathon note

AEGIS is a hackathon prototype built to demonstrate Hindsight-powered persistent agent memory.

Built with Vectorize Hindsight, Python, FastAPI, HTML, CSS, and JavaScript.