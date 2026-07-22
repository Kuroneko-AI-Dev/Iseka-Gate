class VisionState:

    def __init__(self):

        # kamera terakhir yang diproses
        self.last_camera = None

        # objek terakhir dari YOLO
        self.last_objects = []

        # hasil caption terakhir dari BLIP
        self.last_caption = ""

        # teks terakhir dari OCR
        self.last_text = ""

        # waktu terakhir vision berjalan
        self.last_update = None


    def update(
        self,
        camera=None,
        objects=None,
        caption=None,
        text=None
    ):

        if camera is not None:
            self.last_camera = camera

        if objects is not None:
            self.last_objects = objects

        if caption is not None:
            self.last_caption = caption

        if text is not None:
            self.last_text = text