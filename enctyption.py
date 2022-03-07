from cryptography.fernet import Fernet
import base64


class Encryptor:
    def __init__(self, name_to_secret_keys: dict):
        self.instances = {}
        for name, secret in name_to_secret_keys.items():
            self.instances[name] = Fernet(base64.urlsafe_b64encode(bytes(secret, 'utf-8')))

    def encrypt(self, name, message):
        return self.instances[name].encrypt(message)

    def decrypt(self, name, message):
        return self.instances[name].decrypt(message)


def generate_key():
    return Fernet.generate_key()
