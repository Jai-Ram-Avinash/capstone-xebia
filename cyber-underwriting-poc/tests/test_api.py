from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_assessment_endpoint():
    payload = {
        "company_name": "Example Co",
        "industry": "Healthcare",
        "revenue": 150000000,
        "employee_count": 800,
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

    response = client.post("/assessment", json=payload)
    assert response.status_code == 200
    assert "assessment_id" in response.json()
