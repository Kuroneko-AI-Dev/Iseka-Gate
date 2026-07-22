from pathlib import Path

from PIL import Image

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "models" / "blip"


class BlipCaption:

    def __init__(self):

        self.processor = None
        self.model = None


    def load(self):

        if self.model is None:

            self.processor = BlipProcessor.from_pretrained(
                str(MODEL_DIR)
            )

            self.model = BlipForConditionalGeneration.from_pretrained(
                str(MODEL_DIR)
            )


    def generate(
        self,
        image
    ):

        self.load()

        pil = Image.fromarray(image)

        inputs = self.processor(
            images=pil,
            return_tensors="pt"
        )

        output = self.model.generate(
            **inputs,
            max_new_tokens=40
        )

        caption = self.processor.decode(
            output[0],
            skip_special_tokens=True
        )

        return caption