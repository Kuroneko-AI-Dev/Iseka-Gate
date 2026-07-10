from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from models import User


def activate_premium(
    db: Session,
    user: User,
    days: int = 7
):
    user.plan = "PREMIUM"

    user.premium_until = (
        datetime.now(timezone.utc)
        + timedelta(days=days)
    )

    db.commit()
    db.refresh(user)

    return user


def check_premium_status(
    db: Session,
    user: User
):
    if user.premium_until is None:
        return user

    now = datetime.now(timezone.utc)

    if user.premium_until <= now:

        user.plan = "FREE"
        user.premium_until = None

        db.commit()
        db.refresh(user)

    return user


def premium_days_left(
    user: User
):
    if user.premium_until is None:
        return 0

    now = datetime.now(timezone.utc)

    if user.premium_until <= now:
        return 0

    delta = user.premium_until - now

    return delta.days + 1