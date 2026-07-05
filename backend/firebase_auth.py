from firebase_admin import auth

from fastapi import HTTPException


def verify_google_token(id_token: str):

    try:

        decoded = auth.verify_id_token(
            id_token
        )

        return decoded

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Google token tidak valid"
        )