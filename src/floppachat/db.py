import sqlite3

DB_PATH = 'database.db'

def db_connect():
    """
    Connect to SQLite3 database
    """
    conn = sqlite3.connect(DB_PATH)
    return conn

def db_select(table, fields):
    query = 'SELECT * FROM ' + table # TODO reformat query to select given fields only
    conn = db_connect()
    cur = conn.cursor()
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute(query)
        data = self.cur_to_dict(cur)
    except:
        print('Failed to execute query: ' + query)
        return {'data': {}}, 500
    finally:
        conn.close()

    res = []
    rows = cur.fetchall()
    print(rows)
    for row in rows:
        contents = {}
        for f in fields:
            contents[f] = row[f]
        res.append(row)
    return res
