from threading import Thread, Lock
import sys

import requests
import time as t

import RPi.GPIO as io

from ...config import rest
from ..func import get_ip_address

from ..sensors.basic_io_device import BasicIODevice

from ..sensors.distance import DistanceSensor
from ..sensors.rfid_rc522 import RfidSensor
from ..sensors.mcp_3008 import Mcp

from ..sensors.lcd1602 import lcd

from ..util.logger import log

class SensorManager(Thread):
    def __init__(self):
        Thread.__init__(self)

        self.daemon = True
        self.cleanup = False

        self.lock = Lock()

        self.authorized = False
        self.case_open = False
        self.last_state = not self.case_open

        self.cup_detected = False
        self.cup_tick = 0
        self.cup_last_tick = t.time() + 1

        self.case_open_update = 0
        self.pump_start_time = 0
        self.pump_update_time = 0
        self.case_check = 0
        self.lcd_buffer_update = 0

        io.setmode(io.BOARD)

    def register(self):
        headers = { 'Authorization': rest['token'] }

        res = requests.post(f"{rest['host']}/api/v1/devices/", headers=headers)
        json = res.json()

        res = requests.get(f"{rest['host']}/api/v1/devices/{json['device_id']}/")
        json = res.json()

        self.device = json

        log.info('DEVICE', f"Registered device with ID: {json['device_id']}")

        res = requests.get(f"{rest['host']}/api/v1/devices/{json['device_id']}/sensors/")
        json = res.json()

        self.sensors = json

    def getSensorIdByTypeAndTask(self, type, task):
        for sensor in self.sensors:
            if sensor['task_name'] == task and sensor['type'] == type:
                return sensor['sensor_id']
        return None

    def update_reservoir(self):
        self.device['reservoir_size'] -= 100

        #self.set_lcd_buffers("Reservoir Size:", self.device['reservoir_size'])

        headers = {
            'Authorization': rest['token'],
            'Content-Type': 'application/json'
        }
        data = {
            'decline': 100
        }

        res = requests.put(f"{rest['host']}/api/v1/devices/{self.device['device_id']}/", headers=headers, json=data)

    def upload_measurement(self, sensor_id, value):
        headers = {
            'Authorization': rest['token'],
            'Content-Type': 'application/json'
        }
        data = {
            'sensor_id': sensor_id,
            'value': value
        }

        res = requests.post(f"{rest['host']}/api/v1/sensors/{sensor_id}/measurements/", headers=headers, json=data)

    def run(self):
        log.info('SENSR', 'Started')

        self.register()

        self.buzzer = BasicIODevice(35, io.OUT)
        self.buzzer.id = self.getSensorIdByTypeAndTask(10, 'alarm')

        self.pump = BasicIODevice(40, io.OUT)
        self.pump.id = self.getSensorIdByTypeAndTask(8, 'pump')

        self.led = {
            'red': BasicIODevice(38, io.OUT),
            'blue': BasicIODevice(36, io.OUT),
            'green': BasicIODevice(32, io.OUT)
        }

        self.rfid = RfidSensor(22)
        self.rfid.id = self.getSensorIdByTypeAndTask(6, 'tag_reader')

        self.cup_detector = DistanceSensor(11, 7)
        self.cup_detector.start()
        self.cup_detector.id = self.getSensorIdByTypeAndTask(5, 'movement_detection')

        self.lcd = lcd(0x39)

        self.mcp3008 = Mcp(device=1)
        self.mcp3008.setup()
        self.mcp3008.id = self.getSensorIdByTypeAndTask(9, 'case_open')

        self.cleanup = True

        self.set_lcd_buffers("IP Address:", get_ip_address())

        self.loop()

    def loop(self):
        thread = Thread(target = self.read_rfid)
        thread.start()

        while True:
            while self.lock.locked():
                t.sleep(0.0001)
            self.lock.acquire()

            if t.time() - self.lcd_buffer_update >= 15:
                self.set_lcd_buffers("IP Address:", get_ip_address())

            self.check_case_open()

            self.check_cup()

            self.fill_cup_tick()

            self.lock.release()
            t.sleep(0.01)

    def check_case_open(self):
        if t.time() - self.case_check < 1:
            return
        else:
            self.case_check = t.time()

        light_level = self.mcp3008.read_channel(0)

        if light_level > 75:
            if not self.case_open:
                self.case_open = True
                self.case_open_time = t.time()

            if t.time() - self.case_open_time > 10 and not self.authorized:
                self.buzzer.enable()

                self.set_lcd_buffers("   Case Open", "     !!!!!")

        else:
            self.authorized = False

            self.case_open = False
            self.case_open_time = 0
            self.buzzer.disable()

        if self.last_state != self.case_open:
            log.info('CASE_STATE', f'Open: {self.case_open}')

            self.last_state = self.case_open

        if t.time() - self.case_open_update >= 1:
            self.upload_measurement(self.mcp3008.id, light_level)

            self.upload_measurement(self.buzzer.id, self.case_open)

            self.case_open_update = t.time()

    def check_cup(self):
        distance = self.cup_detector.get_last_distance()

        if distance == -1:
            return

        if distance <= 7.5:
            if t.time() - self.cup_last_tick >= 5 and self.device['reservoir_size'] > 0:
                self.cup_detected = True

                log.info('PUMP', 'Enabling...')

        elif self.pump.state:
            self.pump.disable()

        if t.time() - self.pump_update_time >= 1:
            self.upload_measurement(self.pump.id, self.pump.state)

            self.upload_measurement(self.cup_detector.id, distance)

            self.pump_update_time = t.time()

    def fill_cup_tick(self):
        if self.cup_detected:
            if self.cup_tick == 0:
                self.set_lcd_buffers('Filling cup...', 'Don\'t remove!')

                self.cup_last_tick = t.time() - 1
            self.pump.enable()

            if self.cup_tick >= 60:
                log.info('PUMP', 'Done filling, stopping...')

                self.pump.disable()

                self.update_reservoir()

                self.set_lcd_buffers('For more', 'keep cup, 5 sec.')

                self.cup_detected = False
                self.cup_tick = 0
                self.cup_last_tick = t.time() + 1

            if t.time() - self.cup_last_tick >= 1:
                log.info('PUMP', f"Tick: {self.cup_tick}")

                self.cup_tick += int(t.time() - self.cup_last_tick)
                self.cup_last_tick = t.time()


    def set_lcd_buffers(self, a1, a2):
        condition = True

        buffer = []

        if not isinstance(a1, str) or not isinstance(a2, str):
            buffer = ["Invalid", "Buffer"]
        else:
            buffer = [a1, a2]

        self.set_lcd_info(*buffer)

        self.lcd_buffer_update = t.time()


    def set_lcd_info(self, a1, a2):
        if self.pump.state:
            return

        self.lcd.lcd_write(0x01)

        self.lcd.lcd_display_string(a1, 1)
        self.lcd.lcd_display_string(a2, 2)

    def read_rfid(self):
        while True:
            log.info('RFID', 'Waiting for Card')

            id = self.rfid.read_id_no_block()

            if id != None:
                log.info('RFID', f"ID: {id}")

                self.buzzer.disable()

                while self.lock.locked():
                    t.sleep(0.00001)
                self.lock.acquire()

                self.case_open = False
                self.authorized = True

                self.lock.release()
            else:
                log.info('RFID', f"No card to scan. Trying again...")

            t.sleep(1)

    def kill(self):
        if self.cleanup:
            io.cleanup()

        sys.exit()
