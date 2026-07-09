# AI-Native Cyber Insurance Underwriting POC

This repository contains a modular FastAPI + Streamlit proof of concept for cyber insurance underwriting. The solution combines a rule-based risk engine, optional AI-generated summaries, and a lightweight machine learning model to demonstrate how AI can support underwriters.

## Architecture

- Backend: FastAPI, SQLAlchemy, SQLite, Pydantic
- Frontend: Streamlit
- AI: LangChain + OpenAI-compatible model
- ML: Random Forest classifier over sample underwriting data

## Setup

- `cd cyber-underwriting-poc`
- Install python 3.11 and check via `python --version`
- Create and activate a virtual environment.
  `python3.11 -m venv venv`
  `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Start the API: `uvicorn main:app --reload`
- Open new terminal,
  `cd cyber-underwriting-poc`
  `source venv/bin/activate` 
  Start the dashboard: `streamlit run frontend/app.py`

## API Endpoints

- POST /assessment
- GET /assessment/{id}
- GET /companies
- POST /underwrite
- GET /results/{id}
- GET /health

## Example Request

```bash
curl -X POST http://127.0.0.1:8000/underwrite -H "Content-Type: application/json" -d '{
  "company_name": "Sample HealthCo",
  "industry": "Healthcare",
  "revenue": 120000000,
  "employee_count": 600,
  "mfa_enabled": false,
  "edr_enabled": true,
  "backup_strategy": "No",
  "phishing_training": false,
  "incident_response_plan": false,
  "patch_management": false,
  "encryption": true,
  "third_party_risk": "High",
  "previous_claims": true
}'
```

## Testing

Run:

```bash
pytest -q
```
