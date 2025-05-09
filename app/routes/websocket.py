from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt, decode_token, verify_jwt_in_request, get_jwt_identity
from flask_socketio import send, emit, join_room, leave_room, rooms
from app.extensions import socketio
from app.models.Chat_users import Chat_users
from app.models.Chat import Chat

websocket_bp = Blueprint('websocket', __name__)


@socketio.on('connect')
def handle_connect():
    verify_jwt_in_request()

    user_id = get_jwt().get('id')

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
