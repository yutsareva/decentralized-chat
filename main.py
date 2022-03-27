import argparse
import asyncio
import datetime
import logging
import signal

from console import get_user_msg, get_user_menu_msg, print_menu_sync
from menu import handle_menu_input
from server import serve
import state


def signal_handler(sig, frame):
    state.INSIDE_MENU = True
    print_menu_sync()


signal.signal(signal.SIGINT, signal_handler)


async def main():
    while True:
        try:
            if state.STOP:
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
            request = {
                'type': 'MESSAGE',
                'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
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
