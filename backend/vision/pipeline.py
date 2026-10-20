import asyncio

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
        caption = "No visual description."

        # Kamera depan
        if camera == "user":

            faces = await asyncio.to_thread(
                self.run_face,
                image
            )

        # Preview kamera belakang
        elif mode == "preview":

            pass

        # Vision saja
        elif mode == "vision":

            objects, caption = await asyncio.gather(

                asyncio.to_thread(
                    self.run_yolo,
                    image
                ),

                asyncio.to_thread(
                    self.run_blip,
                    image
                )

            )

            objects = self.unique_objects(objects)

        # OCR saja
        elif mode == "ocr":

            texts = await asyncio.to_thread(
                self.run_ocr,
                image
            )

            texts = self.clean_texts(texts)

        # Vision lengkap
        elif mode == "all":

            objects, texts, caption = await asyncio.gather(

                asyncio.to_thread(
                    self.run_yolo,
                    image
                ),

                asyncio.to_thread(
                    self.run_ocr,
                    image
                ),

                asyncio.to_thread(
                    self.run_blip,
                    image
                )

            )

            objects = self.unique_objects(objects)
            texts = self.clean_texts(texts)

            scene = self.build_scene_summary(
                caption,
                objects,
                texts
            )

            self.state.update(

                camera=camera,

                objects=objects,

                caption=caption,

                text="\n".join(scene["text"])

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

        result = self.yolo.detect(image)

        print("=== YOLO OUTPUT ===")
        print(result)
        print("===================")

        return result

        

    def run_ocr(
        self,
        image
    ):

        return self.ocr.detect(image)

    def run_blip(
        self,
        image
    ):

        return self.blip.generate(
            image,
            detailed=True
        )

    def clean_texts(
        self,
        texts
    ):

        result = []

        for item in texts:

            text = item["text"].strip()

            if len(text) < 2:
                continue

            result.append(item)

        return result
    
   # file: vision/pipeline.py

    def unique_objects(
        self,
        objects
    ):

        unique = []

        seen = set()


        for obj in objects:

            if not isinstance(obj, dict):
                continue


            label = (
                obj.get("label")
                or obj.get("name")
            )


            if not label:
                continue


            if label not in seen:

                seen.add(label)

                obj["label"] = label

                unique.append(obj)


        return unique
    def build_scene_summary(
        self,
        caption,
        objects,
        texts
    ):

        return {

            "caption": caption,

            "objects": [

                obj["label"]

                for obj in objects

            ],

            "text": [

                item["text"]

                for item in texts

            ],

            "object_count": len(objects),

            "text_count": len(texts)

        }

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