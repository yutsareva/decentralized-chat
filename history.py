import aiofiles
import aiofiles.os
import datetime
import json
import logging

import state
from enctyption import decrypt_message, encrypt_request


async def save_msg(text, file_name):
    async with aiofiles.open(f"{file_name}.txt", "a") as out:
        await out.write(f"{text}\n")
        await out.flush()


async def send_history(file_name):
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
            "port": state.state.config.port,
            "history": contents
        }
        await state.state.broadcast(request)


async def update_history(j):
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
        decrypted = decrypt_message(msg, state.state.encryptor)
        if decrypted is not None:
            decrypted_history.append(decrypted)
    logging.debug(decrypted_history)

    decrypted_history.sort(key=lambda k: datetime.datetime.strptime(k['time'], '%Y-%m-%d %H:%M:%S'))

    # chat = state.state.find_chat_by_id(j['id'])

    async with aiofiles.open(path, "w") as out:
        for line in decrypted_history:
            encrypted = state.state.encryptor.encrypt(j['id'], json.dumps(line))
            # encrypted = encrypt_request(line, chat, state.state.encryptor)['encrypted']
            await out.write(f"{encrypted}\n")
        await out.flush()
