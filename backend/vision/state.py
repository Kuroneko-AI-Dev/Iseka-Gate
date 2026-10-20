from datetime import datetime


class VisionState:

    def __init__(self):

        # Kamera terakhir
        self.last_camera = None

        # Hasil vision terakhir
        self.last_objects = []
        self.last_caption = ""
        self.last_text = ""

        # Ringkasan scene
        self.last_scene = ""

        # Waktu update
        self.last_update = None

    def update(
        self,
        camera=None,
        objects=None,
        caption=None,
        text=None,
        scene=None
    ):

        if camera is not None:
            self.last_camera = camera

        if objects is not None:
            self.last_objects = objects

        if caption is not None:
            self.last_caption = caption

        if text is not None:
            self.last_text = text

        if scene is not None:
            self.last_scene = scene

        self.last_update = datetime.now()

    def get_object_labels(self):

        labels = []

        for obj in self.last_objects:

            if isinstance(obj, dict):

                label = obj.get("label")

                if label:
                    labels.append(label)

            else:

                labels.append(str(obj))

        return labels

    def has_object(self, label):

        return label in self.get_object_labels()

    def clear(self):

        self.last_camera = None
        self.last_objects = []
        self.last_caption = ""
        self.last_text = ""
        self.last_scene = ""
        self.last_update = None