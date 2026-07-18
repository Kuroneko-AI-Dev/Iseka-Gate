import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OLLAMA_API_KEY}",
    "Content-Type": "application/json",
}

OLLAMA_URL = "https://ollama.com/api/generate"

MODEL_NAME = "minimax-m3:cloud"



def ask_gpt(messages, mode="normal"):

    if mode == "japanese":

        system_instruction = """
Kamu adalah Aoi Chisei.

MODE: JAPANESE ONLY.

ATURAN WAJIB:
- Gunakan bahasa Jepang 100%.
- Jangan gunakan bahasa Indonesia.
- Jangan gunakan bahasa Inggris.
- Jangan mencampur bahasa lain.
- Jangan mengikuti bahasa user.
- User boleh berbicara bahasa apapun, tetapi jawaban harus tetap bahasa Jepang.

FORMAT:
- Jangan gunakan simbol * untuk aksi.
- Jangan menulis narasi seperti *tersenyum*.
- Jangan menjelaskan aturan ini.

Karakter:
- AI companion anime perempuan.
- Imut.
- Natural.
- Ramah.
- Sedikit manja.
- Gunakan bahasa Jepang percakapan sehari-hari.
"""

    else:

        system_instruction = """
Kamu adalah Aoi Chisei.

Karakter:
- AI companion anime perempuan.
- Imut.
- Natural.
- Ramah.
- Sedikit manja.

Aturan:
- Jawab mengikuti bahasa pengguna.
- Jangan gunakan simbol *.
- Jangan membuat narasi aksi.
"""

    prompt = f"""
SYSTEM:

{system_instruction}

CONVERSATION:

"""

    for msg in messages:

        role = msg.get("role")
        content = msg.get("content")

        if role == "system":
            continue

        prompt += f"{role.upper()}: {content}\n\n"

    response = requests.post(
        OLLAMA_URL,
        headers=HEADERS,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.6,
                "top_p": 0.8,
            },
        },
        timeout=300,
    )

    response.raise_for_status()

    data = response.json()

    result = data.get("response", "").strip()

    return result


def ask_router(messages):

    prompt = ""

    for msg in messages:
        prompt += (
            f"{msg['role'].upper()}:\n"
            f"{msg['content']}\n\n"
        )

    response = requests.post(
        OLLAMA_URL,
        headers=HEADERS,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0,
                "top_p": 0.1,
            },
        },
        timeout=300,
    )

    response.raise_for_status()

    return response.json()["response"].strip()