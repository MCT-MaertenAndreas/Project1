class Sensor():
    def __init__(self, db):
        self.db = db

    def add_measurement(self, id, value):
        return self.db.execute_sql('INSERT INTO core_measurement (sensor_id, value) VALUES (%s, %s)', [id, value])

    def get_all(self):
        return self.db.get_rows('SELECT * FROM core_sensors')

    def get(self, id):
        return self.db.get_one_row('SELECT * FROM core_sensors WHERE sensor_id=%s', [id])

    def get_measurements(self, id):
        # return max 1 day
        return self.db.get_rows('SELECT * FROM core_measurement WHERE created_on >= DATE(NOW()) - INTERVAL 1 WEEK AND sensor_id=%s ORDER BY measurement_id DESC', [id])
