from flask import Flask, request
from flask_restx import Resource, Api, reqparse
import os, json, yaml, sys

app = Flask(__name__)
api = Api(app, \
        doc='/docs',
        version='1.0', 
        title='RO-Crate general API', 
        description='Simple API features to explore and make ROCrate',
        default="rocrate",
        default_label="general commands")

projects_types = {}

profiles = api.namespace('profiles', description='profile commands')
spaces = api.namespace('spaces', description='spaces commands')
plugins = api.namespace('plugins', description='plugin commands')

@spaces.route('/')
class Spaces(Resource):
    def get(self):
        with open(os.path.join(os.getcwd(),"projects.json"), "r+") as file:
            data = json.load(file)
            return data,200

@spaces.route('/<string:space_id>')
class Space(Resource):
    def get(self, space_id):
        with open(os.path.join(os.getcwd(),"projects.json"), "r+") as file:
            data = json.load(file)
            try:
                toreturn = data[space_id]
                return toreturn
            except Exception as e:
                return {'message':e},400
    
    def delete(self, space_id):
        with open(os.path.join(os.getcwd(),"projects.json")) as data_file:
            data = json.load(data_file)
            try:
                del data[space_id]
            except Exception as e:
                return {'message':e},400    
        with open(os.path.join(os.getcwd(),"projects.json"), 'w') as data_file:
            data = json.dump(data, data_file)    
            return {'message':'successfully deleted profile'},200 
    
    parser = reqparse.RequestParser()
    parser.add_argument('file_path', type=str, help='Local file path where project is located', required=True)
    parser.add_argument('RO-Profile', type=str, help='Name of ro profile the project will conform to', required=True)

    @spaces.doc(parser=parser)
    def put(self, space_id):
        json_data = request.args
        print(json_data)
        try:
            name = space_id
            roprofile = json_data.get("RO-Profile")
            path_project = json_data.get("file_path")
            entry = {name:{"ro_profile":roprofile,"local_path":path_project}}
            # 1. Read file contents
            with open(os.path.join(os.getcwd(),"projects.json"), "r+")as file:
                data = json.load(file)
                print(data, file=sys.stdout)
                # 2. Update json object
                data.update(entry)
                print(data, file=sys.stdout)
            # 3. Write json file
            with open(os.path.join(os.getcwd(),"projects.json"), "w") as file:
                json.dump(data, file)
            
            return {'message':'entry successfully added'},200
        except Exception as e:
            return {'message':e},400

@api.route('/')
class Home(Resource):
    def get(self):
        return {'message': 'general comand return'},200

@profiles.route('/')
class Profiles(Resource):
    def get(self):
        with open(os.path.join(os.getcwd(),"workflows.json"), "r+") as file:
            data = json.load(file)
            return data,200

@profiles.route('/<string:profile_id>')
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
    parser.add_argument('logo', type=str, help='url for the logo of the profile')
    parser.add_argument('url RO-profile', type=str, help='url to find the ro-profile', required=True)

    @api.doc(parser=parser)
    def put(self, profile_id):
        json_data = request.args
        print(json_data)
        try:
            name = profile_id
            roprourl = json_data.get("url RO-profile")
            try:
                logo = json_data.get("logo")
            except:
                logo = "https://www.researchobject.org/ro-crate/assets/img/ro-crate-w-text.svg"
            entry = {name:{"roprourl":roprourl,"url":logo}}
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

@plugins.route('/')
class Home(Resource):
    def get(self):
        return {'message': 'todo'},200



if __name__ == '__main__':
    app.run(debug=True)