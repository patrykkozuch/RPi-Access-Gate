import asyncio
import datetime
import logging
import sys
import time
from pathlib import Path

import RPi.GPIO as GPIO
import requests
from mfrc522 import SimpleMFRC522

import settings
from app.utils.crypto import CryptoController
from app.utils.led import LedController
from app.utils.mqtt_client import MQTTClient
from app.utils.wifi import WifiController, was_configured

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))


class IOTApp:
    def __init__(self):
        self.led_controller: LedController = LedController()
        self.wifi_controller: WifiController = WifiController(self.led_controller, CryptoController())
        self.reader = SimpleMFRC522()
        self.client = MQTTClient("access-log")
        self.client.tls_set(
            settings.CA_CERT,
            settings.CLIENT_CERT,
            settings.CLIENT_KEY
        )

    @property
    def has_keys(self):
        return Path(settings.KEY_FILE).exists() and Path(settings.IV_FILE).exists()

    def send_pairing_request(self, encoded_uuid):
        return requests.post(
            settings.API_URL + 'pair/device',
            json={
                'deviceId': settings.DEVICE_ID,
                'data': encoded_uuid
            }
        )

    async def _run(self):
        self.led_controller.red()

        if not was_configured() or not self.has_keys:
            encoded_device_id = await self.wifi_controller.configure()
            self.send_pairing_request(encoded_device_id)

        while True:
            if self.wifi_controller.has_connection():
                self.led_controller.green()
            else:
                self.led_controller.red()
            try:
                self.client.connect(settings.MQTT_HOST, settings.MQTT_PORT)

                while True:
                    tag_id, _ = self.reader.read()
                    logger.info(f"Tag ID: {tag_id}")
                    self.client.publish({
                        "tagId": str(tag_id),
                        "deviceId": settings.DEVICE_ID,
                        "timestamp": datetime.datetime.now().isoformat()
                    })
                    time.sleep(5)
            except KeyboardInterrupt:
                raise KeyboardInterrupt
            except Exception as e:
                logger.info(e)
                time.sleep(10)

    @staticmethod
    def run():
        app = IOTApp()
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(app._run())
        except KeyboardInterrupt:
            loop.stop()
            loop.close()
            GPIO.cleanup()
            exit()
        finally:
            GPIO.cleanup()
            loop.stop()
            loop.close()
