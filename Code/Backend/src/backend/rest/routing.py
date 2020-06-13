from flask import Flask
from flask import request
from flask import jsonify
import logging

from .http_response_codes import error_code, success_code

from ..structs.user import User
from ..structs.device import Device
from ..structs.sensor import Sensor

from ..func import get_ip_address
from ..util.logger import log

class Routing():
    def __init__(self, main, debug = False):
        self.main = main
        self.debug = debug

        self.device = Device(main.db)
        self.sensor = Sensor(main.db)

        self.app = Flask(__name__)

    @property
    def user_utils(self):
        return self.main.user_utils

    def start(self):
        (logging.getLogger('werkzeug')).setLevel(logging.ERROR)

        self.setup()

        self.app.run()

    def setup(self):
        @self.app.errorhandler(404)
        def not_found(e):
            return error_code[404]

        @self.app.errorhandler(405)
        def method_not_allowed(e):
            return error_code[405]

        @self.app.route('/')
        def root():
            return error_code[403]

        @self.app.route('/api/v1/status/ip/', methods=['GET'])
        def get_ip():
            return jsonify(ip=get_ip_address())

        @self.app.route('/api/v1/auth/login/', methods=['POST'])
        def login():
            user = request.json['user']
            password = request.json['password']

            log('REST', 'INFO', f'User authenticating: "{user}"')

            row = self.main.db.get_one_row('SELECT user_id, username, password FROM core_users WHERE username=%s OR email=%s', [user, user])

            if row == None:
                log('REST', 'WARN', f'Attempted login with unknown credentials.')
                return jsonify(status="failed", message="Invalid username, email and/or password.")

            if self.user_utils.verify_password(row['password'], password) == False:
                log('REST', 'WARN', f'Attempted login but password check failed.')
                return jsonify(status="failed", message="Invalid username, email and/or password.")

            token = self.user_utils.create_session(row['user_id'])

            if token == -1:
                return error_code[500]

            log('REST', 'INFO', f'User Authorized: {row["username"]}')
            return jsonify(status='success', message=f'Welcome back {row["username"]}', data={'token': token})

        @self.app.route('/api/v1/auth/session/', methods=['GET'])
        def verify_session():
            token = request.headers.get('Authorization')

            if token == None:
                return error_code[401]

            return jsonify(data={'status': self.user_utils.check_token(token)})

        @self.app.route('/api/v1/auth/logout/', methods=['DELETE'])
        def destroy_session():
            token = request.json['token']

            self.user_utils.destroy_session(token)

            return success_code[204]

        @self.app.route('/api/v1/users/register/', methods=['POST'])
        def register():
            token = request.json['token']
            user = request.json['user']

            if (self.user_utils.check_token(token)):
                self.user_utils.create_user(user)

                log('REST', 'INFO', f'New registered user: {user["name"]}, {user["email"]}')

                return success_code[204]

            return error_code[401]

        @self.app.route('/api/v1/sensors/', methods=['GET'])
        def sensor():
            sensors = self.sensor.get_all()
            return jsonify(sensors)

        @self.app.route('/api/v1/sensors/<int:sensor_id>/', methods=['GET'])
        def sensors(sensor_id=-1):
            if sensor_id == -1:
                return error_code[400]

            if request.method == 'GET':
                sensor = self.sensor.get(sensor_id)

                return jsonify(sensor)

            return success_code[204]

        @self.app.route('/api/v1/sensors/<int:sensor_id>/measurements/', methods=['GET', 'POST'])
        def measurements(sensor_id):
            if request.method == 'GET':
                return jsonify(self.sensor.get_measurements(sensor_id))

            id = request.json['sensor_id']
            value = request.json['value']

            self.sensor.add_measurement(id, value)

            return success_code[204]

        @self.app.route('/api/v1/devices/', methods=['GET', 'POST'])
        def devices():
            if request.method == 'GET':
                devices = self.device.get_all()
                return jsonify(devices)

            # POST request
            token = request.headers.get('Authorization')
            if token == None:
                return error_code[401]

            device_id = self.device.verify_api_token(token)

            if device_id == None:
                return jsonify(device_id=-1)
            return jsonify(device_id)

        @self.app.route('/api/v1/devices/<int:device_id>/', methods=['GET', 'PUT'])
        def device(device_id=-1):
            if device_id == -1:
                return error_code[400]

            if request.method == 'GET':
                device = self.device.get(device_id)

                if device == None:
                    return error_code[404]
                return jsonify(device)

            value = request.json.get('decline')

            if value == None:
                reservoir_size = request.json.get('reservoir_size')

                self.device.set_reservoir(device_id, reservoir_size)
            else:
                print(device_id, value)
                self.device.subtract_reservoir(device_id, value)

            return success_code[204]

        @self.app.route('/api/v1/devices/<int:device_id>/sensors/', methods=['GET', 'POST'])
        def device_sensors(device_id=-1):
            if request.method == 'GET':
                if device_id == -1:
                    return error_code[400]

                sensors = self.device.get_sensors(device_id)

                return jsonify(sensors)

            return error_code[405]
