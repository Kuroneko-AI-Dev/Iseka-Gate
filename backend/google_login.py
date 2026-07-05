from google.oauth2 import id_token
from google.auth.transport import requests

from fastapi import HTTPException


def verify_google_token(
    token: str,
    client_id: str
):

    try:

        user = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            client_id
        )

        return user

    except Exception:

        raise HTTPException(
            status_code=401,
            detail="Google token tidak valid."
        )