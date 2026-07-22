from fastapi import APIRouter, Depends
from pydantic import BaseModel
from security import get_current_user

router = APIRouter(prefix="/payment", tags=["Payment"])


class PaymentRequest(BaseModel):
    plan: str


@router.post("/create")
def create_payment(
    data: PaymentRequest,
    current_user=Depends(get_current_user)
):

    return {
        "message": "Payment endpoint ready",
        "plan": data.plan
    }
