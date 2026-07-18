from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from tts_manager import generate_tts
from gpt_service import ask_gpt
from fastapi.staticfiles import StaticFiles
import os
from routers.auth import router as auth_router
from database import engine
from models import Base
import time
import firebase_admin
from firebase_admin import credentials
from schemas import (
    ChatRequest,
    RenameConversation,
    ResearchRequest,
)
from fastapi import Request
from models import (
    User,
    Conversation,
    Message
)
from routers.live import router as live_router
from security import get_current_user
from routers.memory import router as memory_router
from sqlalchemy.orm import Session
from database import get_db
from routers.premium import router as premium_router
from payment import router as payment_router
from routers.admin import router as admin_router
import asyncio
from pydantic import BaseModel
from live.ai_worker import start_ai_worker
from translator import translate_jp_to_id
from kokoro_tts import generate_kokoro_tts
from tools.research import research
from tool_router import choose_tool
from tool_manager import run_tool
from dotenv import load_dotenv
from routers.stt import router as stt_router

load_dotenv()


start = time.time()

# proses LLM
# proses TTS

#print("Total:", time.time() - start)

os.makedirs("audio", exist_ok=True)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://192.168.1.3:5173",
        "https://isekaiport.pages.dev",
        "https://ministers-boards-row-releases.trycloudflare.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/audio",
    StaticFiles(directory="audio"),
    name="audio"
)



if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_admin_key.json")
    firebase_admin.initialize_app(cred)

app.include_router(memory_router)
app.include_router(auth_router)
app.include_router(premium_router)
app.include_router(payment_router)
app.include_router(admin_router)
app.include_router(live_router)
app.include_router(stt_router)


#Base.metadata.create_all(bind=engine)

print(Base.metadata.tables.keys())



class TranslateRequest(BaseModel):
    text:str





@app.post("/translate")
async def translate_text(
    data: TranslateRequest,
    current_user=Depends(get_current_user)
):

    result = translate_jp_to_id(data.text)

    return {
        "translation": result
    }


@app.post("/research")
def web_research(
    data: ResearchRequest,
    current_user=Depends(get_current_user),
):
    return research(
        query=data.query,
        user_id=current_user.id,
        max_results=data.max_results,
    )


@app.on_event("startup")
async def startup():

    asyncio.create_task(
        start_ai_worker()
    )

@app.get("/ping")
def ping():
    return {"ok": True}



@app.post("/chat")
async def chat(
    request: Request,
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    # ============================
    # Conversation
    # ============================

    if data.conversation_id is None:

        conversation = Conversation(
            user_id=current_user.id,
            title=data.message[:30]
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    else:

        conversation = db.query(
            Conversation
        ).filter(
            Conversation.id == data.conversation_id,
            Conversation.user_id == current_user.id
        ).first()

        if not conversation:
            raise HTTPException(
                status_code=404,
                detail="Conversation not found"
            )

    # ============================
    # Simpan pesan user
    # ============================

    user_message = Message(
        conversation_id=conversation.id,
        role="user",
        content=data.message
    )

    db.add(user_message)
    db.commit()

    # ============================
    # Ambil history
    # ============================

    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.created_at)
        .all()
    )

    chat_history = [
        {
            "role": "system",
            "content":
                "Kamu adalah Aoi Chisei, sebuah AI companion anime. "
                "kamu memiliki tubuh virtual semacam karakter anime cewek yang imut rambut biru perak "
                "tapi kamu punya telinga kucing bisa di bilang kamu furry. "
                "kamu bisa menjawab pertanyaan user dengan gaya bahasa yang imut, manja, dan kadang nakal. "
                "kamu bisa bercanda dan menggoda user."
                "jangan baca teks yang diawali dengan * dan di tutup dengan *"
                + f"""

Gaya bicara:
{data.style}

Gunakan gaya tersebut saat menjawab.
"""
        }
    ]

    for m in messages:
        chat_history.append({
            "role": m.role,
            "content": m.content
        })

    print("LLM done")

    tts_mode = "auto"
    tts_notice = None
    tts_provider = None

    # ============================
    # Tool Router
    # ============================

    print("=== GEMINI MODE ===")

    result = None

    tool = choose_tool(data.message)

    print("=" * 40)
    print("TOOL DIPILIH :", tool)
    print("=" * 40)

    if tool["tool"] == "research":

        print("========== ROUTER DEBUG ==========")
        print("TOOL VALUE:", tool)
        print("TOOL TYPE:", type(tool))
        print("==================================")

        result = run_tool(
            tool,
            current_user.id,
            data.message
        )

        print("=" * 40)
        print("HASIL RESEARCH")
        print(result)
        print("=" * 40)

        if result:

            sources = result.get("sources", [])

            if sources:

                source_text = ""

                for index, source in enumerate(sources, start=1):

                    source_text += (
                        f"[{index}] {source['title']}\n"
                        f"URL: {source['url']}\n"
                        f"Isi: {source['snippet']}\n\n"
                    )

                chat_history.append({
                    "role": "user",
                    "content": f"""
Gunakan informasi hasil pencarian web berikut untuk menjawab.

{source_text}

Jangan mengarang informasi.
Jika sumber tidak cukup, katakan dengan jujur.
Sebutkan sumber bila memungkinkan.
"""
                })

    # ============================
    # LLM
    # ============================

    answer = ask_gpt(
        chat_history,
        mode="normal"
    )

    # ============================
    # TTS
    # ============================

    try:

        audio_file = generate_tts(
            answer,
            voice=data.voice
        )

        print("GEMINI SUCCESS")
        print("AUDIO =", audio_file)

        tts_provider = "gemini"

    except Exception as e:

        print("GEMINI FAILED")
        print(e)

        print("=== SWITCH TO KOKORO ===")

        tts_mode = "kokoro"
        tts_provider = "kokoro"

        audio_file = generate_kokoro_tts(answer)

    # ============================
    # Simpan jawaban AI
    # ============================

    ai_message = Message(
        conversation_id=conversation.id,
        role="assistant",
        content=answer
    )

    db.add(ai_message)
    db.commit()

    print("FINAL RESPONSE")
    print("TEXT =", answer)
    print("AUDIO =", audio_file)
    print("PROVIDER =", tts_provider)

    return {
        "text": answer,
        "audio": audio_file,
        "conversation_id": conversation.id,
        "tts_mode": tts_mode,
        "tts_provider": tts_provider,
        "tts_notice": tts_notice
    }


@app.get("/conversations")
def get_conversations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    conversations = db.query(
        Conversation
    ).filter(
        Conversation.user_id == current_user.id
    ).order_by(
        Conversation.created_at.desc()
    ).all()


    return conversations



@app.get("/conversations/{id}")
def get_messages(
    id:int,
    db:Session=Depends(get_db),
    current_user=Depends(get_current_user)
):

    conversation = db.query(Conversation).filter(
        Conversation.id == id,
        Conversation.user_id == current_user.id
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return db.query(Message).filter(Message.conversation_id == id).all()


@app.put("/conversations/{id}")
def rename_conversation(

    id:int,

    data:RenameConversation,

    db:Session=Depends(get_db),

    current_user=Depends(get_current_user)

):

    conversation = db.query(
        Conversation
    ).filter(

        Conversation.id == id,

        Conversation.user_id == current_user.id

    ).first()


    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    conversation.title = data.title

    db.commit()

    db.refresh(conversation)

    return conversation


@app.delete("/conversations/{id}")
def delete_conversation(

    id:int,

    db:Session=Depends(get_db),

    current_user=Depends(get_current_user)

):

    conversation = db.query(
        Conversation
    ).filter(

        Conversation.id == id,

        Conversation.user_id == current_user.id

    ).first()


    if not conversation:

        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )


    db.query(
        Message
    ).filter(

        Message.conversation_id == id

    ).delete()


    db.delete(conversation)

    db.commit()


    return {

        "success":True

    }

print("==== BACKEND INI YANG KEJALAN ====")
