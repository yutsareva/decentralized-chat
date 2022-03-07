import asyncio


class State:
    def __init__(self, active_chat):
        self.lock = asyncio.Lock()
        self.active_chat = active_chat


global state
