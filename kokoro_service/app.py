from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from kokoro_tts import generate_tts

app = FastAPI(
    title="Kokoro TTS Server",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folder audio
os.makedirs("audio", exist_ok=True)

app.mount(
    "/audio",
    StaticFiles(directory="audio"),
    name="audio"
)


class TTSRequest(BaseModel):
    text: str
    voice: str = "af_nicole"


@app.get("/ping")
def ping():
    return {
        "status": "ok"
    }


@app.post("/tts")
def tts(data: TTSRequest):

    filename = generate_tts(
        text=data.text,
        voice=data.voice
    )

    return {
        "audio": filename
    }