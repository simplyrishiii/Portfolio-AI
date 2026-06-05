"""
Lead Qualification AI — Flask API
Endpoints: POST /qualify  GET /health
"""
import os
from flask import Flask, request, jsonify
from scorer import score_lead
from crm import save_lead
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


@app.route("/qualify", methods=["POST"])
def qualify():
    lead = request.get_json(force=True)
    if not lead:
        return jsonify({"error": "Empty payload"}), 400
    required = ["name", "email"]
    if missing := [f for f in required if f not in lead]:
        return jsonify({"error": f"Missing fields: {missing}"}), 422

    result = score_lead(lead)
    table  = "Hot Leads" if result["score"] >= 70 else "Archive"
    record = save_lead(lead, result, table)

    return jsonify({
        "status":      "ok",
        "score":       result["score"],
        "tier":        result["tier"],
        "action":      result["action"],
        "reason":      result["reason"],
        "table":       table,
        "airtable_id": record.get("id"),
    })


@app.route("/health")
def health():
    return jsonify({"status": "running", "model": "gemini-1.5-flash"})


if __name__ == "__main__":
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)))
