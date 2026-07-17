from fastapi import FastAPI
from app.models.supplier import Supplier
from app.services.procurement_service import evaluate_supplier

app = FastAPI(
    title="AI Procurement Intelligence"
)


@app.get("/")
def home():

    return {
        "message": "AI Procurement Intelligence Running"
    }


@app.post("/evaluate")
def evaluate(data: Supplier):

    return evaluate_supplier(data)