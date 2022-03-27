import aiofiles
from dataclasses import dataclass
import json
from typing import List


@dataclass
class Chat:
    name: str
    id: str  # uuid4
    secret: str


@dataclass
class Peer:
    address: str
    port: int


@dataclass
class Config:
    name: str
    port: str
    chats: List[Chat]
    peers: List[Peer]


async def get_config_from_file(filename: str):
    async with aiofiles.open(filename, mode='r') as f:
        config_content = json.loads(await f.read())
        name = config_content["name"]
        port = config_content["port"]
        chats = []
        for chat_json in config_content["chats"]:
            chat = Chat(chat_json["name"], chat_json["id"], chat_json["secret"])
            chats.append(chat)
        peers = []
        for peer_json in config_content["peers"]:
            peer = Peer(peer_json["address"], peer_json["port"])
            peers.append(peer)
    return Config(name, port, chats, peers)
