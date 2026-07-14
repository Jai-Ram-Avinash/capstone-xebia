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