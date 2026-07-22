from pydantic import BaseModel, Field


class VisionResult(BaseModel):

    camera: str

    faces: int = 0

    objects: list[dict] = Field(default_factory=list)

    caption: str = ""

    text: str = ""

    comment: str = ""

    should_comment: bool = False