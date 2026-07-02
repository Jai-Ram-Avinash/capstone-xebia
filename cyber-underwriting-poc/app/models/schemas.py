from pydantic import BaseModel, Field


class AssessmentCreate(BaseModel):
    company_name: str = Field(default="Unknown")
    industry: str = Field(default="Unknown")
    revenue: int = Field(default=0)
    employee_count: int = Field(default=0)
    mfa_enabled: bool = False
    edr_enabled: bool = True
    backup_strategy: str = "Yes"
    phishing_training: bool = False
    incident_response_plan: bool = False
    patch_management: bool = False
    encryption: bool = True
    third_party_risk: str = "Low"
    previous_claims: bool = False


class AssessmentResponse(BaseModel):
    assessment_id: int
    company_id: int


class UnderwritingRequest(AssessmentCreate):
    pass


class UnderwritingResponse(BaseModel):
    result_id: int
    risk_score: int
    risk_category: str
    premium: int
    ai_summary: str
    recommendations: list[str]
    coverage_recommendations: list[str]
    ml_prediction: str
    rule_engine_result: str
