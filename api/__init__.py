from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from api.endpoints import bp
from dotenv import load_dotenv
import os

# Carregar as variáveis de ambiente do arquivo .env.api
load_dotenv('.env.api')

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    user = os.getenv('DB_USER_API', 'default_api_user')
    password = os.getenv('DB_PASSWORD_API', 'default_api_password')
    host = os.getenv('DB_HOST_API', 'veeries.com.br')
    port = int(os.getenv('DB_PORT_API', 3306))
    database = os.getenv('DB_NAME_API', 'veeries')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://{user}:{password}@{host}:{port}/{database}?charset=utf8'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
