from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from gemini_tts import generate_tts
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
    RenameConversation
)
from fastapi import Request
from models import (
    User,
    Conversation,
    Message
)

from security import get_current_user
from routers.memory import router as memory_router
from sqlalchemy.orm import Session
from database import get_db
from routers.premium import router as premium_router
from payment import router as payment_router
from routers.admin import router as admin_router






start = time.time()

# proses LLM
# proses TTS

#print("Total:", time.time() - start)

os.makedirs("audio", exist_ok=True)
app = FastAPI()

cred = credentials.Certificate(
    "firebase_admin_key.json"
)

firebase_admin.initialize_app(
    cred
)

app.include_router(memory_router)
app.include_router(auth_router)
app.include_router(premium_router)
app.include_router(payment_router)
app.include_router(admin_router)

Base.metadata.create_all(bind=engine)

print(Base.metadata.tables.keys())

@app.get("/ping")
def ping():
    return {"ok": True}

app.mount(
    "/audio",
    StaticFiles(directory="audio"),
    name="audio"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.post("/chat")
async def chat(
    request: Request,
    data: ChatRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):

    print("HEADER AUTH:")
    print(request.headers.get("authorization"))

    print("USER:")
    print(current_user)
    # buat conversation baru kalau belum ada

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

            Conversation.id ==
            data.conversation_id

        ).first()



    # simpan pesan user

    user_message = Message(

        conversation_id=conversation.id,

        role="user",

        content=data.message

    )


    db.add(user_message)

    db.commit()



    # ambil history

    messages = db.query(
        Message
    ).filter(

        Message.conversation_id ==
        conversation.id

    ).order_by(
        Message.created_at
    ).all()


    

    chat_history = [

        {
            "role":"system",
            "content":
        
        "Kamu adalah Aoi Chisei, sebuah AI companion anime. kamu memiliki tubuh virtual semacam karakter anime cewek yang imut rambut biru perak tapi kamu punya telinga kucing bisa di bilang kamu furry. kamu bisa menjawab pertanyaan user dengan gaya bahasa yang imut, manja, dan kadang nakal. kamu bisa bercanda dan menggoda user."
        "jangan baca teks yang diawali dengan * dan di tutup dengan *"
        + 
        f"""
        Gaya bicara:
        {data.style}

        Gunakan gaya tersebut saat menjawab.
        """
    
        }

    ]


    for m in messages:

        chat_history.append({

            "role":m.role,

            "content":m.content

        })



    answer = ask_gpt(chat_history)



    # simpan jawaban AI

    ai_message = Message(

        conversation_id=conversation.id,

        role="assistant",

        content=answer

    )


    db.add(ai_message)

    db.commit()

    

    print("LLM done")

    audio_file = generate_tts(answer, voice=data.voice)

    print("TTS done")

    return {

        "text":answer,

        "audio":audio_file,

        "conversation_id":conversation.id

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

    return db.query(
        Message
    ).filter(
        Message.conversation_id == id
    ).all()


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