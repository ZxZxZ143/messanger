from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

#устанавливаем небходимые расширения
socketio = SocketIO(cors_allowed_origins="*")
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()