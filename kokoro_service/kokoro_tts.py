import os
import uuid

import soundfile as sf

from kokoro import KPipeline
import numpy as np

# ==========================================================
# LOAD MODEL SATU KALI SAJA
# ==========================================================

pipeline = KPipeline(
    lang_code="a",
    repo_id="hexgrad/Kokoro-82M"
)

print("KOKORO MODEL LOADED")


# ==========================================================
# GENERATE TTS
# ==========================================================

def generate_tts(
    text: str,
    voice: str = "af_heart"
):

    print("=== KOKORO TTS ===")

    os.makedirs("audio", exist_ok=True)

    generator = pipeline(
        text,
        voice=voice,
        split_pattern=r"[.!?]\s+"
    )

    import numpy as np

    audio_chunks = []

    for result in generator:
        audio_chunks.append(
            result.output.audio.cpu().numpy()
        )

    audio = np.concatenate(audio_chunks)

    filename = f"audio/{uuid.uuid4().hex}.wav"

    sf.write(
        filename,
        audio,
        24000
    )

    print("SAVE :", filename)

    return filename