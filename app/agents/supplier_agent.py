def analyze_supplier(data):

    score = 100

    score -= (5 - data.rating) * 10
    score -= data.delivery_delay

    score = max(0, min(100, score))

    return {
        "supplier": data.name,
        "supplier_score": round(score, 2)
    }