from re import search

from flask import jsonify
from flask_jwt_extended import get_jwt, create_access_token, get_jwt_identity

from app import db
from app.models.User import Users
from app.models.contacts import Contacts
from app.utils.update_jwt import set_jwt_cookies


def get_new_users_service(request):
    user_id = get_jwt().get('id')
    param = request.get_json().get('username')
    contact_ids = db.session.query(Contacts.contact_id).filter_by(user_id=user_id).all()
    contact_ids = [cid for (cid,) in contact_ids]

    # Основной запрос: пользователи, которых нет в этом списке и не ты сам
    users = Users.query.filter(
        Users.id.notin_(contact_ids),
        Users.id != user_id,
        Users.username.ilike(f"%{param}%")
    ).all()

    res = []

    for u in users:
        res.append({"id": u.id, "username": u.username})
    print(res)
    resp = jsonify({"users": res})

    return set_jwt_cookies(resp)

def get_contacts():
    user_id = get_jwt().get('id')

    users_id = Contacts.query.filter_by(user_id=user_id, status="accepted").all()

    response = []

    for id in users_id:
        user = Users.query.filter_by(id=id.contact_id).first()

        response.append({"id": user.id, "username": user.username})

    res = jsonify({"status": 200, "contacts": response})

    return set_jwt_cookies(res)


def get_pending_contacts():
    user_id = get_jwt().get('id')

    users_id = Contacts.query.filter_by(user_id=user_id, status="pending").all()

    response = []

    for id in users_id:
        user = Users.query.filter_by(id=id.contact_id).first()

        response.append({"id": user.id, "username": user.username})

    res = jsonify({"status": 200, "contacts": response})

    return set_jwt_cookies(res)

def add_contacts(request):
    user_id = get_jwt().get('id')
    contact_id = request.get_json().get('contact_id')

    new_contacts = Contacts(user_id=user_id, contact_id=contact_id)
    new_contacts_for_user = Contacts(user_id=contact_id, contact_id=user_id)

    db.session.add(new_contacts)
    db.session.add(new_contacts_for_user)
    db.session.commit()

    res = jsonify({"status": 200})

    return set_jwt_cookies(res)

def accept_contacts(request):
    user_id = get_jwt().get('id')
    contact_id = request.get_json().get('contact_id')

    Contacts.query.filter_by(user_id=user_id, contact_id=contact_id).update({"status": "accepted"})
    Contacts.query.filter_by(user_id=contact_id, contact_id=user_id).update({"status": "accepted"})
    db.session.commit()

    res = jsonify({"status": 200})
    return set_jwt_cookies(res)

def reject_contacts(request):
    user_id = get_jwt().get('id')
    contact_id = request.get_json().get('contact_id')

    Contacts.query.filter_by(user_id=user_id, contact_id=contact_id).update({"status": "blocked"})
    Contacts.query.filter_by(user_id=contact_id, contact_id=user_id).update({"status": "blocked"})
    db.session.commit()

    res = jsonify({"status": 200})
    return set_jwt_cookies(res)

