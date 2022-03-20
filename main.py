import asyncio
import state
import config
from enctyption import Encryptor
from server import serve
from network import handle_send
import argparse
from aioconsole import ainput, aprint
import json
import logging
import sys
from console import get_user_msg


# async def get_active_chat():
#     # TODO: skip if there is only one chat
#     await aprint(">>> Print chat name you want to connect")
#     chat_name = await get_user_msg()
#     # TODO: validate chat name
#     return chat_name


async def main():
    # TODO
    # config.config.active_chat = await get_active_chat()

    while True:
        try:
            message = await get_user_msg()
            if not message:
                continue
            # TODO: allow user to change active chat
            request = {
                'type': 'MESSAGE',
                'name': state.state.config.name,
                'message': message,
                'port': state.state.config.port,
                'id': state.state.active_chat.id
            }
            await state.state.broadcast(request)
        except Exception as ex:
            logging.debug(f'Failed to send message: {ex}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser('Connect to decentralized chat')
    parser.add_argument('--config', help='path to configuration file', required=True)
    parser.add_argument('--debug', help='Print debug logs', action='store_true')

    # parser.add_argument('--port', help='port to start your server on', default=30127)
    args = parser.parse_args()

    if args.debug:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        logging.debug('Set debug logging')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([state.initialize_state(args.config)]))

    loop.run_until_complete(serve())
    loop.create_task(main())
    loop.run_forever()
