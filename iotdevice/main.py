import logging
import os
import signal
import subprocess
import time
import RPi.GPIO as GPIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

BTN_PIN = 21
GPIO.setup(BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


from app.utils.wifi import clear_config


def btn_is_clicked():
    return GPIO.input(BTN_PIN)


def start_app():
    return subprocess.Popen(["/home/iot/.virtualenvs/iot/bin/python", "/home/iot/projects/iotdevice/app.py"])


try:
    app_process = start_app()

    while True:
        if btn_is_clicked():
            logger.info('CLICKED RESTART')
            os.kill(app_process.pid, signal.SIGTERM)
            clear_config()
            app_process = start_app()
            time.sleep(5)
except KeyboardInterrupt:
    os.kill(app_process.pid, signal.SIGTERM)
finally:
    GPIO.cleanup()
