import asyncio
import json
import logging

from config import Config, get_config_from_file
from enctyption import encrypt_request, Encryptor
from history import save_msg
from network import connect, handle_send

INSIDE_MENU = False
STOP = False
loop = None


class State:
    def __init__(self, config: Config):
        self.config = config
        self.active_chat = config.chats[0]
        self.peer_ws = {}
        self.encryptor = Encryptor(config.chats)

    def set_active_chat(self, chat_name):
        chat = self.find_chat(chat_name)
        if chat is not None:
            self.active_chat = chat
        else:
            logging.debug('No chat with name: ', chat_name)

    def find_chat(self, chat_name):
        for chat in self.config.chats:
            if chat.name == chat_name:
                return chat
        return None

    def find_chat_by_id(self, id):
        for chat in self.config.chats:
            if chat.id == id:
                return chat
        return None

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
            # asyncio.create_task(handle_send(ws, json.dumps(request)))
            await handle_send(ws, json.dumps(request))
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
            encrypted_request = encrypt_request(request, self.active_chat, self.encryptor)
            if 'get_history' not in request:
                await save_msg(encrypted_request['encrypted'], request['id'])
            request = encrypted_request
        await self.broadcast_request(request)

    async def broadcast_request(self, request):
        for address in list(self.peer_ws.keys()):
            try:
                logging.debug(f'Sending request to {address}: {request}')
                # asyncio.create_task(handle_send(ws, json.dumps(request)))
                await handle_send(self.peer_ws[address], json.dumps(request))
            except Exception as err:
                logging.debug(f"Failed to broadcast msg: {err}")
                self.peer_ws.pop(address)
                hostname, port = address.split(':')
                await self.add_peer(hostname, port)

    def it_is_me(self, port, name):
        return self.config.port == port and self.config.name == name


state = None


async def initialize_state(config_file_name: str):
    global state
    state = State(await get_config_from_file(config_file_name))
    await state.connect_peers()
