import aiofiles as aiof
import json


async def save_msg(j, file_name):
    async with aiof.open(f"{file_name}.txt", "a") as out:
        await out.write(f"{json.dumps(j)}\n")
        await out.flush()
