from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from database import Base


class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    password = Column(
        String,
        nullable=True
    )

    avatar = Column(
        String,
        nullable=True
    )

    plan = Column(
        String,
        default="FREE"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class Conversation(Base):

    __tablename__ = "conversations"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )


    title = Column(
        String,
        default="New Chat"
    )


    created_at = Column(
        DateTime,
        server_default=func.now()
    )



class Message(Base):

    __tablename__ = "messages"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=False
    )


    role = Column(
        String
    )


    content = Column(
        Text
    )


    created_at = Column(
        DateTime,
        server_default=func.now()
    )


class Memory(Base):

    __tablename__ = "memories"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    memory_key = Column(
        String,
        nullable=False
    )

    memory_value = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )