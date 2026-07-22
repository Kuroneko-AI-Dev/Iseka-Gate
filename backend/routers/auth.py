from fastapi import APIRouter, Depends, HTTPException

from fastapi import HTTPException
from schemas import GoogleLoginRequest

from firebase_auth import verify_google_token



from security import create_access_token
from sqlalchemy.orm import Session

from database import get_db
from models import User
from schemas import RegisterRequest
from schemas import LoginRequest

from auth import register_user
from auth import login_user
from auth import google_user

from security import (
    create_access_token,
    get_current_user
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    exist = db.query(User).filter(
        User.email == data.email
    ).first()

    if exist:
        raise HTTPException(
            status_code=400,
            detail="Email sudah digunakan."
        )


    user = register_user(
        db,
        data.username,
        data.email,
        data.password
    )


    return {
        "message": "Register berhasil.",
        "user_id": user.id
    }


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    user = login_user(
        db,
        data.email,
        data.password
    )


    if not user:
        raise HTTPException(
            status_code=401,
            detail="Email atau password salah."
        )


    token = create_access_token(
        {
            "sub": str(user.id)
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "plan": user.plan
    }


@router.post("/google")
def google_login(
    data: GoogleLoginRequest,
    db: Session = Depends(get_db)
):

    google_data = verify_google_token(
        data.id_token
    )


    email = google_data["email"]


    username = google_data.get(
        "name",
        email.split("@")[0]
    )


    avatar = google_data.get(
        "picture"
    )


    user = google_user(
        db,
        username,
        email,
        avatar
    )


    token = create_access_token(
        {
            "sub": str(user.id)
        }
    )


    return {
        "access_token": token,
        "token_type": "bearer",
        "username": user.username,
        "plan": user.plan,
        "avatar": user.avatar
    }

@router.get("/me")
def me(
    current_user=Depends(get_current_user)
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "plan": current_user.plan,
        "avatar": current_user.avatar,
        "is_admin": current_user.is_admin,
        "is_premium": current_user.is_premium,
        "is_banned": current_user.is_banned
    }

