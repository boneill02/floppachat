from flask_restful import Resource, reqparse
from db import *

class Users(Resource):
    def create_table():
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

    def get(self):
        """
        Returns all users (invoked in HTTP GET request for /users)
        """
        data = {}
        conn = db_connect()
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users')
            data = self.cur_to_dict(cur)
        except:
            print('Failed to pull all users from database')
            return {'data': {}}, 500
        finally:
            conn.close()

        return {'data': data}, 200

    def get_user_by_id(self, uid):
        user = {}
        conn = db_connect()
        conn.row_factory = sqlite3.Row
        try:
            cur = conn.cursor()
            cur.execute('SELECT * FROM users WHERE user_id = ?', (uid,))
            user = self.cur_to_dict(cur)
        except:
            print('Failed to retrieve user with id ' + uid)
        finally:
            conn.close()
        
        return user

    def insert_user(self, user):
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
