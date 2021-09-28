from flask import Flask, request
from flask_restx import Resource, Api, reqparse
import os, json, yaml, sys

app = Flask(__name__)
api = Api(app, doc='/docs')

projects_types = {}






@api.route('/')
class Home(Resource):
    def get(self):
        return {'redirect': 'home'}

@api.route('/profiles')
class Profiles(Resource):
    def get(self):
        with open(os.path.join(os.getcwd(),"workflows.json"), "r+") as file:
            data = json.load(file)
            return data

@api.route('/profiles/<string:profile_id>')
class Profile(Resource):
    def get(self, profile_id):
        with open(os.path.join(os.getcwd(),"workflows.json"), "r+") as file:
            data = json.load(file)
            try:
                toreturn = data[profile_id]
                return toreturn
            except Exception as e:
                return {'message':e},400
    
    def delete(self, profile_id):
        with open(os.path.join(os.getcwd(),"workflows.json")) as data_file:
            data = json.load(data_file)
            try:
                del data[profile_id]
            except Exception as e:
                return {'message':e},400    
        with open(os.path.join(os.getcwd(),"workflows.json"), 'w') as data_file:
            data = json.dump(data, data_file)    
            return {'message':'successfully deleted profile'},200 

    parser = reqparse.RequestParser()
    parser.add_argument('logo', type=str, help='url for the logo of the profile', required=True)

    @api.doc(parser=parser)
    def put(self, profile_id):
        json_data = request.args
        print(json_data)
        try:
            name = profile_id
            print(name, file=sys.stdout)
            logo = json_data.get("logo")
            print(logo, file=sys.stdout)
            entry = {name:{"url":logo}}
            print(entry, file=sys.stdout)
            # 1. Read file contents
            with open(os.path.join(os.getcwd(),"workflows.json"), "r+")as file:
                data = json.load(file)
                print(data, file=sys.stdout)
                # 2. Update json object
                data.update(entry)
                print(data, file=sys.stdout)
            # 3. Write json file
            with open(os.path.join(os.getcwd(),"workflows.json"), "w") as file:
                json.dump(data, file)
            
            return {'message':'entry successfully added'},200
        except Exception as e:
            return {'message':e},400


if __name__ == '__main__':
    app.run(debug=True)