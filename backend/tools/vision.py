from vision import VisionService
from vision.prompts import VisionPrompt

from chat.memory import get_memories
from chat.history import get_recent_messages

from gpt_service import ask_gpt


class VisionTool:

    def __init__(self):

        self.vision = VisionService()

    async def ask(

        self,

        image,

        camera,

        intent,

        user_message,

        user,

        conversation_id,

        db

    ):

        vision = await self.vision.analyze(

            image=image,

            camera=camera,

            mode=intent

        )

        memory = get_memories(

            db,

            user.id

        )

        history = get_recent_messages(

            db,

            conversation_id

        )

        prompt = VisionPrompt.build(

            user_message=user_message,

            vision=vision,

            memory=memory,

            history=history

        )

        answer = await ask_gpt(

            prompt

        )

        return answer