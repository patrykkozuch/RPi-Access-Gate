from enum import Enum

import RPi.GPIO as GPIO

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)
RED = 12
GREEN = 13
BLUE = 19

GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)
GPIO.setup(BLUE, GPIO.OUT)


class Colors(Enum):
    WHITE = 0
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4


class LedController:
    def white(self):
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.HIGH)

    def red(self):
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.LOW)

    def green(self):
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.LOW)

    def blue(self):
        GPIO.output(RED, GPIO.LOW)
        GPIO.output(GREEN, GPIO.LOW)
        GPIO.output(BLUE, GPIO.HIGH)

    def yellow(self):
        GPIO.output(RED, GPIO.HIGH)
        GPIO.output(GREEN, GPIO.HIGH)
        GPIO.output(BLUE, GPIO.LOW)
