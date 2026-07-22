from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import User
from fastapi import HTTPException
from models import User, Conversation, Message
from sqlalchemy import func
from datetime import date
from security import get_current_user

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def get_current_admin(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Admin only"
        )

    return current_user

@router.get("/users")
def get_users(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin,
            "is_premium": user.is_premium,
            "is_banned": user.is_banned,
            "created_at": user.created_at
        }
        for user in users
    ]

@router.patch("/user/{user_id}/premium")
def set_premium(
    user_id: int,
    is_premium: bool,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    user.is_premium = is_premium

    db.commit()
    db.refresh(user)

    return {
        "message": "Status premium berhasil diubah",
        "username": user.username,
        "is_premium": user.is_premium
    }

@router.patch("/user/{user_id}/ban")
def set_ban(
    user_id: int,
    is_banned: bool,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    user.is_banned = is_banned

    db.commit()
    db.refresh(user)

    return {
        "message": "Status user berhasil diubah",
        "username": user.username,
        "is_banned": user.is_banned
    }

@router.delete("/user/{user_id}")
def delete_user(
    user_id: int,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User tidak ditemukan")

    conversations = db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).all()

    for conv in conversations:

        db.query(Message).filter(
            Message.conversation_id == conv.id
        ).delete()

    db.query(Conversation).filter(
        Conversation.user_id == user_id
    ).delete()

    db.delete(user)

    db.commit()

    return {"message": "User berhasil dihapus"}

@router.get("/stats")
def get_stats(
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):

    total_users = db.query(User).count()

    premium_users = db.query(User).filter(
        User.is_premium == True
    ).count()

    banned_users = db.query(User).filter(
        User.is_banned == True
    ).count()

    today_users = db.query(User).filter(
        func.date(User.created_at) == date.today()
    ).count()

    return {
        "total_users": total_users,
        "premium_users": premium_users,
        "banned_users": banned_users,
        "today_users": today_users
    }
