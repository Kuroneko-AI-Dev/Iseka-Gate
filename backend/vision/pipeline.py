from .schemas import VisionResult
from .state import VisionState
from .caption import BlipCaption
from .utils import ImageUtils

from .detectors import (
    FaceDetector,
    YoloDetector,
    OCRDetector,
)


class VisionPipeline:

    def __init__(self):

        self.state = VisionState()

        self.face = FaceDetector()
        self.yolo = YoloDetector()
        self.ocr = OCRDetector()
        self.blip = BlipCaption()

    async def process(
        self,
        image,
        camera,
        mode="all"
    ):

        image = await ImageUtils.read(image)
        image = ImageUtils.resize(image)

        faces = []
        objects = []
        texts = []
        caption = ""

        # Kamera depan
        if camera == "user":

            faces = self.run_face(image)

        # Preview kamera belakang
        elif mode == "preview":

            pass

        # Deteksi objek
        elif mode == "vision":

            objects = self.run_yolo(image)

            caption = self.run_blip(image)

        # OCR saja
        elif mode == "ocr":

            texts = self.run_ocr(image)

        # Vision lengkap
        elif mode == "all":

            objects = self.run_yolo(image)

            texts = self.run_ocr(image)

            caption = self.run_blip(image)


            self.state.update(
                camera=camera,
                objects=objects,
                caption=caption,
                text="\n".join(
                    item["text"]
                    for item in texts
                )
            )

        return self.build_result(

            camera,

            faces,

            objects,

            texts,

            caption

        )

    def run_face(
        self,
        image
    ):

        return self.face.detect(image)

    def run_yolo(
        self,
        image
    ):

        return self.yolo.detect(image)

    def run_ocr(
        self,
        image
    ):

        return self.ocr.detect(image)

    def run_blip(
        self,
        image
    ):

        return self.blip.generate(image)

    def build_result(
        self,
        camera,
        faces,
        objects,
        texts,
        caption
    ):

        return VisionResult(

            camera=camera,

            faces=len(faces),

            objects=objects,

            caption=caption,

            text="\n".join(
                item["text"]
                for item in texts
            ),

            comment="",

            should_comment=False

        )