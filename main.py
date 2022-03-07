import asyncio
from config import get_config
from enctyption import Encryptor


async def main():
    config = await get_config()
    encryptor = Encryptor(config.chats_to_secret_keys)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
