from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from security import get_current_user
from premium import (
    activate_premium,
    check_premium_status,
    premium_days_left
)

router = APIRouter(
    prefix="/premium",
    tags=["Premium"]
)


@router.post("/activate")
def activate(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    raise HTTPException(
        status_code=403,
        detail="Premium hanya dapat diaktifkan setelah pembayaran terverifikasi."
    )


@router.get("/status")
def status(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    user = check_premium_status(
        db,
        current_user
    )

    return {
        "plan": user.plan,
        "premium_until": user.premium_until,
        "days_left": premium_days_left(user)
    }
