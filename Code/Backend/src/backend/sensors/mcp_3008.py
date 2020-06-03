import spidev
import RPi.GPIO as io

class MCP3008(object):
    def __init__(self):
        self.spi = spidev.SpiDev()

        self.spi.open(0,0)

    def read(self, channel):
        self.spi.max_speed_hz = 1350000
        adc = self.spi.xfer2([1,(8+channel)<<4,0])
        data = ((adc[1]&3) << 8) + adc[2]
        return data
