from google import genai
from dotenv import load_dotenv

import wave
import base64
import os
import uuid

load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)



def generate_tts(text, voice="Leda"):

    print("=== GENERATE TTS ===")
    print("VOICE =", voice)

    os.makedirs("audio", exist_ok=True)


    for file in os.listdir("audio"):
        if file.endswith(".wav"):
            os.remove(os.path.join("audio", file))


    print("SEND TO GEMINI")


    interaction = client.interactions.create(
        model="gemini-2.5-flash-preview-tts",

        input=text,

        response_format={
            "type": "audio"
        },

        generation_config={
            "speech_config": [
                {
                    "voice": voice
                }
            ]
        }
    )


    print("RESPONSE RECEIVED")


    filename = f"audio/{uuid.uuid4().hex}.wav"


    wave_file(
        filename,
        base64.b64decode(
            interaction.output_audio.data
        )
    )


    print("SAVE OK")


    return filename