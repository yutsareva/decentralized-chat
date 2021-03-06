from console import print_menu
from history import print_history
import logging
import state


async def handle_menu_input(message):
    if message == 'exit':
        state.STOP = True
        return
    if message.startswith('chat'):
        try:
            _, chat_name = message.split(" ", 1)
        except Exception as ex:
            logging.debug('Invalid menu msg: ', ex)
            return
        state.state.set_active_chat(chat_name)
    elif message == 'load history':
        request = {
            'type': 'MESSAGE',
            'get_history': True,
            'port': state.state.config.port,
            'id': state.state.active_chat.id
        }
        await state.state.broadcast(request)
    elif message == 'show history':
        await print_history(state.state)
    state.INSIDE_MENU = False
    return

