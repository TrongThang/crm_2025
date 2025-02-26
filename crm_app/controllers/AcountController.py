from flask_restful import Resource
from flask import request, jsonify
from crm_app.services.userService import *

class LoginController(Resource):
    def post(seft):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        result = login(username=username, password=password)

        return result
    
class RegisterController(Resource):
    def post(seft):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        result = register(username=username, password=password)

        return result