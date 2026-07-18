import subprocess
import uuid


def convert_to_wav(input_file):

    output_file = f"audio/{uuid.uuid4().hex}.wav"


    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            input_file,
            "-ar",
            "16000",
            "-ac",
            "1",
            output_file
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


    return output_file