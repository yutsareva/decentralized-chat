import asyncio
import websockets
import json
from aioconsole import ainput, aprint
import state
import config
from console import print_peer_msg


async def handle_receive(websocket):
    async for message in websocket:
        j = json.loads(message)
        print(f"got msg: {j}")
        if j['type'] == 'MESSAGE':
            # TODO: encrypt, print only active chat messages to stdout, the rest to files
            address, port = websocket.remote_address
            await print_peer_msg(j['name'], address, port, j['port'], j['message'])

            await state.state.add_peer(address, j['port'])
            # ws = await connect(address, j['port'])
            # config.config.peer_ws[f"{address}:{j['port']}"] = ws
            # TODO: peer discovery
        elif j['type'] == 'NEW_PEER':
            address, port = websocket.remote_address
            await state.state.add_peer(address, j['port'])
            await state.state.add_peer(j['peer']['address'], j['peer']['port'])
        elif j['type'] == 'PING':
            address, _ = websocket.remote_address
            await state.state.add_peer(address, j['port'])




async def serve():
    import os
    my_ip = os.popen('curl -s ifconfig.me').readline()
    await aprint(f"start server on {my_ip}:{state.state.config.port}")
    async with websockets.serve(handle_receive, "127.0.0.1", state.state.config.port):
        await asyncio.Future()
