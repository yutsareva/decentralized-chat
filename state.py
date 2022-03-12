from config import Config, get_config_from_file
from network import connect
import sys


class State:
    def __init__(self, config: Config):
        self.config = config
        self.active_chat = ""
        self.peer_ws = {}

    async def connect_peers(self):
        for p in self.config.peers:
            try:
                ws = await connect(p.address, p.port)
                self.peer_ws[f"{p.address}:{p.port}"] = ws
            except OSError as err:
                print(f"OS error: {err}", file=sys.stderr)

    async def add_peer(self, address, port):
        connect_address = f"{address}:{port}"
        if connect_address in self.peer_ws:
            return
        ws = await connect(address, port)
        self.peer_ws[connect_address] = ws


state = None


async def initialize_state(config_file_name: str):
    global state
    state = State(await get_config_from_file(config_file_name))
    await state.connect_peers()
