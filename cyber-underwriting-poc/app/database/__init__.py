from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.utils.config import get_settings

Base = declarative_base()

engine = create_engine(get_settings().database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db() -> None:
    from app.models.company import Company
    from app.models.cyber_assessment import CyberAssessment
    from app.models.underwriting_result import UnderwritingResult

    Base.metadata.create_all(bind=engine)
