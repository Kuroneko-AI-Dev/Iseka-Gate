import traceback

from gemini_tts import generate_tts as gemini_generate
from super_tonic_tts import generate_supertonic_tts


def generate_tts(
    text,
    voice="Leda"
):

    try:

        audio = gemini_generate(
            text,
            voice
        )

        return audio

    except Exception as e:

        print("GEMINI FAILED")
        print(e)

        print("SWITCH TO SUPERTONIC")

        audio = generate_supertonic_tts(
            text,
            voice="F1"
        )

        return audio