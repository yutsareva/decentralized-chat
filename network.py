import websockets

async def handle_send(websocket, message):
    await websocket.send(message)


async def connect(address, port):
    return await websockets.connect(f"ws://{address}:{port}")
