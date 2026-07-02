from app.services.risk_engine import calculate_premium


def test_premium_calculation():
    assert calculate_premium(20) == 10000 + (20 * 150)  # base + risk score * 150
    assert calculate_premium(85) == 10000 + (85 * 150) + 0.3 * (85 * 150)
