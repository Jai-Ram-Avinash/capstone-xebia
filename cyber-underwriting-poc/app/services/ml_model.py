from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score


def train_model() -> tuple[Pipeline, dict[str, object]]:
    sample_data = pd.DataFrame(
        [
            {"mfa_enabled": False, "edr_enabled": True, "backup_strategy": "No", "phishing_training": False, "incident_response_plan": False, "patch_management": False, "encryption": True, "third_party_risk": "High", "previous_claims": True, "risk_category": "Critical"},
            {"mfa_enabled": True, "edr_enabled": True, "backup_strategy": "Yes", "phishing_training": True, "incident_response_plan": True, "patch_management": True, "encryption": True, "third_party_risk": "Low", "previous_claims": False, "risk_category": "Low"},
            {"mfa_enabled": False, "edr_enabled": False, "backup_strategy": "No", "phishing_training": False, "incident_response_plan": False, "patch_management": False, "encryption": False, "third_party_risk": "High", "previous_claims": True, "risk_category": "Critical"},
            {"mfa_enabled": True, "edr_enabled": True, "backup_strategy": "Yes", "phishing_training": True, "incident_response_plan": False, "patch_management": True, "encryption": True, "third_party_risk": "Medium", "previous_claims": False, "risk_category": "Medium"},
        ]
    )

    X = sample_data.drop(columns=["risk_category"])
    y = sample_data["risk_category"]
    categorical_features = ["backup_strategy", "third_party_risk"]
    numeric_features = [col for col in X.columns if col not in categorical_features]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", "passthrough", numeric_features),
        ]
    )

    model = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", RandomForestClassifier(n_estimators=50, random_state=42))])
    model.fit(X, y)

    predictions = model.predict(X)
    accuracy = accuracy_score(y, predictions)
    return model, {"accuracy": accuracy}


def predict_risk_category(model: Pipeline, assessment: dict[str, object]) -> str:
    df = pd.DataFrame([assessment])
    return str(model.predict(df)[0])
