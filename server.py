import asyncio
import websockets
import json
from aioconsole import ainput, aprint
import socket
import config
from console import print_peer_msg


async def handle_recieve(websocket):
    async for message in websocket:
        j = json.loads(message)
        # TODO: encrypt, print only active chat messages to stdout, the rest to files
        address, port = websocket.remote_address
        # await aprint(f"\033[A\33[2K\r{j['name']} [{address}:{port} ({j['port']})] > {j['message']}", end="\nyou > ")
        await print_peer_msg(j['name'], address, port, j['port'], j['message'])

        ws = await connect(address, j['port'])
        config.config.peer_ws[f"{address}:{j['port']}"] = ws
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


async def serve(port):
    import os
    my_ip = os.popen('curl -s ifconfig.me').readline()
    await aprint(f"start server on {my_ip}:{port}")
    async with websockets.serve(handle_recieve, "127.0.0.1", port):
        await asyncio.Future()  # run forever


# if __name__ == "__main__":
#     asyncio.run(main())
