import asyncio
import state
import config
from enctyption import Encryptor
from server import serve
from network import handle_send
import argparse
from aioconsole import ainput, aprint
import json
from console import get_user_msg


# async def get_active_chat():
#     # TODO: skip if there is only one chat
#     await aprint(">>> Print chat name you want to connect")
#     chat_name = await get_user_msg()
#     # TODO: validate chat name
#     return chat_name


async def main():
    # TODO
    # encryptor = Encryptor(state.state.config.chats_to_secret_keys)

    # TODO
    # config.config.active_chat = await get_active_chat()

    while True:
        message = await get_user_msg()
        if not message:
            continue
        # TODO: allow user to change active chat
        request = {
            'name': state.state.config.name,
            'message': message,
            'port': state.state.config.port
        }
        send_tasks = []
        for address, ws in state.state.peer_ws.items():
            print(f"send to {address}: {request}")
            send_tasks.append(asyncio.create_task(handle_send(ws, json.dumps(request))))


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Connect to a decentralized chat')
    parser.add_argument('--config', help='path to configuration file')
    # parser.add_argument('--port', help='port to start your server on', default=30127)
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(state.initialize_state(args.config))

    loop.create_task(serve())
    loop.create_task(main())
    loop.run_forever()
