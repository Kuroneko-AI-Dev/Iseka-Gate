from pydantic import BaseModel, Field


class VisionResult(BaseModel):

    # Kamera yang digunakan
    camera: str

    # Jumlah wajah
    faces: int = 0

    # Object detection (YOLO)
    objects: list[dict] = Field(default_factory=list)

    # OCR
    text: str = ""

    # Caption utama
    caption: str = ""

    # Ringkasan scene
    scene: str = ""

    # Warna dominan (opsional)
    colors: list[str] = Field(default_factory=list)

    # Aktivitas yang terdeteksi
    actions: list[str] = Field(default_factory=list)

    # Ekspresi wajah
    emotions: list[str] = Field(default_factory=list)

    # Ringkasan visual siap dipakai LLM
    summary: str = ""

    # Auto comment
    comment: str = ""

    should_comment: bool = False