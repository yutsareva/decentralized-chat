import json
import logging
import websockets

from console import print_peer_msg
from enctyption import decrypt_message
from history import save_msg, send_history, update_history
import state


async def handle_receive(websocket):
    try:
        async for message in websocket:
            try:
                j = json.loads(message)
                logging.debug(f"got msg: {j}")
                if j['type'] == 'MESSAGE':
                    decrypted = decrypt_message(j['encrypted'], state.state.encryptor)
                    if not decrypted:
                        continue
                    if 'get_history' in decrypted:
                        address, port = websocket.remote_address
                        await state.state.add_peer(address, decrypted['port'])
                        await send_history(decrypted['id'])
                        continue

                    await save_msg(j['encrypted'], file_name=decrypted['id'])
                    j.update(decrypted)
                    address, port = websocket.remote_address
                    if state.state.active_chat.id == j['id']:
                        await print_peer_msg(j['name'], address, port, j['port'], j['message'])

                    await state.state.add_peer(address, j['port'])
                    # ws = await connect(address, j['port'])
                    # config.config.peer_ws[f"{address}:{j['port']}"] = ws
                    # TODO: peer discovery
                elif j['type'] == 'NEW_PEER':
                    address, port = websocket.remote_address
                    await state.state.add_peer(address, j['port'])
                    await state.state.add_peer(j['peer']['address'], j['peer']['port'])
                elif j['type'] == 'PING':
                    address, _ = websocket.remote_address
                    await state.state.add_peer(address, j['port'])
                elif j['type'] == 'HISTORY':
                    # decrypted = decrypt_message(j['encrypted'], state.state.encryptor)
                    # if not decrypted:
                    #     continue
                    # await update_history(decrypted)
                    await update_history(j)
            except Exception as ex:
                logging.debug('Failed to handle message: ', ex)
    except Exception as ex:
        logging.debug('Failed get message fromm socket: ', ex)


def serve():
    import os
    my_ip = os.popen('curl -s ifconfig.me').readline()
    logging.debug(f"start server on {my_ip}:{state.state.config.port}")
    return websockets.serve(handle_receive, "0.0.0.0", state.state.config.port)
