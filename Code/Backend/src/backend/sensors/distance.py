from threading import Thread, Lock

import RPi.GPIO as io
import time as t

from ..util.logger import log

class DistanceSensor(Thread):
    def __init__(self, echo, trig):
        Thread.__init__(self)

        self.lock = Lock()

        self.echo = echo
        self.trig = trig

        self.avg_size = 3

        self.measurements = []

        self.setup()

    def setup(self):
        io.setup(self.trig, io.OUT)
        io.setup(self.echo, io.IN)

        io.output(self.trig, io.LOW)

        log.info('DISTANCE_SENSOR', 'Waiting for sensor to settle...')
        t.sleep(2)

    def run(self):
        while True:
            if self.lock.acquire(False):
                distance = self.get_current_distance()
                if distance != -1:
                    self.measurements.append(distance)
                if len(self.measurements) > self.avg_size:
                    self.measurements.pop(0)
                self.lock.release()
                t.sleep(2)
            else:
                t.sleep(0.001)

    # will instantly calculate the distance given by the sensor
    def get_current_distance(self):
        io.output(self.trig, io.HIGH)
        t.sleep(0.00001)
        io.output(self.trig, io.LOW)

        while io.input(self.echo) == 0:
            start_time = t.time_ns()
        while io.input(self.echo) == 1:
            end_time = t.time_ns()

        try:
            duration = end_time - start_time
        except UnboundLocalError as e:
            return -1
        except Exception as e:
            raise Exception(e)

        return round(duration * 17150 / 1000000000, 2)


    # will give the last known value which was updated async
    def get_last_distance(self):
        if len(self.measurements) < self.avg_size:
            return -1
        while self.lock.acquire(False) == False:
            t.sleep(0.001)
        value = sum(self.measurements) / len(self.measurements)
        self.lock.release()

        return value
