from typing import Any

from sqlalchemy.orm import Session

from app.models.cyber_assessment import CyberAssessment


class AssessmentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, assessment_data: dict[str, Any]) -> CyberAssessment:
        assessment = CyberAssessment(**assessment_data)
        self.session.add(assessment)
        self.session.commit()
        self.session.refresh(assessment)
        return assessment

    def get_by_id(self, assessment_id: int) -> CyberAssessment | None:
        return self.session.query(CyberAssessment).filter(CyberAssessment.id == assessment_id).first()
