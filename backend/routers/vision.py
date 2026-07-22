from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form

from vision import VisionService

router = APIRouter(
    prefix="/vision",
    tags=["Vision"]
)

vision = VisionService()


@router.post("/analyze")
async def analyze(

    image: UploadFile = File(...),

    camera: str = Form(...),

    mode: str = Form("preview")

):

    return await vision.analyze(

        image=image,

        camera=camera,

        mode=mode

    )