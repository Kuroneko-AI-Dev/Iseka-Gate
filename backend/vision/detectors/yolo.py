from pathlib import Path

from ultralytics import YOLO


BASE_DIR = Path(__file__).resolve().parents[2]

MODEL_PATH = BASE_DIR / "models" / "yolo" / "yolov8n.pt"


class YoloDetector:

    def __init__(self):

        self.model = YOLO(str(MODEL_PATH))


    def detect(

        self,

        image,

        conf=0.45

    ):

        results = self.model(

            image,

            conf=conf,

            verbose=False

        )

        objects = []

        for result in results:

            for box in result.boxes:

                cls = int(box.cls[0])

                name = self.model.names[cls]

                score = float(box.conf[0])

                xyxy = box.xyxy[0].tolist()

                objects.append({

                    "name": name,

                    "confidence": round(score, 3),

                    "box": [

                        int(v)

                        for v in xyxy

                    ]

                })

        return objects