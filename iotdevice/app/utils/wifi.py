import asyncio
import functools
import os
import socket
import time
from asyncio import Future
from pathlib import Path

import websockets

import settings
from app.utils.led import LedController
from app.utils.crypto import CryptoController
from app.utils.logger import get_logger

logger = get_logger(__name__, 'wifi')


def was_configured():
    return Path(settings.WIFI_CONFIG_PATH).exists()


def clear_config():
    logger.info('CLEARING CONFIG')

    if was_configured():
        Path(settings.WIFI_CONFIG_PATH).unlink()

    key_file = Path(settings.KEY_FILE)
    iv_file = Path(settings.IV_FILE)

    if key_file.exists():
        key_file.unlink()

    if iv_file.exists():
        iv_file.unlink()

    os.system(f'nmcli connection down {settings.WIFI_NAME}')
    os.system(f'nmcli connection delete {settings.WIFI_NAME}')


class WifiController:

    def __init__(
            self,
            led_controller: LedController,
            crypto_controller: CryptoController
    ):
        self.led_controller = led_controller
        self.crypto_controller = crypto_controller

    async def configure(self):
        loop = asyncio.get_event_loop()
        stop = loop.create_future()
        while not self.has_connection() or not was_configured():
            clear_config()

            logger.info('WIFI NOT CONFIGURED, CONFIGURING...')
            self._start_access_point()
            self.led_controller.blue()

            async def setup_wifi(stop_future: Future):
                async with websockets.serve(functools.partial(self._change_network, stop_future), '0.0.0.0', 5678):
                    await stop_future

            await setup_wifi(stop)

            self.led_controller.red()

        key, iv = self.crypto_controller.get_user_key()
        return self.crypto_controller.encrypt_data(settings.DEVICE_ID, key, iv)

    def _start_access_point(self):
        logger.info('START ACCESS POINT')
        os.system(f'nmcli connection up {settings.AP_SSID}')

    def _parse_message(self, message: str):
        logger.info(f'RECEIVED ENCRYPTED: {message}')

        message = self.crypto_controller.decrypt(message)
        logger.info(message)

        message_split = message.split(',')
        logger.info(f'RECEIVED: {message_split}')

        return message_split

    async def _change_network(self, stop_future, websocket, path):
        logger.info('WAITING FOR MESSAGES')
        encrypted_device_id = None

        while True:
            try:
                self.led_controller.blue()

                message = await websocket.recv()
                message_split = self._parse_message(message)

                if len(message_split) != 4:
                    logger.info('SSID, password, key or initialization vector not specified')
                    continue

                self.led_controller.white()

                ssid, password, key, iv = message_split

                self.crypto_controller.save_key(key, iv)
                logger.info('KEYS SAVED')

                encrypted_device_id = self.crypto_controller.encrypt_data(settings.DEVICE_ID, key, iv)
                await websocket.send(encrypted_device_id)

                for _ in range(10):
                    if not self._update_config(ssid, password):
                        await websocket.close()
                        stop_future.set_result(True)
                        break
                    time.sleep(3)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except websockets.exceptions.ConnectionClosed:
                await websocket.close()
                stop_future.set_result(True)
                break
            except Exception as e:
                logger.error(e)

    def _update_config(self, ssid, password):
        logger.info('CONFIGURING WIFI')
        os.system(f'nmcli connection down {settings.AP_SSID}')
        os.system('nmcli dev wifi rescan')
        return os.system(f'nmcli device wifi connect \'{ssid}\' password \'{password}\' name \'{settings.WIFI_NAME}\'')

    def has_connection(self):
        try:
            socket.setdefaulttimeout(10)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('8.8.8.8', 53))
            return True
        except socket.error:
            return False
