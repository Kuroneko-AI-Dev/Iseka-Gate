from pydantic import BaseModel, Field

from pydantic import BaseModel



class VisionObject(BaseModel):
    name: str
    confidence: float
    box: list[int]


class VisionData(BaseModel):

    camera: str

    faces: int = 0

    objects: list[VisionObject] = []

    caption: str = ""

    text: str = ""

    should_comment: bool = False


class ChatRequest(BaseModel):

    message: str

    conversation_id: int | None = None

    voice: str = "Leda"

    style: str | None = ""

    vision: VisionData | None = None
    
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


class LiveConnectRequest(BaseModel):
    username: str


class ResearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)
    max_results: int = Field(default=5, ge=1, le=5)
