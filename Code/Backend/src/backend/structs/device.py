class Device():
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.get_rows('SELECT * FROM core_devices')

    def get(self, id):
        return self.db.get_one_row('SELECT * FROM core_devices WHERE device_id=%s', [id])

    def get_sensors(self, id):
        return self.db.get_rows('SELECT S.sensor_id, S.device_id, S.hint_name, S.sensor_type as `type`, T.name, K.internal_name as `task_name`, K.name as `task`, K.description as `task_description` FROM core_sensors S INNER JOIN core_sensor_type T ON S.sensor_type=T.sensor_type_id INNER JOIN core_sensor_task K ON S.task_id=K.task_id WHERE device_id=%s', [id])

    def set_reservoir(self, id, reservoir_size):
        return self.db.execute_sql('UPDATE core_devices SET reservoir_size=%s, reservoir_filled=%s WHERE device_id=%s', [reservoir_size, reservoir_size, id])

    def subtract_reservoir(self, id, value):
        return self.execute_sql('UPDATE core_devices SET reservoir_size=reservoir_size-%s WHERE device_id=%s', [value, id])

    def verify_api_token(self, token):
        return self.db.get_one_row('SELECT core_devices.device_id FROM core_devices INNER JOIN core_tokens ON core_devices.token_id=core_tokens.token_id WHERE core_tokens.token=%s AND core_tokens.token_type=2', [token])
