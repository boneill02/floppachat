import sqlite3

DB_PATH = 'database.db'

def db_connect():
    """
    Connect to SQLite3 database
    """
    conn = sqlite3.connect(DB_PATH)
    return conn
