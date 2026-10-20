import os
import requests
from dotenv import load_dotenv

load_dotenv()


OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

OLLAMA_URL = "https://ollama.com/api/generate"

MODEL_NAME = "minimax-m3:cloud"


HEADERS = {
    "Authorization": f"Bearer {OLLAMA_API_KEY}",
    "Content-Type": "application/json"
}


def translate_jp_to_id(text):

    prompt = f"""
Terjemahkan teks bahasa Jepang berikut ke bahasa Indonesia.

ATURAN:
- Jangan menjawab sebagai karakter.
- Jangan membuat kalimat baru.
- Jangan menambah atau mengurangi isi.
- Hanya keluarkan hasil terjemahan.

Teks:
{text}
"""


    response = requests.post(

        OLLAMA_URL,

        headers=HEADERS,

        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        },

        timeout=300
    )


    response.raise_for_status()


    data = response.json()


    return data.get(
        "response",
        ""
    ).strip()