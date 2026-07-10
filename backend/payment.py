from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/payment", tags=["Payment"])


class PaymentRequest(BaseModel):
    plan: str


@router.post("/create")
def create_payment(data: PaymentRequest):

    return {
        "message": "Payment endpoint ready",
        "plan": data.plan
    }