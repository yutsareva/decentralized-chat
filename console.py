from aioconsole import ainput, aprint

CRED = '\033[91m'
CEND = '\033[0m'
MESSAGE_WAIT_STR = f"{CRED}you > {CEND}"
PEER_MSG = "\33[2K\r" + CRED + "{name} [{address}:{port} ({port2})] > " + CEND + "{message}"


async def print_peer_msg(peer_name, address, port, port2, message):
    await aprint(PEER_MSG.format(
        name=peer_name, address=address, port=port, port2=port2, message=message), end=f"\n{MESSAGE_WAIT_STR}")


async def get_user_msg():
    return await ainput(MESSAGE_WAIT_STR)
