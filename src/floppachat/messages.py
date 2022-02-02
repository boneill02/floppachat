from flask_restful import Resource, reqparse
from db import *

class Messages(Resource):
    def __init__(self):
        self.table = 'messages'
        self.fields = [ 'msg_id', 'sender_id', 'room_id', 'top', 'bottom', 'img_url' ]
        self.create_table()

    def create_table(self):
        """
        Creates the messages table in the SQLite database
        """
        conn = db_connect()
        try:
            conn.execute('''
    	        CREATE TABLE messages (
    	            msg_id INTEGER PRIMARY KEY NOT NULL,
    	            sender_id INTEGER NOT NULL,
    	            room_id INTEGER NOT NULL,
    	            top TEXT NOT NULL,
    	            bottom TEXT NOT NULL,
    	            img_url TEXT NOT NULL
    	        );''')
            conn.commit()
        except:
            pass
        conn.close()

    def get(self):
        """
        Returns all messages (invoked in HTTP GET request for /messages)
        """
        parser = reqparse.RequestParser()
        parser.add_argument('msg_id', required=False)
        parser.add_argument('room_id', required=False)
        args = parser.parse_args()

        if args['msg_id'] != None:
            return db_select(self.table, None, 'msg_id = ' + args['msg_id'])
        if args['room_id'] != None:
            return db_select(self.table, None, 'room_id = ' + args['room_id'])
        return db_select(self.table)
    
    def get_msg_by_id(self, mid):
        return db_select(self.table, None, 'msg_id = ' + str(mid))

    def insert_message(self, msg):
        """
        Inserts message with the given attributes
        """
        conn = db_connect()
        cur = conn.cursor()
        cur.execute('INSERT INTO messages (sender_id, room_id, top, bottom, img_url) VALUES (?, ?, ?, ?, ?)',
                (msg['sender_id'], msg['room_id'], msg['top'], msg['bottom'], msg['img_url']))
        conn.commit()
        uid = cur.lastrowid
        inserted_msg = self.get_msg_by_id(uid)

        return inserted_msg

    def post(self):
        """
        Adds a message (invoked in HTTP POST request for /messages)
        """
        parser = reqparse.RequestParser()
        parser.add_argument('sender_id', required=True)
        parser.add_argument('room_id', required=True)
        parser.add_argument('top', required=True)
        parser.add_argument('bottom', required=True)
        parser.add_argument('img_url', required=True)
        args = parser.parse_args()
        print(args)

        new_msg = {
            'sender_id': args['sender_id'],
            'room_id': args['room_id'],
            'top': args['top'],
            'bottom': args['bottom'],
            'img_url': args['img_url']
        }

        result = self.insert_message(new_msg)

        if result == {}:
            return {'data': {}}, 500
        else:
            data = self.get()
            return {'data': data}, 200
