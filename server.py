import asyncio
import websockets
import json
from aioconsole import ainput, aprint


async def handle_recieve(websocket):
    while True:
        message = await websocket.recv()
        j = json.loads(message)
        # TODO: encrypt, print only active chat messages to stdout, the rest to files
        await aprint(f"{j['name']} > {j['message']}")
        # TODO: peer discovery


async def handle_send(websocket, message):
    await websocket.send(message)


# async def handle_send(websocket):
#     while True:
#         message = await ainput(f"you > ")
#         await websocket.send(message)


# async def connect(address, port):
#     async with websockets.connect(f"ws://{address}:{port}") as websocket:
#         recv = asyncio.create_task(handle_recieve(websocket))
#         send = asyncio.create_task(handle_send(websocket))
#
#         await recv
#         await send

async def connect(address, port):
    return await websockets.connect(f"ws://{address}:{port}")
# if __name__ == "__main__":
#     asyncio.run(main())
