from pydantic import BaseModel

from pydantic import BaseModel


class ChatRequest(BaseModel):

    message: str

    conversation_id: int | None = None

    voice: str = "Leda"

    style: str | None = ""
    
class RegisterRequest(BaseModel):

    username: str
    email: str
    password: str


class LoginRequest(BaseModel):

    email: str
    password: str

class GoogleLoginRequest(BaseModel):
    id_token: str


class RenameConversation(BaseModel):
    title: str


class MemoryCreate(BaseModel):
    memory_key: str
    memory_value: str


class MemoryUpdate(BaseModel):
    memory_key: str
    memory_value: str