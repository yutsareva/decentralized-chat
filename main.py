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
from console import get_user_msg, get_user_menu_msg, print_menu, print_menu_sync
import signal
from menu import handle_menu_input
from menu import open_menu


# async def get_active_chat():
#     # TODO: skip if there is only one chat
#     await aprint(">>> Print chat name you want to connect")
#     chat_name = await get_user_msg()
#     # TODO: validate chat name
#     return chat_name


def signal_handler(sig, frame):
    state.INSIDE_MENU = True
    print_menu_sync()


signal.signal(signal.SIGINT, signal_handler)


async def main():
    # TODO
    # config.config.active_chat = await get_active_chat()

    while True:
        try:
            if state.STOP:
                print("STOP____")
                return
            if state.INSIDE_MENU:
                message = await get_user_menu_msg()
            else:
                message = await get_user_msg()
            if state.INSIDE_MENU:
                await handle_menu_input(message)
                continue
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

    args = parser.parse_args()

    if args.debug:
        root = logging.getLogger()
        root.setLevel(logging.DEBUG)
        logging.debug('Set debug logging')

    state.loop = asyncio.get_event_loop()
    state.loop.run_until_complete(asyncio.wait([state.initialize_state(args.config)]))

    state.loop.run_until_complete(serve())
    state.loop.run_until_complete(main())