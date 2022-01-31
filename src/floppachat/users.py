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
        conn = db_connect()
        try:
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
            if conn != None:
                conn.close()

    def get(self):
        """
        Returns all users (invoked in HTTP GET request for /users)
        """
        return db_select(self.table)

    def get_user_by_id(self, uid):
        return db_select(self.table, None, 'user_id = ' + str(uid))

    def insert_user(self, user):
        """
        Inserts user with the given attributes
        """
        inserted_user = {}
        conn = db_connect()
        cur = conn.cursor()
        cur.execute('INSERT INTO users (username, email, pass) VALUES (?, ?, ?)',
                (user['username'], user['email'], user['pass']))
        conn.commit()
        uid = cur.lastrowid
        inserted_user = self.get_user_by_id(uid)

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
            data = self.get()
            return {'data': data}, 200
