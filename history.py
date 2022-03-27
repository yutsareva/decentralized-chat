import aiofiles
import aiofiles.os
import datetime
import json
import logging

from console import print_peer_msg
from enctyption import decrypt_message, encrypt_request
# import state


async def save_msg(text, file_name):
    async with aiofiles.open(f"{file_name}.txt", "a") as out:
        await out.write(f"{text}\n")
        await out.flush()


async def send_history(file_name, state):
    path = f"{file_name}.txt"
    try:
        await aiofiles.os.stat(str(path))
    except Exception:
        return

    contents = []
    async with aiofiles.open(path, mode='r') as f:
        async for line in f:
            contents.append(line)
        request = {
            "type": "HISTORY",
            "id": file_name,
            "port": state.config.port,
            "history": contents
        }
        await state.broadcast(request)


async def update_history(j, state):
    history = []
    for msg in j['history']:
        history.append(msg)

    path = f"{j['id']}.txt"
    async with aiofiles.open(path, mode='r') as f:
        async for msg in f:
            history.append(msg)

    history = list(set(history))

    decrypted_history = []
    for msg in history:
        decrypted = decrypt_message(msg, state.encryptor)
        if decrypted is not None:
            decrypted_history.append(decrypted)
    logging.debug(decrypted_history)

    decrypted_history.sort(key=lambda k: datetime.datetime.strptime(k['time'], '%Y-%m-%d %H:%M:%S'))

    # chat = state.find_chat_by_id(j['id'])

    async with aiofiles.open(path, "w") as out:
        for line in decrypted_history:
            encrypted = state.encryptor.encrypt(j['id'], json.dumps(line))
            # encrypted = encrypt_request(line, chat, state.encryptor)['encrypted']
            await out.write(f"{encrypted}\n")
        await out.flush()


async def print_history(state):
    path = f"{state.active_chat.id}.txt"
    async with aiofiles.open(path, mode='r') as f:
        async for msg in f:
            j = decrypt_message(msg, state.encryptor)
            await print_peer_msg(j['name'], '', '', j['port'], j['message'])

    # if state.state.active_chat.id == j['id']:
    #     await print_peer_msg(j['name'], '', '', j['port'], j['message'])
    # history = list(set(history))
    #
    # decrypted_history = []
    # for msg in history:
    #     decrypted = decrypt_message(msg, state.state.encryptor)