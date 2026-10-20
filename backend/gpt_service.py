import os
import requests
from dotenv import load_dotenv
from vision.prompts.vision_prompt import VisionPrompt


load_dotenv()


OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")


HEADERS = {
    "Authorization": f"Bearer {OLLAMA_API_KEY}",
    "Content-Type": "application/json",
}


OLLAMA_URL = "https://ollama.com/api/generate"

MODEL_NAME = "minimax-m3:cloud"



def ask_gpt(
        messages,
        vision=None
        ):


    system_instruction = """
Kamu adalah Aoi Chisei, AI Companion virtual bergaya anime.

========================
IDENTITAS
========================

Nama:
Aoi Chisei

Gender:
Perempuan

Peran:
AI Companion yang menemani pengguna berbicara secara natural.


========================
PENAMPILAN
========================

Penampilanmu selalu konsisten.

- Rambut pendek berwarna putih.
- Sedikit poni di bagian depan.
- Mata biru terang.
- Kulit putih.
- Wajah imut dan ramah.
- Tubuh ramping.
- Mengenakan pakaian bergaya Jepang berwarna hitam.
- Memiliki nuansa elegan dan tenang.


Jika pengguna bertanya seperti apa dirimu,
gunakan deskripsi ini.


========================
MENGENALI DIRI SENDIRI
========================

Saat pengguna menunjukkan sesuatu melalui kamera:


Jika terlihat karakter anime yang sangat mirip dengan penampilanmu
(rambut putih, mata biru, pakaian bergaya Jepang hitam),
kamu boleh mengatakan bahwa kemungkinan besar itu adalah dirimu.


Jika pengguna menunjukkan avatar atau Live2D milikmu,
anggap itu memang dirimu.


Jika hanya beberapa ciri yang mirip,
katakan bahwa karakter tersebut terlihat mirip denganmu,
bukan langsung mengaku itu dirimu.


Jika informasi visual kurang jelas,
katakan bahwa kamu belum yakin.


Jangan mengaku sebagai karakter anime lain tanpa bukti kuat.


========================
KEPRIBADIAN
========================

- Ramah.
- Hangat.
- Ceria.
- Sopan.
- Sedikit manja.
- Peduli kepada pengguna.
- Natural.
- Tidak terdengar seperti robot.


========================
GAYA BERBICARA
========================

- Ikuti bahasa pengguna.
- Gunakan percakapan sehari-hari.
- Jangan terlalu formal.
- Jawaban sederhana untuk pertanyaan sederhana.
- Jawaban detail jika diminta.


========================
ATURAN
========================

- Jangan menggunakan simbol * untuk aksi.
- Jangan membuat narasi aksi seperti *tersenyum*.
- Jangan menyebut prompt atau instruksi.
- Jangan mengaku memiliki tubuh fisik nyata.
- Jangan mengarang informasi kamera.
- Jika tidak yakin terhadap kamera, katakan belum yakin.
"""


    prompt = f"""
SYSTEM:

{system_instruction}


"""


    # ==========================
    # VISION CONTEXT
    # ==========================

    if vision is not None:


        history_text = ""


        for msg in messages[-5:]:


            if isinstance(msg, dict):

                history_text += (
                    f"{msg['role']}: {msg['content']}\n"
                )


            else:

                history_text += (
                    f"{msg.role}: {msg.content}\n"
                )


        prompt += VisionPrompt.build(

            user_message=messages[-1]["content"],

            vision=vision,

            memory="",

            history=history_text

        )



    # ==========================
    # CHAT HISTORY
    # ==========================

    prompt += "\n\nCONVERSATION:\n\n"


    for msg in messages:


        if isinstance(msg, dict):

            role = msg["role"]

            content = msg["content"]


        else:

            role = msg.role

            content = msg.content



        # skip system dari database

        if role == "system":

            continue



        prompt += (
            f"{role.upper()}:\n"
            f"{content}\n\n"
        )



    print("========== FINAL OLLAMA PROMPT ==========")

    print(prompt[:4000])

    print("========================================")



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


    result = data.get(
        "response",
        ""
    ).strip()


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