from fastapi import APIRouter, Depends, HTTPException
import asyncio
from fastapi import WebSocket

from live.websocket import connect as websocket_connect, disconnect as websocket_disconnect
from schemas import LiveConnectRequest
from live.manager import LiveManager
from routers.admin import get_current_admin

router = APIRouter(
    prefix="/live",
    tags=["Live"]
)

manager = LiveManager()


@router.post("/connect")
async def connect_live(
    data: LiveConnectRequest,
    admin=Depends(get_current_admin)
):

    if manager.connected:

        raise HTTPException(
            status_code=400,
            detail="Sudah terhubung."
        )

    manager.connect(data.username)

    manager.start()

    return {
        "success": True
    }


@router.get("/status")
async def status(admin=Depends(get_current_admin)):

    return {

        "connected": manager.connected,

        "username": manager.username,

        "room_id": manager.room_id

    }


@router.post("/disconnect")
async def disconnect_live(admin=Depends(get_current_admin)):

    if manager.client:

        await manager.client.disconnect()

    return {
        "success": True
    }

@router.websocket("/ws")
async def websocket(ws: WebSocket):

    await websocket_connect(ws)

    try:

        while True:

            await ws.receive_text()

    except:

        websocket_disconnect(ws)
