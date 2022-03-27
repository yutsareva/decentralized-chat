from aioconsole import ainput, aprint

COLOURS = [30, 31, 32, 33, 34, 35, 36, 37, 90, 92, 93, 94, 95, 96]

COLOR = '\033[{color}m'
CRED = '\033[91m'
CEND = '\033[0m'
MESSAGE_WAIT_STR = f"{CRED}you > {CEND}"
PEER_MSG = "\33[2K\r" + COLOR + "{name} > " + CEND + "{message}"
# PEER_MSG = "\33[2K\r" + COLOR + "{name} [{address}:{port} ({port2})] > " + CEND + "{message}"


async def print_peer_msg(peer_name, address, port, port2, message):
    color = COLOURS[abs(hash(peer_name)) % len(COLOURS)]
    await aprint(PEER_MSG.format(
        color=color, name=peer_name, address=address, port=port, port2=port2, message=message),
        end=f"\n{MESSAGE_WAIT_STR}")


async def get_user_msg():
    return await ainput(MESSAGE_WAIT_STR)
