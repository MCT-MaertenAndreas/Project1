import requests

class BaseSensor():
    def __init__(self, manager, sensor_code, task_type):
        self.manager = manager

        self.sensor_code = sensor_code
        self.task_type = task_type

        self.register()

    def register(self):
        print('Registering sensor')

        req = requests.post('http://localhost/api/v1/sensors/', data={ 'code':self.sensor_code, 'task_type': self.task_type })
