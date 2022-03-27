from typing import List
import json
from cryptography.fernet import Fernet
import logging

from config import Chat


class Encryptor:
    def __init__(self, chats: List[Chat]):
        self.instances = {}
        for chat in chats:
            self.instances[chat.id] = Fernet(chat.secret)

    def encrypt(self, id, message):
        return self.instances[id].encrypt(bytes(message, 'utf-8')).decode("utf-8")

    def decrypt(self, id, message):
        return self.instances[id].decrypt(bytes(message, 'utf-8')).decode("utf-8")


def generate_key():
    return Fernet.generate_key()


def encrypt_request(req: dict, chat: Chat, encryptor: Encryptor):
    new_req = {
        'type': req['type']
    }
    del req['type']
    try:
        new_req['encrypted'] = encryptor.encrypt(chat.id, json.dumps(req))
    except Exception as ex:
        logging.debug(f'Failed to encrypt request: {ex}')
    return new_req


def decrypt_message(msg, encryptor: Encryptor):
    for id in encryptor.instances.keys():
        try:
            decrypted = encryptor.decrypt(id, msg)
            logging.debug(f'Decrypted message: {decrypted}')
            loaded_decrypted = json.loads(decrypted)
            logging.debug(f'Decrypted loaded message: {loaded_decrypted}')
            if loaded_decrypted['id'] != id:
                raise Exception(f'Decrypted message has invalid id: {loaded_decrypted["id"]}, expected: {id}')
            return loaded_decrypted
        except Exception as ex:
            logging.debug(f'Failed to decrypt message {msg}: {ex}')
    return None
