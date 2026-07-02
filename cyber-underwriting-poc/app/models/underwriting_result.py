from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class UnderwritingResult(Base):
    __tablename__ = "underwriting_results"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    premium = Column(Float, nullable=False)
    ai_summary = Column(String, nullable=False)
    recommendations = Column(String, nullable=False)

    company = relationship("Company", back_populates="results")
