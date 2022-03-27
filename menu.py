from console import print_menu
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
        state.INSIDE_MENU = False
        return
    # if message.startswith('load history'):
    #     try:
    #         _, _, chat_name = message.split(" ", 2)
    #     except Exception as ex:
    #         logging.debug('Invalid menu msg: ', ex)
    #         return
    #     state.state.set_active_chat(chat_name)
    #     state.INSIDE_MENU = False
    #     return

