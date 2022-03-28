from aioconsole import ainput, aprint

COLOURS = [30, 31, 32, 33, 34, 35, 36, 37, 90, 92, 93, 94, 95, 96]

COLOR = '\033[{color}m'
CRED = '\033[91m'
CEND = '\033[0m'
MESSAGE_WAIT_STR = f"{CRED}you > {CEND}"
PEER_MSG = "\33[2K\r" + COLOR + "{name} > " + CEND + "{message}"
# PEER_MSG = "\33[2K\r" + COLOR + "{name} [{address}:{port} ({port2})] > " + CEND + "{message}"

MESSAGE_MENU_WAIT_STR = f"you > "
MENU_STR = "\33[2K\r>>> To change chat print 'chat CHAT_NAME'" + \
           "\n>>> To exit print 'exit'" + \
           "\n>>> To load chat history print 'load history'" + \
           "\n>>> To output chat history print 'show history'"


async def print_peer_msg(peer_name, address, port, port2, message, it_is_me=False, noend=False):
    if it_is_me:
        color = 91
        peer_name = 'you'
    else:
        color = COLOURS[abs(hash(peer_name)) % len(COLOURS)]
    end_str = "\n" if noend else f"\n{MESSAGE_WAIT_STR}"
    await aprint(PEER_MSG.format(
        color=color, name=peer_name, address=address, port=port, port2=port2, message=message),
        end=end_str)


async def get_user_msg():
    return await ainput(MESSAGE_WAIT_STR)


async def print_menu():
    await aprint(MENU_STR, end=f"\n{MESSAGE_MENU_WAIT_STR}")


def print_menu_sync():
    print(MENU_STR, end=f"\n{MESSAGE_MENU_WAIT_STR}")


async def get_user_menu_msg():
    return await ainput(MESSAGE_MENU_WAIT_STR)
