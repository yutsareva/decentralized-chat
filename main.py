import asyncio
from config import get_config
from enctyption import Encryptor
from server import connect, handle_send, handle_recieve
import argparse
from aioconsole import ainput, aprint
import global_state
import json


async def get_active_chat():
    # TODO: skip if there is only one chat
    await aprint(">>> Print chat name you want to connect")
    chat_name = await ainput("you > ")
    # TODO: validate chat name
    return chat_name


async def main():
    parser = argparse.ArgumentParser('Connect to a decentralized chat')
    parser.add_argument('--port', dest='port to start your server on', action='store_const', default=30127)
    args = parser.parse_args()
    config = await get_config(args.port)
    encryptor = Encryptor(config.chats_to_secret_keys)

    peer_ws = {}
    recv_tasks = []
    for address, port in config.peers():
        ws = await connect(address, port)
        peer_ws[f"{address}:{port}"] = ws
        recv_tasks.append(handle_recieve(ws))
        # _ = await asyncio.gather(
        #     recv_tasks
        # )

    chat_name = get_active_chat()
    global_state.state = global_state.State(chat_name)

    while True:
        message = await ainput(f"you > ")
        # TODO: allow user to change active chat
        request = {
            'name': config.name,
            'message': message
        }
        send_tasks = []
        for _, ws in peer_ws.items():
            send_tasks.append(asyncio.create_task(handle_send(ws, json.dumps(request))))

        # _ = await asyncio.gather(
        #     send_tasks
        # )



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
