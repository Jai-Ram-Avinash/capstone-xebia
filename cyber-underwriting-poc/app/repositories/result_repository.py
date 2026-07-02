from typing import Any

from sqlalchemy.orm import Session

from app.models.underwriting_result import UnderwritingResult


class ResultRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, result_data: dict[str, Any]) -> UnderwritingResult:
        result = UnderwritingResult(**result_data)
        self.session.add(result)
        self.session.commit()
        self.session.refresh(result)
        return result

    def get_by_id(self, result_id: int) -> UnderwritingResult | None:
        return self.session.query(UnderwritingResult).filter(UnderwritingResult.id == result_id).first()
