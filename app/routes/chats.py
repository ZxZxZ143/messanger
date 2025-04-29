from flask_jwt_extended import jwt_required
from flask import blueprints, Blueprint, request, render_template
from ..services.chat_service import get_user_messages, send_message_service, get_user_friends, get_users_by_username, \
    create_new_chat, create_new_group_chat, edit_message_service

chats_bp = Blueprint('chats', __name__, url_prefix='')


@chats_bp.route('/home', methods=['GET'])
@chats_bp.route('/', methods=['GET'])
def homePage():
    return render_template(template_name_or_list="home.html")


@chats_bp.route('/create_chat', methods=['GET'])
def create_chats():
    return render_template(template_name_or_list="new_chat.html")

@chats_bp.route('/get_friends', methods=['POST'])
@jwt_required()
def get_friends():
    return get_user_friends(request)


@chats_bp.route('/send_message', methods=['POST'])
@jwt_required()
def send_message():
    return send_message_service(request=request)


@chats_bp.route("/get_message", methods=["POST"])
@jwt_required()
def get_message():
    return get_user_messages(request=request)


@chats_bp.route("/find_friends", methods=["POST"])
@jwt_required()
def find_friends():
    return get_users_by_username(request=request)


@chats_bp.route("/create_new_chat", methods=["POST"])
@jwt_required()
def create_chat():
    return create_new_chat(request=request)

@chats_bp.route("/create_new_group_chat", methods=["POST"])
@jwt_required()
def create_new_group_chats():
    return create_new_group_chat(request=request)

@chats_bp.route("/edit_message", methods=["POST"])
@jwt_required()
def edit_message():
    return edit_message_service(request=request)