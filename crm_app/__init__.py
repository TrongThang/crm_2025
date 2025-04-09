from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from flask_cors import CORS
import os 
import redis # 172.23.182.206

app = Flask(__name__)
CORS(app, supports_credentials=True)

import time

def connect_redis():
    while True:
        try:
            redis_host = os.getenv('REDIS_HOST', 'localhost')  # Mặc định là localhost
            client = redis.Redis(host=redis_host, port=6379)
            client.ping()
            print("Connected to Redis")
            return client
        except redis.ConnectionError:
            print("Waiting for Redis...")
            time.sleep(1)

redis_client = connect_redis()

UPLOAD_FOLDER = 'uploads'
app.secret_key = '@@#*&Y()P2T@@#*@#$#$%^&*('
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/crm_2025?charset=utf8mb4'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db_host = os.getenv('DB_HOST', 'mysql')  # Mặc định là localhost
db_password = os.getenv('DB_PASSWORD', '')  # Mặc định là không
db_user = os.getenv('DB_USER', 'root')  # Mặc định là root
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/crm_2025?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SWAGGER'] = {
    'title': "API CRM APP 2025",
    'uiversion': 3
}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

swagger = Swagger(app, template_file='main.yaml')
# swagger = Swagger(app, template_file='./docs/swaggers/main.yaml')
db = SQLAlchemy(app=app)

def wait_for_db():
    while True:
        try:
            db.session.execute('SELECT 1')
            print("MySQL connected")
            break
        except Exception as e:
            print(f"Waiting for MySQL: {e}")
            time.sleep(1)

wait_for_db()