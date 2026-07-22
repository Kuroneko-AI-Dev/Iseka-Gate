import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "minimax-m3:cloud"


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
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=300
    )

    response.raise_for_status()

    return response.json()["response"].strip()