from flask_restful import Resource, reqparse
import pandas as pd

DB_PATH = 'db/users.csv'

class Users(Resource):
    # returns all users
    def get(self):
        data = pd.read_csv(DB_PATH).to_dict()
        return {'data': data}, 200

    # add a user (id, username)
    def post(self):
        # parse args
        parser = reqparse.RequestParser()
        parser.add_argument('id', required=True)
        parser.add_argument('username', required=True)
        args = parser.parse_args()

        # add to dataframe
        new_data = pd.DataFrame([{
            'id': args['id'],
            'username': args['username'],
        }])
        data = pd.read_csv(DB_PATH)
        data = data.append(new_data, ignore_index=True)

        data.to_csv(DB_PATH, index=False)
        return {'data': data.to_dict()}, 200
