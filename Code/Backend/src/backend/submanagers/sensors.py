from threading import Thread
import sys

import time as t

import RPi.GPIO as io

from ..sensors.distance import DistanceSensor
from ..util.logger import log

class SensorManager(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.daemon = True
        self.cleanup = False

        io.setmode(io.BOARD)

    def run(self):
        log.info('SENSR', 'Started')

        self.distance_sensor = DistanceSensor(11, 7)
        self.distance_sensor.start()

        self.cleanup = True

        self.loop()

    def loop(self):
        log.info('SENSR', 'Measurement loop started...')
        while True:
            log.info('SENSR', 'Getting distance:')
            print(self.distance_sensor.get_last_distance(), 'cm')
            t.sleep(10)

    def kill(self):
        if self.cleanup:
            io.cleanup()

        sys.exit()
