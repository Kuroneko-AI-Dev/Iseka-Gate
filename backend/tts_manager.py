import traceback

from gemini_tts import generate_tts as gemini_generate
from kokoro_tts import generate_kokoro_tts


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


        print("SWITCH TO KOKORO")


        audio = generate_kokoro_tts(
            text,
            voice="af_nicole"
        )


        return audio