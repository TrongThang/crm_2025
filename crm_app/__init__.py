from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS
import os 

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
app.secret_key = '@@#*&Y()P2T@@#*@#$#$%^&*('
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/crm_2025?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SWAGGER'] = {
    'title': "API To Do App",
    'uiversion': 3
}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

swagger = Swagger(app)
db = SQLAlchemy(app=app)
