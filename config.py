# from aioconsole import ainput, aprint
from typing import List

# from enctyption import generate_key
import aiofiles
from dataclasses import dataclass
import json


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


# async def get_config(port: int):
#     await aprint(">>> Print your name")
#     name = await ainput("you >")
#
#     peer_addresses = []
#     while True:
#         await aprint(">>> Print known peer address; press ENTER if no known peers left")
#         peer_address = await ainput(f"{name} > ")
#         if not peer_address:
#             break
#         peer_addresses.append(peer_address)
#
#     chats_to_secret_keys = {}
#     while True:
#         await aprint(">>> Print existing chat name and its secret key separated by a space; press ENTER if no chats left")
#         new_chat = await ainput(f"{name} > ")
#         if not new_chat:
#             break
#         chat_name, secret_key = new_chat.split()
#         secret_key_length = 32
#         if len(secret_key) != secret_key_length:
#             await aprint(f">>> Invalid secret key, try again")
#             continue
#
#         chats_to_secret_keys[chat_name] = secret_key
#     while True:
#         await aprint(">>> Do you want to start a new chat? Enter unique chat name if yes, else press ENTER")
#         chat_name = await ainput(f"{name} > ")
#         if not chat_name:
#             break
#         secret_key = generate_key()
#         await aprint(">>> Your key:")
#         await aprint(f">>> {secret_key.decode('utf-8')}")
#         chats_to_secret_keys[chat_name] = secret_key
#
#     return Config(name, peer_addresses, chats_to_secret_keys, port)
