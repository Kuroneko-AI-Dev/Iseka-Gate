import requests
import os
from dotenv import load_dotenv

load_dotenv()


WHISPER_SERVER = os.getenv(
    "WHISPER_SERVER",
    "http://127.0.0.1:8178"
)


def transcribe_audio(audio_file):

    url = f"{WHISPER_SERVER}/inference"


    with open(audio_file, "rb") as f:

        files = {
            "file": (
                os.path.basename(audio_file),
                f,
                "audio/webm"
            )
        }


        data = {
            "language": "id",
            "response_format": "json",
            "temperature": "0.0"
        }


        response = requests.post(
            url,
            files=files,
            data=data,
            timeout=120
        )


    print("WHISPER STATUS:", response.status_code)
    print("WHISPER RESPONSE:", response.text)


    response.raise_for_status()


    result = response.json()


    return result.get("text", "")