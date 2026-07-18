from fastapi import WebSocket

connections = []


async def connect(ws: WebSocket):

    await ws.accept()

    connections.append(ws)


def disconnect(ws: WebSocket):

    if ws in connections:
        connections.remove(ws)


async def broadcast(data):

    dead = []

    for ws in connections:

        try:

            await ws.send_json(data)

        except:

            dead.append(ws)

    for ws in dead:

        disconnect(ws)