import logging
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.schemas import AssessmentCreate, AssessmentResponse, UnderwritingRequest, UnderwritingResponse
from app.models.company import Company
from app.models.cyber_assessment import CyberAssessment
from app.models.underwriting_result import UnderwritingResult
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.company_repository import CompanyRepository
from app.repositories.result_repository import ResultRepository
from app.services.ai_underwriter import AIUnderwriter
from app.services.ml_model import predict_risk_category, train_model
from app.services.risk_engine import calculate_risk

router = APIRouter()
logger = logging.getLogger(__name__)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/assessment", response_model=AssessmentResponse)
def save_assessment(payload: AssessmentCreate, db: Session = Depends(get_db)) -> dict[str, Any]:
    try:
        company_repo = CompanyRepository(db)
        assessment_repo = AssessmentRepository(db)
        company = company_repo.create(
            {
                "company_name": payload.company_name,
                "industry": payload.industry,
                "revenue": payload.revenue,
                "employee_count": payload.employee_count,
            }
        )
        assessment = assessment_repo.create({"company_id": company.id, **payload.model_dump(exclude={"company_name", "industry", "revenue", "employee_count"})})
        logger.info("Assessment saved", extra={"company_id": company.id})
        return {"assessment_id": assessment.id, "company_id": company.id}
    except Exception as exc:
        logger.exception("Assessment save failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/assessment/{assessment_id}")
def get_assessment(assessment_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    assessment = AssessmentRepository(db).get_by_id(assessment_id)
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return {
        "id": assessment.id,
        "company_id": assessment.company_id,
        "mfa_enabled": assessment.mfa_enabled,
        "edr_enabled": assessment.edr_enabled,
        "backup_strategy": assessment.backup_strategy,
        "phishing_training": assessment.phishing_training,
        "incident_response_plan": assessment.incident_response_plan,
        "patch_management": assessment.patch_management,
        "encryption": assessment.encryption,
        "third_party_risk": assessment.third_party_risk,
        "previous_claims": assessment.previous_claims,
    }


@router.get("/companies")
def list_companies(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    companies = CompanyRepository(db).get_all()
    return [{"id": company.id, "company_name": company.company_name, "industry": company.industry} for company in companies]


@router.post("/underwrite", response_model=UnderwritingResponse)
def run_underwriting(payload: UnderwritingRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    try:
        company_repo = CompanyRepository(db)
        assessment_repo = AssessmentRepository(db)
        result_repo = ResultRepository(db)

        company = company_repo.create(
            {
                "company_name": payload.company_name,
                "industry": payload.industry,
                "revenue": payload.revenue,
                "employee_count": payload.employee_count,
            }
        )
        assessment = assessment_repo.create({"company_id": company.id, **payload.model_dump(exclude={"company_name", "industry", "revenue", "employee_count"})})

        risk_result = calculate_risk(payload.model_dump())
        ai_underwriter = AIUnderwriter()
        ai_summary = ai_underwriter.generate_summary(payload.model_dump(), risk_result)

        model, _ = train_model()
        ml_prediction = predict_risk_category(model, payload.model_dump())

        result = result_repo.create(
            {
                "company_id": company.id,
                "risk_score": risk_result["risk_score"],
                "risk_level": risk_result["risk_category"],
                "premium": risk_result["premium"],
                "ai_summary": ai_summary,
                "recommendations": "; ".join(risk_result["recommendations"]),
            }
        )
        logger.info("Underwriting completed", extra={"result_id": result.id, "ml_prediction": ml_prediction})
        return {
            "result_id": result.id,
            "risk_score": risk_result["risk_score"],
            "risk_category": risk_result["risk_category"],
            "premium": risk_result["premium"],
            "ai_summary": ai_summary,
            "recommendations": risk_result["recommendations"],
            "coverage_recommendations": risk_result["coverage_recommendations"],
            "ml_prediction": ml_prediction,
            "rule_engine_result": risk_result["risk_category"],
        }
    except Exception as exc:
        logger.exception("Underwriting failed")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/results/{result_id}")
def get_result(result_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    result = ResultRepository(db).get_by_id(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    return {
        "id": result.id,
        "company_id": result.company_id,
        "risk_score": result.risk_score,
        "risk_level": result.risk_level,
        "premium": result.premium,
        "ai_summary": result.ai_summary,
        "recommendations": result.recommendations,
    }
