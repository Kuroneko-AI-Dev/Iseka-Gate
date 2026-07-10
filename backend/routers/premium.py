from fastapi import APIRouter, Depends
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

    user = activate_premium(
        db,
        current_user,
        days=7
    )

    return {
        "message": "Premium berhasil diaktifkan.",
        "plan": user.plan,
        "premium_until": user.premium_until
    }


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