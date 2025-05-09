from flask import Flask
from flask_mail import Mail

from config import Config
from .extensions import db, bcrypt, jwt, socketio
from .routes.contacts import contacts_bp


#создаем фабричную функцию, которая отвечает за инициализацию приложения
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'kyrlukov205@gmail.com'
    app.config['MAIL_PASSWORD'] = 'zydg ddvc uwjo lrfs'  # не обычный пароль, а сгенерированный "App password"
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@example.com'

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    mail = Mail(app)

    from app.routes.auth import auth_bp
    from app.routes.chats import chats_bp
    from app.routes.websocket import websocket_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(chats_bp)
    app.register_blueprint(contacts_bp)

    return app
