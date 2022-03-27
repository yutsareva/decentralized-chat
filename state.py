import asyncio
import json
import logging

from config import Config, get_config_from_file
from enctyption import encrypt_request, Encryptor
from network import connect, handle_send
import sys


class State:
    def __init__(self, config: Config):
        self.config = config
        # TODO: select active chat
        # TODO: check there is at least one chat
        self.active_chat = config.chats[0]
        self.peer_ws = {}
        self.encryptor = Encryptor(config.chats)

    async def connect_peers(self):
        for p in self.config.peers:
            try:
                ws = await connect(p.address, p.port)
                self.peer_ws[f"{p.address}:{p.port}"] = ws
            except OSError as err:
                logging.debug(f"OS error: {err}")

    async def add_peer(self, address, port):
        connect_address = f"{address}:{port}"
        logging.debug(f'Peer address: {connect_address}')
        logging.debug(f'Existing peers: {self.peer_ws}')
        if connect_address in self.peer_ws:
            return
        await self.broadcast_new_peer_info(address, port)
        try:
            ws = await connect(address, port)
            self.peer_ws[connect_address] = ws
            request = {
                'type': 'PING',
                'port': self.config.port
            }
            asyncio.create_task(handle_send(ws, json.dumps(request)))
        except OSError as err:
            logging.debug(f"OS error: {err}")

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
        if request['type'] == 'MESSAGE':
            request = encrypt_request(request, self.active_chat, self.encryptor)

            for address, ws in self.peer_ws.items():
                try:
                    logging.debug(f'Sending request to {address}: {request}')
                    # asyncio.create_task(handle_send(ws, json.dumps(request)))
                    await handle_send(ws, json.dumps(request))
                except Exception as err:
                    logging.debug(f"Failed to broadcast msg: {err}")
                    del self.peer_ws[address]
                    hostname, port = address.split(':')
                    await self.add_peer(hostname, port)


state = None


async def initialize_state(config_file_name: str):
    global state
    state = State(await get_config_from_file(config_file_name))
    await state.connect_peers()
