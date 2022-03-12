import asyncio
import json

from config import Config, get_config_from_file
from network import connect, handle_send
import sys


class State:
    def __init__(self, config: Config):
        self.config = config
        self.active_chat = ""
        self.peer_ws = {}

    async def connect_peers(self):
        for p in self.config.peers:
            try:
                ws = await connect(p.address, p.port)
                self.peer_ws[f"{p.address}:{p.port}"] = ws
            except OSError as err:
                print(f"OS error: {err}", file=sys.stderr)

    async def add_peer(self, address, port):
        connect_address = f"{address}:{port}"
        if connect_address in self.peer_ws:
            return
        await self.broadcast_new_peer_info(address, port)
        ws = await connect(address, port)
        self.peer_ws[connect_address] = ws
        request = {
            'type': 'PING',
            'port': self.config.port
        }
        asyncio.create_task(handle_send(ws, json.dumps(request)))

    async def broadcast_new_peer_info(self, address, port):
        request = {
            "type": "NEW_PEER",
            "port": self.config.port,
            "peer": {
                "address": address,
                "port": port
            }
        }
        await self.broadcast(request)

    async def broadcast(self, request):
        for address, ws in self.peer_ws.items():
            print(f"send to {address}: {request}")
            asyncio.create_task(handle_send(ws, json.dumps(request)))



state = None


async def initialize_state(config_file_name: str):
    global state
    state = State(await get_config_from_file(config_file_name))
    await state.connect_peers()
