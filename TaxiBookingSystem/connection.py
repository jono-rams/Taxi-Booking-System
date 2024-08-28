import sqlite3


class Database:
    def __init__(self):
        self.conn = None

    def connect(self, db_name):
        """
        Connect to the SQLite database specified by the provided db_name.
        :param db_name: path to the database
        :return:
        """
        try:
            self.conn = sqlite3.connect(db_name)
            print(f"Connected to SQLite database {db_name} version {sqlite3.version}")
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite database: {e}")

    def close_connection(self):
        """
        Close the connection to the SQLite database.
        """
        print("Closing connection to SQLite database")
        self.conn.close()

    def execute_query(self, query, params=None, fetch_all=False):
        """
        Execute the provided SQL query with the given parameters.
        :param query: SQL query to be executed
        :param params: tuple of parameters for the query
        :param fetch_all: If True, fetch all rows from the result set, otherwise fetch only first row
        :return: Result of the query or None if an error occurred
        """

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

    def insert_data(self, query, data):
        """
        Insert data into the database using the provided SQL query and parameters.
        :param query: SQL query to be executed
        :param data: tuple of values to be inserted
        :return: True if insertion was successful, False otherwise
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, data)
            self.conn.commit()  # Commit the changes to database
            return True

        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return False

        finally:
            cursor.close()
