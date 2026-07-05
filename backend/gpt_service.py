import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "minimax-m3:cloud"


def ask_gpt(messages):
    prompt = ""

    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"

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

    data = response.json()

    return data.get("response", "")