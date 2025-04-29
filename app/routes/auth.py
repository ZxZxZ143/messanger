from flask import Flask, render_template, request, jsonify, redirect, blueprints, Blueprint
from flask_jwt_extended import jwt_required

from app.services.auth_service import register_user, login_user


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


@auth_bp.route('/check_token', methods=['POST'])
@jwt_required()
def check_token():
    return jsonify({"status": 200, "message": "token for user valid"}), 200
