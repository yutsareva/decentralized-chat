import asyncio
import config
from enctyption import Encryptor
from server import connect, handle_send, serve
import argparse
from aioconsole import ainput, aprint
import json
from console import get_user_msg

async def get_active_chat():
    # TODO: skip if there is only one chat
    await aprint(">>> Print chat name you want to connect")
    chat_name = await get_user_msg()
    # TODO: validate chat name
    return chat_name


async def main(port):
    config.config = await config.get_config(port)
    encryptor = Encryptor(config.config.chats_to_secret_keys)

    config.config.active_chat = await get_active_chat()
    for address, port in config.config.peer_addresses:
        ws = await connect(address, port)
        config.config.peer_ws[f"{address}:{port}"] = ws

    while True:
        message = await get_user_msg()
        if not message:
            continue
        # TODO: allow user to change active chat
        request = {
            'name': config.config.name,
            'message': message,
            'port': config.config.port
        }
        send_tasks = []
        for address, ws in config.config.peer_ws.items():
            print(f"send to {address}: {request}")
            send_tasks.append(asyncio.create_task(handle_send(ws, json.dumps(request))))


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Connect to a decentralized chat')
    parser.add_argument('--port', help='port to start your server on', default=30127)
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.create_task(serve(args.port))
    loop.create_task(main(args.port))
    loop.run_forever()
