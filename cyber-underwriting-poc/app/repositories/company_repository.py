from typing import Any

from sqlalchemy.orm import Session

from app.models.company import Company


class CompanyRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, company_data: dict[str, Any]) -> Company:
        company = Company(**company_data)
        self.session.add(company)
        self.session.commit()
        self.session.refresh(company)
        return company

    def get_all(self) -> list[Company]:
        return self.session.query(Company).all()

    def get_by_id(self, company_id: int) -> Company | None:
        return self.session.query(Company).filter(Company.id == company_id).first()
