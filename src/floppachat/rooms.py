from flask_restful import Resource, reqparse
from db import *

class Rooms(Resource):
    def __init__(self):
        self.table = 'rooms'
        self.fields = [ 'room_id', 'users' ]
        self.create_table()

    def create_table(self):
        """
        Creates the rooms table in the SQLite database
        """
        conn = db_connect()
        try:
            conn.execute('''
    	        CREATE TABLE rooms (
    	            room_id INTEGER PRIMARY KEY NOT NULL,
    	            users TEXT NOT NULL
    	        );''')
            conn.commit()
        except:
            pass
        conn.close()

    def get(self):
        """
        Returns all rooms (invoked in HTTP GET request for /rooms)
        """
        parser = reqparse.RequestParser()
        parser.add_argument('room_id', required=False)
        args = parser.parse_args()

        if args['room_id'] != None:
            return get_room_by_id(args['room_id'])

        return db_select(self.table, None, None)
    
    def get_room_by_id(self, rid):
        return db_select(self.table, None, 'room_id = ' + str(rid))

    def insert_room(self, room):
        """
        Creates a room with the given attributes
        """
        conn = db_connect()
        cur = conn.cursor()
        cur.execute('INSERT INTO rooms (users) VALUES (?)', (room['users']))
        conn.commit()
        uid = cur.lastrowid
        inserted_msg = self.get_room_by_id(uid)

        return inserted_msg

    def post(self):
        """
        Adds a message (invoked in HTTP POST request for /rooms)
        """
        parser = reqparse.RequestParser()
        parser.add_argument('users', required=True)
        args = parser.parse_args()
        print(args)

        new_room = {
            'users': args['users']
        }

        result = self.insert_room(new_room)

        if result == {}:
            return {'data': {}}, 500
        else:
            data = self.get()
            return {'data': data}, 200
