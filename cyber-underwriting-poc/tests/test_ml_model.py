from app.services.ml_model import predict_risk_category, train_model


def test_ml_model_predicts_category():
    model, _ = train_model()
    prediction = predict_risk_category(
        model,
        {
            "mfa_enabled": False,
            "edr_enabled": True,
            "backup_strategy": "No",
            "phishing_training": False,
            "incident_response_plan": False,
            "patch_management": False,
            "encryption": True,
            "third_party_risk": "High",
            "previous_claims": True,
        },
    )
    assert prediction in {"Critical", "Medium", "Low", "High"}
