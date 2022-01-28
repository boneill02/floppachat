from flask_restful import Resource

class Messages(Resource):
    def __init__(self):
        self.table = 'messages'
        self.fields = [ 'msg_id', 'sender_id', 'room_id', 'top', 'bottom', 'img_url' ]
        self.create_table()

    def create_table(self):
        """
        Creates the messages table in the SQLite database
        """
        try:
            conn = db_connect()
            conn.execute('''
	            CREATE TABLE messages (
	                msg_id INTEGER PRIMARY KEY NOT NULL,
	                sender_id INTEGER NOT NULL,
	                room_id INTEGER NOT NULL,
	                top TEXT NOT NULL
	                bottom TEXT NOT NULL
	                img_url TEXT NOT NULL
	            );''')

            conn.commit()
            print('Successfully created messages table')
        except:
            print('Failed to create messages table')
        finally:
            conn.close()

    def get(self):
        """
        Returns all messages (invoked in HTTP GET request for /messages)
        """
        return db_select_all(self.table, self.fields)
