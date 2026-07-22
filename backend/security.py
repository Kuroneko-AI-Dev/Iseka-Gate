from pwdlib import PasswordHash

from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
from jose import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from premium import check_premium_status
from database import get_db
from models import User


load_dotenv()


password_hash = PasswordHash.recommended()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db)
):
    try:
        if not SECRET_KEY:
            raise RuntimeError("SECRET_KEY belum dikonfigurasi")

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise ValueError("Token tidak memiliki subject")


    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Token tidak valid"
        )


    user = db.query(User).filter(
        User.id == int(user_id)
    ).first()


    if not user:

        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    if user.is_banned:
        raise HTTPException(status_code=403, detail="Akun ini telah diblokir")

    user = check_premium_status(
        db,
        user
    )

    return user


def hash_password(password: str):
    return password_hash.hash(password)



def verify_password(password: str, hashed: str):
    return password_hash.verify(
        password,
        hashed
    )



def create_access_token(data: dict):

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY belum dikonfigurasi")

    payload = data.copy()

    payload["exp"] = (
        datetime.utcnow()
        +
        timedelta(
            days=ACCESS_TOKEN_EXPIRE_DAYS
        )
    )


    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
