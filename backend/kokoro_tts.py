import requests
import shutil
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


KOKORO_URL = os.getenv(
    "KOKORO_SERVER",
    "http://127.0.0.1:9000"
)

os.makedirs("audio", exist_ok=True)


def generate_kokoro_tts(
    text,
    voice="af_nicole"
):

    print("=== KOKORO TTS ===")
    print("VOICE =", voice)
    print(text[:100])


    response = requests.post(
        f"{KOKORO_URL}/tts",
        json={
            "text": text,
            "voice": voice
        },
        timeout=120
    )


    response.raise_for_status()


    data = response.json()


    source = data["audio"]


    if not source.startswith("http"):

          source = (
            KOKORO_URL + "/"
            + source.lstrip("/").replace("\\", "/")
        )

    filename = f"{uuid.uuid4().hex}.wav"


    destination = os.path.join(
        "audio",
        filename
    )


    with requests.get(
        source,
        stream=True
    ) as r:

        r.raise_for_status()

        with open(
            destination,
            "wb"
        ) as f:

            shutil.copyfileobj(
                r.raw,
                f
            )


    print("KOKORO SAVED =", filename)


    return f"audio/{filename}"