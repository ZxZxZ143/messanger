from flask import Blueprint
from .auth import auth_bp
from .chats import chats_bp
from .websocket import websocket_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(chats_bp, url_prefix="")
    app.register_blueprint(websocket_bp, url_prefix="/websocket")
