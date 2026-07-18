import json

from gpt_service import ask_router


ROUTER_PROMPT = """

Jika ada kemungkinan informasi berubah seiring waktu, SELALU pilih research.
Kamu adalah AI Tool Router.

Tugasmu memilih apakah pertanyaan perlu mencari informasi terbaru dari internet.

Gunakan:

research
Jika pertanyaan membutuhkan informasi yang dapat berubah seiring waktu, seperti:
- berita terbaru
- harga saham
- harga crypto
- harga emas
- kurs mata uang
- cuaca
- skor pertandingan
- jadwal pertandingan
- hasil pertandingan
- jadwal film
- jadwal kereta
- jadwal pesawat
- informasi pemerintah terbaru
- nama presiden
- nama menteri
- pejabat negara
- kabinet
- kebijakan terbaru
- peraturan terbaru
- tanggal
- waktu sekarang
- data real-time
- informasi hari ini
- informasi terbaru
- cari di internet
- cek web
- search

chat
Jika pertanyaannya tidak membutuhkan internet, seperti:
- coding
- membuat program
- matematika
- penjelasan konsep
- cerita
- puisi
- roleplay
- identitas AI
- percakapan biasa
- opini
- brainstorming
- terjemahan

Jawab HANYA JSON.

Contoh:
{"tool":"research"}

atau

{"tool":"chat"}
"""


def choose_tool(message):

    messages = [

        {
            "role":"system",
            "content": ROUTER_PROMPT
        },

        {
            "role":"user",
            "content": message
        }

    ]


    result = ask_router(messages)

    print("======================")
    print("ROUTER RAW")
    print(result)
    print("======================")


    try:

        data = json.loads(result)

        return data


    except Exception:

        if "research" in result.lower():

            return {
                "tool":"research"
            }


        return {
            "tool":"chat"
        }