from TikTokLive.events import CommentEvent

from .queue import add_comment
from .websocket import broadcast


async def on_comment(event: CommentEvent):

    data = {

        "user": event.user.nickname,

        "unique_id": event.user.unique_id,

        "comment": event.comment

    }

    print("comment:", data)

    await add_comment(data)

    await broadcast(data)