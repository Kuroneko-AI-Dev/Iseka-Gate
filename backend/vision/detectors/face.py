import mediapipe as mp

from vision.utils import ImageUtils


class FaceDetector:

    def __init__(self):

        self.detector = mp.solutions.face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.6
        )


    def detect(self, image):

        rgb = ImageUtils.rgb(image)

        result = self.detector.process(rgb)

        faces = []

        if result.detections:

            h, w = image.shape[:2]

            for detection in result.detections:

                box = detection.location_data.relative_bounding_box

                x = int(box.xmin * w)
                y = int(box.ymin * h)

                bw = int(box.width * w)
                bh = int(box.height * h)

                faces.append({

                    "x": x,
                    "y": y,
                    "w": bw,
                    "h": bh,

                    "score": float(
                        detection.score[0]
                    )

                })

        return faces