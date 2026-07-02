from __future__ import annotations

from typing import Any


BASE_PREMIUM = 10_000
PREMIUM_MULTIPLIER = 150


def calculate_risk(assessment: dict[str, Any]) -> dict[str, Any]:
    score = 0
    recommendations: list[str] = []

    if not assessment.get("mfa_enabled", False):
        score += 20
        recommendations.append("Enable MFA")
    if assessment.get("backup_strategy") in {"No", "None", ""}:
        score += 20
        recommendations.append("Implement immutable backups")
    if not assessment.get("patch_management", False):
        score += 20
        recommendations.append("Deploy patch management")
    if not assessment.get("incident_response_plan", False):
        score += 15
        recommendations.append("Create IR Plan")
    if not assessment.get("phishing_training", False):
        score += 10
        recommendations.append("Employee Awareness Training")

    score = min(score, 100)
    risk_category = categorize_risk(score)
    premium = calculate_premium(score)
    coverage_recommendations = recommend_coverage(risk_category)

    return {
        "risk_score": score,
        "risk_category": risk_category,
        "premium": premium,
        "recommendations": recommendations,
        "coverage_recommendations": coverage_recommendations,
    }


def categorize_risk(score: int) -> str:
    if score <= 25:
        return "Low"
    if score <= 50:
        return "Medium"
    if score <= 75:
        return "High"
    return "Critical"


def calculate_premium(risk_score: int) -> int:
    premium = BASE_PREMIUM + (risk_score * PREMIUM_MULTIPLIER)
    if risk_score >= 76:
        premium = int(premium * 1.3)
    elif risk_score <= 25:
        premium = int(premium * 0.9)
    return premium


def recommend_coverage(risk_category: str) -> list[str]:
    base_coverage = [
        "Cyber Liability",
        "Ransomware Coverage",
        "Business Interruption",
        "Data Recovery",
        "Incident Response",
        "Digital Forensics",
        "Third Party Liability",
        "PCI DSS Coverage",
    ]
    if risk_category in {"High", "Critical"}:
        base_coverage.append("Extended Vendor Risk Coverage")
    return base_coverage
