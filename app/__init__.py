from flask import Flask
from config import Config
from .extensions import db, bcrypt, jwt, socketio
from .routes.contacts import contacts_bp


#создаем фабричную функцию, которая отвечает за инициализацию приложения
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.chats import chats_bp
    from app.routes.websocket import websocket_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chats_bp)
    app.register_blueprint(contacts_bp)

    return app
