from sqlalchemy.orm import Session

from models import User
from security import hash_password
from security import verify_password


def register_user(
    db: Session,
    username,
    email,
    password
):

    user = User(

        username=username,

        email=email,

        password=hash_password(password)

    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def login_user(
    db: Session,
    email,
    password
):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.password
    ):
        return None

    return user

def google_user(
    db: Session,
    username,
    email,
    avatar=None
):

    user = db.query(User).filter(
        User.email == email
    ).first()


    # user sudah ada
    if user:

        if avatar and user.avatar != avatar:
            user.avatar = avatar

            db.commit()
            db.refresh(user)

        return user



    # user baru dari Google
    user = User(

        username=username,

        email=email,

        password=None,

        avatar=avatar

    )


    db.add(user)

    db.commit()

    db.refresh(user)


    return user