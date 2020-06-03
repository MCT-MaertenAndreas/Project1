class Device():
    def __init__(self, db):
        self.db = db

    def get_all(self):
        return self.db.get_rows('SELECT * FROM core_devices')

    def get(self, id):
        return self.db.get_one_row('SELECT * FROM core_devices WHERE device_id=%s', [id])

    def get_sensors(self, id):
        return self.db.get_rows('SELECT S.sensor_id, S.device_id, S.hint_name, T.name, K.name as `task`, K.description as `task_description` FROM core_sensors S INNER JOIN core_sensor_type T ON S.sensor_type=T.sensor_type_id INNER JOIN core_sensor_task K ON S.task_id=K.task_id WHERE device_id=%s', [id])
