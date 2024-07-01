import base64
import logging
import string

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from typing import Union
import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _is_hex(text) -> bool:
    return all(c in string.hexdigits for c in text)


def _to_bytes(data: str) -> bytes:
    if _is_hex(data):
        return bytes.fromhex(data)
    else:
        return base64.b64decode(data)

def _parse_key(key, iv):
    if isinstance(key, str):
        key = _to_bytes(key)
    if isinstance(iv, str):
        iv = _to_bytes(iv)
    return key, iv

class CryptoController:
    def save_key(self, key: Union[str, bytes], iv: Union[str, bytes]) -> None:
        logger.info("SAVING KEYS")

        key, iv = _parse_key(key, iv)

        with open(settings.KEY_FILE, 'w') as f:
            f.write(base64.b64encode(key).decode())
        with open(settings.IV_FILE, 'w') as f:
            f.write(base64.b64encode(iv).decode())

    def get_user_key(self) -> tuple[bytes, bytes]:
        with open(settings.KEY_FILE, 'r') as f:
            key = f.readline()

        with open(settings.IV_FILE, 'r') as f:
            iv = f.readline()

        return _parse_key(key, iv)

    def encrypt_data(self, data: str, key: Union[bytes, str], iv: Union[bytes, str]) -> str:
        key, iv = _parse_key(key, iv)

        cypher = AES.new(key, AES.MODE_CBC, iv=iv)
        padded = pad(bytes(data.encode('utf-8')), 16)

        return base64.b64encode(cypher.encrypt(padded)).decode()

    def get_encrypted_device_id(self) -> str:
        return self.encrypt_data(settings.DEVICE_ID, *self.get_user_key())

    def decrypt(self, data: str, key: Union[bytes, str] = settings.INIT_KEY, iv: Union[bytes, str] = settings.INIT_IV) -> str:
        data = base64.b64decode(data)

        key, iv = _parse_key(key, iv)

        cypher = AES.new(key, AES.MODE_CBC, iv=iv)
        unpadded = unpad(cypher.decrypt(data), 16)

        return unpadded.decode()
