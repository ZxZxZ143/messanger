from datetime import timedelta

from flask_mail import Mail, Message
from flask import Flask, render_template, request, jsonify, redirect, blueprints, Blueprint, url_for
from flask_jwt_extended import jwt_required, create_access_token, decode_token

from app.extensions import mail, db
from app.models.User import Users
from app.services.auth_service import register_user, login_user, refresh_service, hash_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET'])
def registerPage():
    return render_template(template_name_or_list="register.html")


@auth_bp.route('/login', methods=['GET'])
def loginPage():
    return render_template(template_name_or_list="login.html")


@auth_bp.route('/logout', methods=['POST'])
def logout():
    return redirect("/login?logout=success")


@auth_bp.route('/register', methods=['POST'])
def register():
    return register_user(request)


@auth_bp.route('/login', methods=['POST'])
def login():
    return login_user(request)


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    return refresh_service(request)


@auth_bp.route('/forgot_pass', methods=['GET'])
def forgot_password():
    return render_template(template_name_or_list="forgot_pass.html")

@auth_bp.route('/send_email', methods=['POST'])
def send_email():
    print(1)
    email = request.get_json()['email']
    msg = Message("Password Reset Request", recipients=[email], reply_to='nonreply@example.com')
    token = create_access_token(identity=email, expires_delta=timedelta(minutes=15))

    url = url_for('auth.reset_password', _external=True, token=token)

    msg.body = f"""
    вот ссылочка, возрадуйся, ты теперь сможешь зайти на аккаунт сын шлюхи, который забыл свой пароль
        {url}
        """
    msg.sender = 'nonreply@example.com'
    mail.send(msg)
    return jsonify({'status': 'success'})

@auth_bp.route('/check_token', methods=['POST'])
@jwt_required()
def check_token():
    return jsonify({"status": 200, "message": "token for user valid"}), 200

@auth_bp.route('/reset_password', methods=['GET'])
def reset_password():
    token = request.args.get("token")
    token = decode_token(token)
    if token is None:
        return render_template(template_name_or_list="reset_peassword_exp.html")
    token = token["sub"]
    user = Users.query.filter_by(email=token).first()
    if user is None:
        return render_template(template_name_or_list="login.html")
    return render_template(template_name_or_list="reset_password.html")

@auth_bp.route('/reset_password', methods=['POST'])
def reset_password_post():
    password = request.get_json().get("password")
    token = request.get_json().get("token")
    email = decode_token(token)["sub"]

    user = Users.query.filter_by(email=email).first()

    try:
        user.password = password
        user.password_hash = hash_password(password)

        db.session.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        print(e)
        return jsonify({"status": "fail"})