from flask_restful import Resource
from flask import request, jsonify
from crm_app.services.userService import *
import jwt
class LoginController(Resource):

    def post(seft):
        print('vào đăng nhập')
        data = request.get_json()
        print(data)
        username = data.get('username')
        password = data.get('password')
        result = login(username=username, password=password)

        return result
    
class GetMeController(Resource):
    def get(seft):
        token = request.headers.get("Authorization")
        result = getMe(token=token)
        return result

class RegisterController(Resource):
    def post(seft):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        result = register(username=username, password=password)

        return result