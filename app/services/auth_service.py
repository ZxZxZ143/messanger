from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, \
    get_jwt_identity, get_jwt

from app.models.User import Users
from app.extensions import bcrypt, db


def register_user(request):
    if Users.query.filter_by(username=request.form['username']).first() is None:
        if request.form['password'] != "" and request.form['username'] != "" and request.form['email'] != "":
            new_user = Users(
                username=request.form['username'],
                email=request.form['email'],
                password=request.form['password'],
                password_hash=hash_password(request.form['password']))
            db.session.add(new_user)
            db.session.commit()

            access_token = create_access_token(identity=new_user.username, additional_claims={"id": new_user.id})
            refresh_token = create_refresh_token(identity=new_user.username, additional_claims={"id": new_user.id})
            res = jsonify({"status": 200, "message": "reg success", "user_id": new_user.id})
            set_access_cookies(res, access_token)
            set_refresh_cookies(res, refresh_token)

            return res, 200
        else:
            return jsonify({"status": 401, "message": "reg failed"}), 401
    else:
        return jsonify({"status": 401, "message": "Login already exists"}), 401


def login_user(request):
    username = request.form['username']
    password = request.form['password']

    user = Users.query.filter_by(username=username).first()
    if user is None:
        return jsonify({"status": 401, "message": "login doesn`t exist"}), 401

    if check_password(password, user.password_hash):
        access_token = create_access_token(identity=username, additional_claims={"id": user.id})
        refresh_token = create_refresh_token(identity=username, additional_claims={"id": user.id})

        res = jsonify({"status": 200, "message": "login success", "user_id": user.id})

        set_access_cookies(res, access_token)
        set_refresh_cookies(res, refresh_token)

        return res, 200

    return jsonify({"status": 401, "message": "Wrong data"}), 401


def refresh_service(request):
    try:
        user_name = get_jwt_identity()
        user_id = get_jwt().get('id')
        res = jsonify({"status": 200, "message": "refresh success"})

        access_token = create_access_token(identity=user_name, additional_claims={"id": user_id})
        refresh_token = create_refresh_token(identity=user_name, additional_claims={"id": user_id})

        set_access_cookies(res, access_token)
        set_refresh_cookies(res, refresh_token)

        return res, 200
    except Exception as e:
        print(e)
        return jsonify({"status": 401, "message": "refresh failed"}), 401

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_password(password, hashed):
    return bcrypt.check_password_hash(hashed, password)
