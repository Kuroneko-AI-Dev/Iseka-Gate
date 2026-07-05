from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = "ISI_NANTI"


def verify_google_token(token: str):

    user = id_token.verify_oauth2_token(
        token,
        requests.Request(),
        GOOGLE_CLIENT_ID
    )

    return user