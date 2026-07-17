def calculate_risk(data):

    risk = 0

    if data.rating < 3:
        risk += 40

    if data.delivery_delay > 20:
        risk += 40

    if data.delivery_delay > 50:
        risk += 20

    risk = min(risk, 100)

    if risk < 30:
        category = "Low Risk"
    elif risk < 70:
        category = "Medium Risk"
    else:
        category = "High Risk"

    return {
        "risk_score": risk,
        "risk_category": category
    }