import sqlite3

DB_PATH = 'database.db'

def cur_to_dict(self, cur):
    """
    Helper function to convert data in SQLite cursor to a dictionary
    """
    res = []
    rows = cur.fetchall()
    print(rows)
    for row in rows:
        user = {}
        user['user_id'] = row['user_id']
        user['username'] = row['username']
        user['email'] = row['email']
        user['pass'] = row['pass']
        res.append(user)
    return res

def db_connect():
    """
    Connect to SQLite3 database
    """
    conn = sqlite3.connect(DB_PATH)
    return conn

def db_select(table, fields=None, where=None):
    query = 'SELECT '
    if fields == None:
        query += '* '
    else:
        query += fields

    query += 'FROM ' + table + ' '

    if where != None:
        query += 'WHERE ' + where

    conn = db_connect()
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    print(query)
    cur.execute(query)

    res = []
    rows = cur.fetchall()
    for row in rows:
        print(row)
        contents = {}
        for f in row.keys():
            contents[f] = row[f]
        res.append(contents)
    conn.close()
    return res
