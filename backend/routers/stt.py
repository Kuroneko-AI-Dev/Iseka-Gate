from fastapi import APIRouter, UploadFile, File, Depends
from security import get_current_user
from stt_service import transcribe_audio
import os
import uuid
from audio_converter import convert_to_wav

router = APIRouter(
    prefix="/stt",
    tags=["STT"]
)


os.makedirs(
    "audio/uploads",
    exist_ok=True
)


@router.post("")
async def speech_to_text(
    file: UploadFile = File(...),
    current_user = Depends(get_current_user)
):

    filename = (
        f"audio/uploads/{uuid.uuid4().hex}.wav"
    )

    with open(filename, "wb") as f:
        f.write(
            await file.read()
        )


    wav_file = convert_to_wav(filename)

    text = transcribe_audio(wav_file)


    os.remove(filename)


    return {
        "text": text
    }