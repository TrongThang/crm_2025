from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS
import os 
import redis

app = Flask(__name__)
CORS(app)

redis_client = redis.Redis(host='172.23.182.206', port=6379)

UPLOAD_FOLDER = 'uploads'
app.secret_key = '@@#*&Y()P2T@@#*@#$#$%^&*('
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/crm_2025?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SWAGGER'] = {
    'title': "API To Do App",
    'uiversion': 3
}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/uploads/<path:folder>/<path:filename>')
# def serve_static(folder, filename):
#     print("folder:", folder)
#     print("filename:", filename)
#     print('path:', (os.path.join(app.config['UPLOAD_FOLDER'], folder), filename))
#     # return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], 'loai_sp'), filename)
#     # return send_from_directory('uploads/loai_sp/', filename)
#     return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER'], folder), filename)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

swagger = Swagger(app)
db = SQLAlchemy(app=app)
