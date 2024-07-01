import json
import time

from paho.mqtt import client as mqtt

from app.utils.logger import get_logger

logger = get_logger(__name__, 'mqtt')


def _log_connect(client, userdata, flags, rc, properties=None):
    logger.info("connected to endpoint with result code: %s", rc)


def _log_message(mqttc, userdata, msg):
    logger.info('received message: topic: %s payload: %s', msg.topic, msg.payload.decode())


def _log_publish(client, userdata, mid):
    logger.info(f"Message published - messageId: {mid}")


def _log_subscribe(client, userdata, mid, granted_qos, properties=None):
    logger.info(f"Subscribed to topic - messageId: {mid}")


class MQTTClient:
    def __init__(self, topic):
        self._client = mqtt.Client(protocol=mqtt.MQTTv5)
        self._client.on_connect = _log_connect
        self._client.on_message = _log_message
        self._client.on_subscribe = _log_subscribe
        self._client.on_publish = _log_publish

        self.topic = topic

    @property
    def is_connected(self) -> bool:
        return self._client.is_connected

    def tls_set(self, ca_cert, client_cert, client_key):
        self._client.tls_set(ca_cert, client_cert, client_key, tls_version=2)

    def publish(self, data):
        self._client.publish(self.topic, json.dumps(data))

    def subscribe(self):
        self._client.subscribe(self.topic)

    def connect(self, host, port):
        self._client.connect(host, port, 60)

        while not self._client.is_connected():
            self._client.loop()
            time.sleep(0.5)

    def loop_forever(self):
        self._client.loop_forever()
