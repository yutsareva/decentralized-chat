import asyncio
import websockets
import json
from aioconsole import ainput, aprint
import state
import config
import logging
from console import print_peer_msg
from enctyption import decrypt_message


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
                    j.update(decrypted)
                    #  TODO: print only active chat messages to stdout, the rest to files
                    address, port = websocket.remote_address
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
            except Exception as ex:
                logging.debug('Failed to handle message: ', ex)
    except Exception as ex:
        logging.debug('Failed get message fromm socket: ', ex)


def serve():
    import os
    my_ip = os.popen('curl -s ifconfig.me').readline()
    logging.debug(f"start server on {my_ip}:{state.state.config.port}")
    return websockets.serve(handle_receive, "127.0.0.1", state.state.config.port)
