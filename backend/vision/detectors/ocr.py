from pathlib import Path

import easyocr


BASE_DIR = Path(__file__).resolve().parents[2]


MODEL_DIR = BASE_DIR / "models" / "easyocr"


class OCRDetector:

    def __init__(self):

        self.reader = None


    def load(self):

        if self.reader is None:

            self.reader = easyocr.Reader(

                ["en", "id"],

                gpu=False,

                model_storage_directory=str(MODEL_DIR)

            )


    def detect(

        self,

        image

    ):

        self.load()

        result = self.reader.readtext(image)

        texts = []

        for item in result:

            texts.append({

                "text": item[1],

                "confidence": float(item[2])

            })

        return texts