from pathlib import Path

BASE_DIR = Path(__file__).parent
LOGS_DIR = BASE_DIR.joinpath('logs')
CERTS_DIR = BASE_DIR.joinpath('certs')

CA_CERT = CERTS_DIR.joinpath("AmazonRootCA1.pem")
CLIENT_CERT = CERTS_DIR.joinpath("client.pem.crt")
CLIENT_KEY = CERTS_DIR.joinpath("client.pem.key")

MQTT_HOST = "FILL_THIS.amazonaws.com"
MQTT_PORT = 8883

DEVICE_ID = "f60084cb-583f-43cb-8f84-d22796977fbc"

#### WIFI SETTINGS ####
AP_INTERFACE = 'wlan0'

AP_SSID = 'IOT-HotSpot'
AP_PASSWORD = 'IOT2024'

WIFI_NAME = 'IOT-WiFi'
WIFI_CONFIG_PATH = f'/etc/NetworkManager/system-connections/{WIFI_NAME}.nmconnection'

#### CRYPTO ####
_KEY_DIR = BASE_DIR.joinpath('keys')
_KEY_DIR.mkdir(parents=True, exist_ok=True)

KEY_FILE = _KEY_DIR.joinpath('user.key')
IV_FILE = _KEY_DIR.joinpath('user.iv')

# Hardcoded default key for initial communication between app and device
INIT_KEY = "955ffdd4e88b685b2978f8c58664f88a459e458737658e8b2acc7d0484f78742"
INIT_IV = "605f40ff8c98ae0abbd6c4d5057aa13c"

#### REQUESTS ####
API_URL = 'FILL_THIS'
