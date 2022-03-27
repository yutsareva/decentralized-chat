import aiofiles as aiof
import json


async def save_msg(j):
    async with aiof.open(j['id'], "a") as out:
        await out.write(json.dumps(j))
        await out.flush()
