from app.services.risk_engine import calculate_risk, categorize_risk


def test_rule_engine_returns_critical_for_high_risk_profile():
    assessment = {
        "company_name": "Sample HealthCo",
        "industry": "Healthcare",
        "revenue": 120_000_000,
        "employee_count": 600,
        "mfa_enabled": False,
        "edr_enabled": True,
        "backup_strategy": "No",
        "phishing_training": False,
        "incident_response_plan": False,
        "patch_management": False,
        "encryption": True,
        "third_party_risk": "High",
        "previous_claims": True,
    }

    result = calculate_risk(assessment)

    assert result["risk_score"] == 85
    assert result["risk_category"] == "Critical"
    assert "Enable MFA" in result["recommendations"]
    assert "Implement immutable backups" in result["recommendations"]


def test_category_thresholds():
    assert categorize_risk(10) == "Low"
    assert categorize_risk(40) == "Medium"
    assert categorize_risk(60) == "High"
    assert categorize_risk(90) == "Critical"
