from app.agents.supplier_agent import analyze_supplier
from app.agents.risk_agent import calculate_risk
from app.agents.recommendation_agent import generate_recommendation


def evaluate_supplier(data):

    supplier = analyze_supplier(data)

    risk = calculate_risk(data)

    recommendation = generate_recommendation(
        risk["risk_score"]
    )

    return {
        **supplier,
        **risk,
        "recommendation": recommendation
    }