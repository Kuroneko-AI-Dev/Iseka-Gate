from pathlib import Path

import cv2
import torch

from PIL import Image

from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration,
)


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_DIR = BASE_DIR / "models" / "blip"



class BlipCaption:


    def __init__(self):

        self.processor = None
        self.model = None

        self.device = torch.device("cpu")



    def load(self):

        if self.model is not None:
            return


        print("Loading BLIP model...")


        self.processor = BlipProcessor.from_pretrained(
            str(MODEL_DIR)
        )


        self.model = (
            BlipForConditionalGeneration
            .from_pretrained(
                str(MODEL_DIR)
            )
            .to(self.device)
        )


        self.model.eval()


        print("BLIP loaded on CPU")



    def generate(
        self,
        image,
        detailed=True
    ):

        self.load()


        rgb = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2RGB
        )


        pil = Image.fromarray(
            rgb
        ).convert("RGB")


        pil.thumbnail(
            (768,768)
        )


        # PENTING:
        # BLIP base captioning jangan diberi text prompt

        inputs = self.processor(
            images=pil,
            return_tensors="pt"
        )


        inputs = {
            k:v.to(self.device)
            for k,v in inputs.items()
        }



        with torch.inference_mode():

            output = self.model.generate(

                **inputs,

                max_new_tokens=80,

                min_new_tokens=5,

                num_beams=3,

                repetition_penalty=1.2

            )



        caption = self.processor.decode(
            output[0],
            skip_special_tokens=True
        ).strip()



        print("========================")
        print("BLIP CAPTION:")
        print(caption)
        print("========================")


        return caption