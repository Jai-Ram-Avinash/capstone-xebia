from fastapi import FastAPI
from dotenv import load_dotenv

from app.api.routes import router
from app.database import init_db
from app.utils.logging_config import setup_logging

load_dotenv()

setup_logging()

app = FastAPI(title="AI-Native Cyber Underwriting POC", version="0.1.0")
app.include_router(router)

init_db()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
