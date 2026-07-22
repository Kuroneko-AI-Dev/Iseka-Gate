import cv2
import numpy as np


class ImageUtils:

    @staticmethod
    async def read(upload_file):

        data = await upload_file.read()

        image = np.frombuffer(
            data,
            dtype=np.uint8
        )

        image = cv2.imdecode(
            image,
            cv2.IMREAD_COLOR
        )

        return image


    @staticmethod
    def resize(

        image,

        width=640

    ):

        h, w = image.shape[:2]

        scale = width / w

        new_h = int(h * scale)

        return cv2.resize(

            image,

            (width, new_h)

        )


    @staticmethod
    def rgb(image):

        return cv2.cvtColor(

            image,

            cv2.COLOR_BGR2RGB

        )


    @staticmethod
    def bgr(image):

        return cv2.cvtColor(

            image,

            cv2.COLOR_RGB2BGR

        )


    @staticmethod
    def crop(

        image,

        x1,

        y1,

        x2,

        y2

    ):

        return image[y1:y2, x1:x2]


    @staticmethod
    def encode(image):

        _, buffer = cv2.imencode(

            ".jpg",

            image

        )

        return buffer.tobytes()