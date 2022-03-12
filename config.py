from aioconsole import ainput, aprint
from enctyption import generate_key


class Config:
    def __init__(self, name, peer_addresses: list[str], chats_to_secret_keys: dict, port: int):
        self.name = name
        self.chats_to_secret_keys = chats_to_secret_keys
        self.peer_addresses = []
        for peer_address in peer_addresses:
            self.peer_addresses.append(peer_address.split(':'))
        self.port = port
        self.active_chat = ""
        self.peer_ws = {}


global config
config = None


async def get_config(port: int):
    await aprint(">>> Print your name")
    name = await ainput("you >")

    peer_addresses = []
    while True:
        await aprint(">>> Print known peer address; press ENTER if no known peers left")
        peer_address = await ainput(f"{name} > ")
        if not peer_address:
            break
        peer_addresses.append(peer_address)

    chats_to_secret_keys = {}
    while True:
        await aprint(">>> Print existing chat name and its secret key separated by a space; press ENTER if no chats left")
        new_chat = await ainput(f"{name} > ")
        if not new_chat:
            break
        chat_name, secret_key = new_chat.split()
        secret_key_length = 32
        if len(secret_key) != secret_key_length:
            await aprint(f">>> Invalid secret key, try again")
            continue

        chats_to_secret_keys[chat_name] = secret_key
    while True:
        await aprint(">>> Do you want to start a new chat? Enter unique chat name if yes, else press ENTER")
        chat_name = await ainput(f"{name} > ")
        if not chat_name:
            break
        secret_key = generate_key()
        await aprint(">>> Your key:")
        await aprint(f">>> {secret_key.decode('utf-8')}")
        chats_to_secret_keys[chat_name] = secret_key

    return Config(name, peer_addresses, chats_to_secret_keys, port)
