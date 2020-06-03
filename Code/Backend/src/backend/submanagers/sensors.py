from threading import Thread
import sys

import time as t

import RPi.GPIO as io

from ..func import get_ip_address

from ..sensors.distance import DistanceSensor
from ..sensors.rfid_rc522 import RfidSensor
from ..sensors.mcp_3008 import MCP3008

from ..sensors.lcd1602 import lcd

from ..util.logger import log

class SensorManager(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.daemon = True
        self.cleanup = False

        io.setmode(io.BOARD)

    def run(self):
        log.info('SENSR', 'Started')

        self.rfid = RfidSensor(22)

        self.water_level = DistanceSensor(self, 'water_level', 11, 7)
        self.water_level.start()

        self.lcd = lcd(0x39)

        self.mcp3008 = MCP3008()

        self.cleanup = True

        self.loop()

    def loop(self):
        log.info('SENSR', 'Measurement loop started...')

        thread = Thread(target = self.print_ip)
        thread.start()

        thread = Thread(target = self.read_rfid)
        thread.start()

        while True:
            log.info('DISTANCE_SENSOR', f'Getting distance: {self.water_level.get_last_distance()} cm')

            t.sleep(3)

            log.info('PHOTORESISTOR', f'Light level: {self.mcp3008.read(0)}')

            t.sleep(3)

    def print_ip(self):
        self.lcd.lcd_display_string("IP Address:", 1)
        self.lcd.lcd_display_string(get_ip_address('wlan0'), 2)

    def read_rfid(self):
        while True:
            log.info('RFID', 'Waiting for Card')

            id = self.rfid.read_id_no_block()

            if id != None:
                log.info('RFID', f"ID: {id}")
            else:
                log.info('RFID', f"No card to scan. Trying again...")

            t.sleep(5)

    def kill(self):
        if self.cleanup:
            io.cleanup()

        sys.exit()
