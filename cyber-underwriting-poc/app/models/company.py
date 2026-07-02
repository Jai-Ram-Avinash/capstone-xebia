from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    industry = Column(String, nullable=False)
    revenue = Column(Integer, nullable=False)
    employee_count = Column(Integer, nullable=False)

    assessments = relationship("CyberAssessment", back_populates="company")
    results = relationship("UnderwritingResult", back_populates="company")
