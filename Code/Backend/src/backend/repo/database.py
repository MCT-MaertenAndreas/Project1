from mysql import connector

class Database(object):
    def __init__(self, db_config, debug = False):
        self.config = db_config

    def connect(self):
        try:
            self.db = connector.connect(**self.config)

            if "AttributeError" in str(type(self.db)):
                raise Exception("invalid database params in config file")

            self.cursor = self.db.cursor(dictionary=True, buffered=True)
        except connector.Error as err:
            if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception('ACCESS_DENIED_ERROR: credentials missmatch')
            elif err.errno == connector.errorcode.ER_BAD_DB_ERROR:
                raise Exception('BAD_DB: unknown database name')
            else:
               raise Exception(err)

    def close(self):
        self.cursor.close()
        self.db.close()

        self.db = None

    @property
    def execute(self):
        return self.cursor.execute

    @property
    def fetchall(self):
        return self.cursor.fetchall

    @property
    def fetchone(self):
        return self.cursor.fetchone

    @property
    def rowcount(self):
        return self.cursor.rowcount

    def get_rows(self, sqlQuery, params=None):
        result = None
        self.connect()

        try:
            self.execute(sqlQuery, params)
            result = self.fetchall()
            if (result is None):
                raise ValueError(f"No results returned for the query {sqlQuery}")
        except Exception as error:
            if debug:
                print(error)
            result = None
        finally:
            self.close()

            return result

    def get_one_row(self, sqlQuery, params=None):
        self.connect()

        try:
            self.execute(sqlQuery, params)
            result = self.fetchone()

            if (result is None):
                raise ValueError(f"No results returned for the query {sqlQuery}")
        except Exception as error:
            if debug:
                print(error)
            result = None
        finally:
            self.close()

            return result

    def execute_sql(self, sqlQuery, params=None):
        result = None
        self.connect()

        try:
            self.execute(sqlQuery, params)
            self.db.commit()

            result = self.cursor.lastrowid #bevestigig van create (int of 0)
            if result != 0:  # is een insert, deze stuur het lastrowid terug.
                result = result
            else:  # is een update of een delete
                if self.rowcount == -1:  # Er is een fout in de SQL
                    raise Exception(f'Incorrect SQL syntax, {sqlQuery}')
                elif self.rowcount == 0:  # Er is niks gewijzigd, where voldoet niet of geen wijziging in de data
                    result = 0
                else:  # Hoeveel rijen werden gewijzigd
                    result = self.rowcount
        except connector.Error as error:
            self.db.rollback()
            result = None
            print (f"Error: Data was not saved. {error.msg}")
        finally:
            self.close()

            return result
