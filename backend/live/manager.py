from TikTokLive import TikTokLiveClient
import asyncio
import threading
from TikTokLive.events import (
    ConnectEvent,
    DisconnectEvent,
    CommentEvent,
)

from .events import on_comment


class LiveManager:

    def __init__(self):
        self.connected = False
        self.room_id = None
        self.thread = None
        self.client = None
        self.username = None

    def connect(self, username: str):

        self.username = username

        # boleh pakai "raphael_ai" atau "@raphael_ai"
        if not username.startswith("@"):
            username = f"@{username}"

        self.client = TikTokLiveClient(
            unique_id=username
        )

        @self.client.on(ConnectEvent)
        async def connected(event: ConnectEvent):

            self.connected = True
            self.room_id = self.client.room_id
            print("\n")
            print("=" * 50)
            print("TikTok Connected")
            print(f"Username : {event.unique_id}")
            print(f"Room ID  : {self.client.room_id}")
            print("=" * 50)

        @self.client.on(DisconnectEvent)
        async def disconnected(event: DisconnectEvent):
            self.connected = False
            self.room_id = None
            print("\nTikTok Disconnected")

        @self.client.on(CommentEvent)
        async def comment(event: CommentEvent):

            await on_comment(event)

    def run(self):

        if self.client is None:
            raise RuntimeError("Client belum dibuat.")

        self.client.run()

    def start(self):

        if self.client is None:
            raise RuntimeError("Client belum dibuat.")

        if self.thread and self.thread.is_alive():
            return

        self.thread = threading.Thread(
            target=self.run,
            daemon=True
        )

        self.thread.start()

    async def disconnect(self):

        if self.client:

            await self.client.disconnect()