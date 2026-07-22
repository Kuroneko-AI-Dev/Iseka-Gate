from .pipeline import VisionPipeline


class VisionService:

    def __init__(self):

        self.pipeline = VisionPipeline()


    async def analyze(
        self,
        image,
        camera,
        mode
    ):

        return await self.pipeline.process(

            image=image,

            camera=camera,

            mode=mode

        )