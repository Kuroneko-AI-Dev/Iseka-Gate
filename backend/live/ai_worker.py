import asyncio

from .queue import get_comment
from .websocket import broadcast

from gpt_service import ask_gpt
from tts_manager import generate_kokoro_tts



async def start_ai_worker():


    print("LIVE AI WORKER STARTED")



    while True:


        comment = await get_comment()



        print(
            "PROCESS TIKTOK COMMENT:",
            comment
        )



        chat_history = [

            {

                "role":"system",

                "content":

                """
                Kamu adalah Aoi Chisei,
                sebuah AI companion anime.

                Kamu memiliki tubuh virtual
                karakter anime cewek imut
                rambut biru perak dan telinga kucing.

                Gaya bicara:
                imut, manja, kadang nakal,
                seperti sedang live streaming.

                Jawab komentar TikTok
                dengan singkat dan natural.

                Jangan terlalu panjang.
                """

            },


            {

                "role":"user",

                "content":

                f"""
                {comment['user']} berkata:

                {comment['comment']}
                """

            }

        ]




        try:



            answer = await asyncio.to_thread(

                ask_gpt,

                chat_history

            )



            print(
                "AI RESPONSE:",
                answer
            )



            audio = await asyncio.to_thread(

             generate_kokoro_tts,

                answer

            )




            await broadcast({

                "type":"ai_reply",

                "user":"Aoi Chisei",

                "message":answer,

                "audio":audio

            })





        except Exception as e:


            print(
                "LIVE AI ERROR:",
                e
            )