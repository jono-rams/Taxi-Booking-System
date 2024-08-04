import sqlite3


class Database:
    def __init__(self):
        self.conn = None

    def connect(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            print(f"Connected to SQLite database {db_name} version {sqlite3.version}")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")

    def close_connection(self):
        print("Closing connection to SQLite database")
        self.conn.close()

    def execute_query(self, query, params=None, fetch_all=False):
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch_all:
                return cursor.fetchall()
            else:
                return cursor.fetchone()

        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

        finally:
            cursor.close()
