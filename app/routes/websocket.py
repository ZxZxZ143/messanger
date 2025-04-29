from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, decode_token
from flask_socketio import send, emit, join_room, leave_room, rooms
from app.extensions import socketio
from app.models.Chat_users import Chat_users
from app.models.Chat import Chat

websocket_bp = Blueprint('websocket', __name__)


@socketio.on('connect')
def handle_connect():
    token = request.args.get("token")  # Получаем заголовок Authorization

    decoded_token = decode_token(token)  # Декодируем токен
    user_id = decoded_token.get("id")

    user_chats = Chat_users.query.filter_by(user_id=user_id).all()

    for chat in user_chats:
        join_room(chat.chat_id)

    join_room(user_id)


@socketio.on('send_message')
def handle_message_send(data):
    print(data)
    socketio.emit("receive_message", {"text": data["text"], "user_id": data["user_id"], "chat_id": data["chat_id"], "message_id": data["message_id"]}, room=data["chat_id"],
                  include_self=False)



@socketio.on('edit_message')
def handle_message_edit(data):
    socketio.emit("edited_message", {"text": data["text"], "user_id": data["user_id"], "chat_id": data["chat_id"], "message_id": data["message_id"]}, room=data["chat_id"],
                  include_self=False)


@socketio.on('join_chat')
def handle_disconnect(data):
    join_room(data["chat_id"])
