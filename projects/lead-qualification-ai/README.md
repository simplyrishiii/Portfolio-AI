# Lead Qualification AI System

> Autonomous B2B lead scoring and routing — zero human intervention required.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Gemini](https://img.shields.io/badge/Gemini-1.5--Flash-green)](https://ai.google.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Architecture
```
Inbound Lead → n8n Webhook → Gemini Scoring Agent → Airtable CRM → Auto-Response
                                      ↓
                            Score ≥ 70 → Hot Leads table
                            Score < 70 → Archive table
```

## Stack
| Layer | Tech |
|-------|------|
| LLM Scoring | Google Gemini 1.5 Flash |
| Orchestration | n8n (workflow automation) |
| CRM | Airtable |
| Backend | Flask + ngrok |
| Deployment | Render |

## Setup
```bash
git clone https://github.com/simplyrishiii/Portfolio-AI
cd Portfolio-AI/projects/lead-qualification-ai
pip install -r requirements.txt
cp .env.example .env   # fill your keys
python app.py
```

Import `n8n_workflow.json` into your n8n instance. Set webhook URL to your endpoint.

## API
```bash
curl -X POST http://localhost:5000/qualify \
  -H 'Content-Type: application/json' \
  -d '{"name":"John","email":"john@acme.com","company":"Acme","message":"Need AI solution for 500 users ASAP, budget approved"}'
```

## Response
```json
{
  "score": 87,
  "tier": "HOT",
  "action": "CALL_NOW",
  "reason": "Decision maker with approved budget and urgent timeline",
  "table": "Hot Leads"
}
```
