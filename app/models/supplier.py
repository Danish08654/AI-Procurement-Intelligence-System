from pydantic import BaseModel, Field


class Supplier(BaseModel):
    name: str = Field(..., min_length=2)
    rating: float = Field(..., ge=0, le=5)
    delivery_delay: float = Field(..., ge=0, le=100)
    country: str