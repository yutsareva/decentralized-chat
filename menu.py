from console import print_menu
import logging
import state
import asyncio
import signal

async def open_menu():
    await print_menu()
    # inp = await print_menu()
    # if inp == 'exit':
    #     exit(0)
    # # elif inp == ''
    # # TODO
    # exit(0)


async def handle_menu_input(message):
    if message == 'exit':
        state.STOP = True
        return
    elif message.startswith('chat'):
        try:
            _, chat_name = message.split(" ", 1)
        except Exception as ex:
            logging.debug('Invalid menu msg: ', ex)
            return
        state.state.set_active_chat(chat_name)
        state.INSIDE_MENU = False
        return

