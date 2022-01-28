import sqlite3

DB_PATH = 'database.db'

def db_connect():
    """
    Connect to SQLite3 database
    """
    conn = sqlite3.connect(DB_PATH)
    return conn

"""
Select all fields of all rows on given table
"""
def db_select_all(table, fields):
    query = 'SELECT * FROM ' + table
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

"""
Select given fields from all rows on given table
"""
def db_select(table, fields):
    fields_str = ''
    for f in fields:
        fields_str += f + ' '
    query = 'SELECT ' + fields_str + ' FROM ' + table
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
