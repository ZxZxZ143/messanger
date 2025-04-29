from flask import jsonify
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_socketio import join_room
from pygments.lexers import q

from app.extensions import db, socketio
from ..models.Message_status import Message_status
from ..models.User import Users
from ..models.Chat_users import Chat_users
from ..models.Chat import Chat
from ..models.Message import Message


def send_message_service(request):
    data = request.get_json()
    chat_id = data.get('chat_id')
    message = data.get('message')
    user_id = data.get('sender_id')

    chat = Chat.query.filter_by(id=chat_id).first()

    if chat is None:
        return jsonify({"status": 404, "message": "chat not found"}), 404

    try:
        new_message = Message(
            chat_id=chat_id,
            sender_id=user_id,
            content=message
        )

        db.session.add(new_message)
        db.session.commit()
        message_status = Message_status(
            message_id=new_message.id,
            user_id=user_id,
        )

        db.session.add(message_status)
        db.session.commit()
    except Exception as error:
        db.session.rollback()
        return jsonify({"status": 500, "message": str(error)}), 500

    return jsonify({"status": 200, "message": "success", "chat_id": chat_id, "message_id": new_message.id}), 200


def get_user_messages(request):
    data = request.get_json()
    chat_id = data.get('chat_id')
    response = []
    messages = Message.query.filter_by(chat_id=chat_id).order_by(Message.sent_at.asc()).all()
    for m in messages:
        response.append({"content": m.content, "sender_id": m.sender_id, "message_id": m.id})
    return jsonify({"status": 200, "messages": response}), 200


def get_user_friends(request):
    user_name = get_jwt_identity()
    user_id = Users.query.filter_by(username=user_name).first().id

    user_chats = Chat_users.query.filter_by(user_id=user_id).all()
    response = []
    for c in user_chats:
        is_group = Chat.query.filter_by(id=c.chat_id).first().is_group
        chat_name = Chat.query.filter_by(id=c.chat_id).first().name
        if not is_group:
            second_user_id = Chat_users.query.filter(
                Chat_users.user_id != user_id,
                Chat_users.chat_id == c.chat_id).first().user_id

            chat_name = Users.query.filter_by(id=second_user_id).first().username

        res_part = [chat_name, c.chat_id]

        chats = Chat_users.query.filter_by(chat_id=c.chat_id).all()
        for chat in chats:
            if user_id != chat.user_id:
                username = Users.query.filter_by(id=chat.user_id).first().username
                res_part.append(username)
        response.append(res_part)

    return jsonify({"status": 200, "message": "success", "chats": response}), 200


def get_users_by_username(request):
    current_user = get_jwt_identity()
    user_name = request.get_json().get('username')

    users = Users.query.filter(Users.username.ilike(f"%{user_name}%")).all()
    response = []
    for u in users:
        if u.username != current_user:
            response.append([u.username, u.id])

    if len(response) == 0:
        return jsonify({"status": 404, "message": "user not found"}), 404
    else:
        return jsonify({"status": 200, "message": "success", "users": response}), 200


def create_new_chat(request):
    try:
        user_id = get_jwt().get('id')
        goal_user_id = request.get_json().get('id')

        new_chat = Chat(
            name="chat_name"
        )

        db.session.add(new_chat)
        db.session.commit()

        add_current_user_in_chat = Chat_users(
            chat_id=new_chat.id,
            user_id=user_id
        )

        add_goal_user_in_chat = Chat_users(
            chat_id=new_chat.id,
            user_id=goal_user_id
        )

        db.session.add(add_current_user_in_chat)
        db.session.add(add_goal_user_in_chat)
        db.session.commit()

        chat_name_for_user = Users.query.filter_by(id=goal_user_id).first().username
        chat_name_for_goal_user = Users.query.filter_by(id=user_id).first().username

        socketio.emit('join_chat', {"chat_id": new_chat.id, "chat_name": chat_name_for_goal_user, "user_id": user_id},
                      room=goal_user_id)
        socketio.emit('join_chat', {"chat_id": new_chat.id, "chat_name": chat_name_for_user, "user_id": user_id},
                      room=user_id)

        return jsonify({"status": 200, "message": "chat created", "chat_id": new_chat.id}), 200
    except Exception as e:
        return jsonify({"status": 500, "message": "something went wrong"}), 500


def create_new_group_chat(request):
    try:
        user_id = get_jwt().get('id')
        users = request.get_json().get('users')
        name = request.get_json().get('name')

        new_chat = Chat(
            name=name,
            is_group=True
        )

        db.session.add(new_chat)
        db.session.commit()

        for u in users:
            new_chat_user = Chat_users(
                chat_id=new_chat.id,
                user_id=u
            )

            db.session.add(new_chat_user)

        new_chat_user = Chat_users(
            chat_id=new_chat.id,
            user_id=user_id
        )

        db.session.add(new_chat_user)
        db.session.commit()

        for u in users:
            socketio.emit('join_chat', {"chat_id": new_chat.id, "chat_name": name, "user_id": u},
                          room=u)

        socketio.emit('join_chat', {"chat_id": new_chat.id, "chat_name": name, "user_id": user_id},
                      room=user_id)

        return jsonify({"status": 200, "message": "success", "chat_id": new_chat.id}), 200
    except Exception as e:
        return jsonify({"status": 500, "message": "something went wrong", "error": e}), 500


def edit_message_service(request):
    message_id = int(request.get_json().get('message_id'))
    content = request.get_json().get('content')

    message = Message.query.filter_by(id=message_id).first()

    if message is None:
        return jsonify({"status": 404, "message": "message not found"}), 404

    try:
        message.content = content

        db.session.commit()

        return jsonify({"status": 200, "message": "success", "message_id": message_id, "chat_id": message.chat_id}), 200
    except Exception as e:
        return jsonify({"status": 500, "message": "something went wrong", "error": e}), 500