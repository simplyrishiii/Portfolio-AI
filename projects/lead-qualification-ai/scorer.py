"""
Lead Scoring Engine — Gemini 1.5 Flash
BANT framework: Budget / Authority / Need / Timeline (25 pts each)
"""
import os, json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
_model = genai.GenerativeModel("gemini-1.5-flash")

PROMPT = """\
You are a B2B lead qualification expert using the BANT framework.
Score this lead and return ONLY valid JSON (no markdown fences).

Lead data:
{lead}

Scoring rubric (25 pts each):
- budget:    Does the lead have/mention budget for a $500+/mo solution?
- authority: Are they a decision-maker or influencer?
- need:      Do they have a clear, urgent pain point?
- timeline:  Are they looking to buy within 90 days?

Return:
{{
  "score": <int 0-100>,
  "tier": "<HOT|WARM|COLD>",
  "budget": <0-25>,
  "authority": <0-25>,
  "need": <0-25>,
  "timeline": <0-25>,
  "reason": "<one crisp sentence>",
  "action": "<CALL_NOW|NURTURE|DISQUALIFY>"
}}"""


def score_lead(lead: dict) -> dict:
    resp = _model.generate_content(PROMPT.format(lead=json.dumps(lead, indent=2)))
    raw  = resp.text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
    data = json.loads(raw)
    # Clamp score
    data["score"] = max(0, min(100, int(data.get("score", 0))))
    data["tier"]  = data.get("tier", "COLD").upper()
    return data
