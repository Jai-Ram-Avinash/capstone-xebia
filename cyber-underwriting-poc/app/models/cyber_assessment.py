from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class CyberAssessment(Base):
    __tablename__ = "cyber_assessments"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    mfa_enabled = Column(Boolean, nullable=False)
    edr_enabled = Column(Boolean, nullable=False)
    backup_strategy = Column(String, nullable=False)
    phishing_training = Column(Boolean, nullable=False)
    incident_response_plan = Column(Boolean, nullable=False)
    patch_management = Column(Boolean, nullable=False)
    encryption = Column(Boolean, nullable=False)
    third_party_risk = Column(String, nullable=False)
    previous_claims = Column(Boolean, nullable=False)

    company = relationship("Company", back_populates="assessments")
