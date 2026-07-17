def generate_recommendation(risk_score):

    if risk_score < 30:
        return "Approved Vendor"

    if risk_score < 70:
        return "Needs Further Review"

    return "Avoid Supplier"