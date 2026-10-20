import requests
import shutil
import uuid
import os

from dotenv import load_dotenv
from voice_filter import apply_voice_filter

load_dotenv()


SUPER_TONIC_URL = os.getenv(
    "SUPER_TONIC",
    "http://127.0.0.1:9000"
)

os.makedirs("audio", exist_ok=True)


def generate_supertonic_tts(
    text,
    voice="F1"
):

    print("=== SUPER_TONIC TTS ===")
    print("VOICE =", voice)
    print(text[:100])

    response = requests.post(
        f"{SUPER_TONIC_URL}/tts",
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
            SUPER_TONIC_URL + "/"
            + source.lstrip("/").replace("\\", "/")
        )

    # ========================================
    # DOWNLOAD ORIGINAL AUDIO
    # ========================================

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

    print(
        "SUPER_TONIC SAVED =",
        filename
    )

    # ========================================
    # VOICE FILTER
    # ========================================

    filtered_filename = (
        f"{uuid.uuid4().hex}_filtered.wav"
    )

    filtered_destination = os.path.join(
        "audio",
        filtered_filename
    )

    apply_voice_filter(
        destination,
        filtered_destination,
        preset="normal"
    )

    print(
        "SUPER_TONIC FILTERED =",
        filtered_filename
    )

    # ========================================
    # RETURN FILTERED AUDIO
    # ========================================

    return f"audio/{filtered_filename}"