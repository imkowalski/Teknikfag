import time
import board
import busio
import adafruit_am2320
from signal import signal, SIGINT
from sys import exit

# create the I2C shared bus
class AM2320:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.am = adafruit_am2320.AM2320(i2c)

    def read(self):
        return (self.am.temperature, self.am.relative_humidity)

    def close(self):
        pass

am = AM2320()
print(am.read())