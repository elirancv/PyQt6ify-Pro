import sqlite3
from sqlite3 import Error
import logging

def create_connection(db_file):
    """ create a database connection to the SQLite database specified by db_file """
    try:
        conn = sqlite3.connect(db_file)
        logging.info(f"Connected to SQLite database: {db_file}")
        return conn
    except Error as e:
        logging.error(f"Failed to connect to SQLite database: {e}")
        return None

def main():
    database = "my_pyqt_app.db"

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        logging.info("Database is ready for new project setup.")
    else:
        logging.error("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
