from flask_restful import Resource, reqparse
from db import *

class Users(Resource):
    def __init__(self):
        self.table = 'users'
        self.fields = [ 'user_id', 'username', 'email', 'pass' ]
        self.create_table()

    def create_table(self):
        """
        Creates the users table in the SQLite database
        """
        try:
            conn = db_connect()
            conn.execute('''
                CREATE TABLE users (
                    user_id INTEGER PRIMARY KEY NOT NULL,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    pass TEXT NOT NULL
                );''')
    
            conn.commit()
            print('Successfully created users table')
        except:
            print('Failed to create users table')
        finally:
            conn.close()

    def get(self):
        """
        Returns all users (invoked in HTTP GET request for /users)
        """
        return db_select_all(self.table, self.fields)

    def get_user_by_id(self, uid): # TODO make generic function in db.py for this
        """
        Returns user with user_id=uid
        """
        query = 'SELECT * FROM ' + self.table + 'WHERE user_id = ' + uid
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
            for f in self.fields:
                contents[f] = row[f]
            res.append(row)
        return res

    def insert_user(self, user):
        """
        Inserts user with the given attributes
        """
        inserted_user = {}
        conn = db_connect()
        try:
            cur = conn.cursor()
            cur.execute('INSERT INTO users (username, email, pass) VALUES (?, ?, ?)',
                    (user['username'], user['email'], user['pass']))
            conn.commit()
            uid = cur.lastrowid
            inserted_user = self.get_user_by_id(uid)
        except:
            print('Failed to insert user')
        finally:
            conn.close()

        return inserted_user

    def post(self):
        """
        Adds a user (invoked in HTTP POST request for /users)
        """
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('pass', required=True)
        args = parser.parse_args()

        new_user = {
            'username': args['username'],
            'email': args['email'],
            'pass': args['pass']
        }

        result = self.insert_user(new_user)

        if result == {}:
            return {'data': {}}, 500
        else:
            data = self.get_user_by_id(result[0]['user_id'])
            return {'data': data}, 200
