from flask import Flask
from flask_restful import Api

import users, messages

# create tables
users.Users.create_table()

# Initialize API
app = Flask('FloppaChat')
api = Api(app)
api.add_resource(users.Users, '/users')
api.add_resource(messages.Messages, '/messages')

if __name__ == '__main__':
    app.run()

