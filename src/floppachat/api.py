from flask import Flask
from flask_restful import Api

import users, messages

class ChatAPI:
    def __init__(self):
        users.Users.create_table()
        pass
    def run(self):
        app = Flask('FloppaChat')
        api = Api(app)
        api.add_resource(users.Users, '/users')
        api.add_resource(messages.Messages, '/messages')
        app.run()
