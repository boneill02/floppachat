import sqlite3

DB_PATH = 'database.db'

def db_connect():
    conn = sqlite3.connect(DB_PATH)
    return conn
