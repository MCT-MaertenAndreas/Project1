from mysql import connector

class Database(object):
    def __init__(self, db_config, debug = False):
        self.config = db_config

        self.debug = debug

    def connect(self):
        try:
            con = connector.connect(**self.config)

            if "AttributeError" in str(type(con)):
                raise Exception("invalid database params in config file")

            cur = con.cursor(dictionary=True, buffered=True)

            return con, cur
        except connector.Error as err:
            if err.errno == connector.errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception('ACCESS_DENIED_ERROR: credentials missmatch')
            elif err.errno == connector.errorcode.ER_BAD_DB_ERROR:
                raise Exception('BAD_DB: unknown database name')
            else:
               raise Exception(err)

    def get_rows(self, sqlQuery, params=None):
        result = None
        con, cur = self.connect()

        try:
            cur.execute(sqlQuery, params)
            result = cur.fetchall()
            if (result is None):
                raise ValueError(f"No results returned for the query {sqlQuery}")
        except Exception as error:
            if self.debug:
                print(error)
            result = None
        finally:
            con.close()
            cur.close()

            return result

    def get_one_row(self, sqlQuery, params=None):
        con, cur = self.connect()

        try:
            cur.execute(sqlQuery, params)
            result = cur.fetchone()

            if (result is None):
                raise ValueError(f"No results returned for the query {sqlQuery}")
        except Exception as error:
            if self.debug:
                print(error)
            result = None
        finally:
            con.close()
            cur.close()

            return result

    def execute_sql(self, sqlQuery, params=None):
        result = None
        con, cur = self.connect()

        try:
            self.execute(sqlQuery, params)
            con.commit()

            result = self.cursor.lastrowid #bevestigig van create (int of 0)
            if result != 0:  # is een insert, deze stuur het lastrowid terug.
                result = result
            else:  # is een update of een delete
                if cur.rowcount == -1:  # Er is een fout in de SQL
                    raise Exception(f'Incorrect SQL syntax, {sqlQuery}')
                elif cur.rowcount == 0:  # Er is niks gewijzigd, where voldoet niet of geen wijziging in de data
                    result = 0
                else:  # Hoeveel rijen werden gewijzigd
                    result = cur.rowcount
        except connector.Error as error:
            con.rollback()
            result = None
            print (f"Error: Data was not saved. {error.msg}")
        finally:
            con.close()
            cur.close()

            return result
