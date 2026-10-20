from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from supertonic import TTS
import re
import uuid
import os
import traceback


app = FastAPI(title="Supertonic TTS")


AUDIO_DIR = "audio"
os.makedirs(AUDIO_DIR, exist_ok=True)


print("Loading Supertonic model...")

tts = TTS(auto_download=True)

print("Supertonic loaded!")


app.mount(
    "/audio",
    StaticFiles(directory=AUDIO_DIR),
    name="audio"
)



class TTSRequest(BaseModel):
    text: str
    voice: str = "F1"



@app.post("/tts")
async def generate(req: TTSRequest):

    try:

        style = tts.get_voice_style(
            req.voice
        )

        # =========================================
        # CLEAN TEXT UNTUK SUPERTONIC
        # =========================================

        text = req.text

        # Hapus Unicode Variation Selector
        text = text.replace("\ufe0f", "")

        # Hapus Zero Width Joiner
        text = text.replace("\u200d", "")

        print("TTS TEXT:", repr(text))

        # =========================================
        # SYNTHESIZE
        # =========================================

        wav, duration = tts.synthesize(
            text=text,
            lang="id",
            voice_style=style,
            speed=1.12,
        )

        filename = f"{uuid.uuid4().hex}.wav"

        path = os.path.join(
            AUDIO_DIR,
            filename
        )

        tts.save_audio(
            wav,
            path
        )

        print("WAV TYPE:", type(wav))
        print("DURATION TYPE:", type(duration))
        print("DURATION:", duration)

        return {
            "success": True,
            "audio": "/audio/" + filename,
            "duration": str(duration)
        }

    except Exception as e:

        traceback.print_exc()

        return {
            "success": False,
            "error": str(e)
        }