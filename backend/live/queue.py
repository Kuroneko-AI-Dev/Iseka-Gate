import asyncio

comment_queue = asyncio.Queue()


async def add_comment(comment: dict):

    await comment_queue.put(comment)


async def get_comment():

    return await comment_queue.get()