from flask import jsonify
from flask_jwt_extended import get_jwt

from app import db
from app.models.User import Users
from app.models.contacts import Contacts


def get_contacts():
    user_id = get_jwt().get('id')

    users_id = Contacts.query.filter_by(user_id=user_id, status="accepted").all()

    response = []

    for id in users_id:
        user = Users.query.filter_by(id=id.contact_id).first()

        response.append({"id": user.id, "username": user.username})

    return jsonify({"status": 200, "contacts": response}), 200


def get_pending_contacts():
    user_id = get_jwt().get('id')

    users_id = Contacts.query.filter_by(user_id=user_id, status="pending").all()

    response = []

    for id in users_id:
        user = Users.query.filter_by(id=id.contact_id).first()

        response.append({"id": user.id, "username": user.username})

    return jsonify({"status": 200, "contacts": response}), 200

def add_contacts(request):
    user_id = get_jwt().get('id')
    contact_id = request.get_json().get('contact_id')

    new_contacts = Contacts(user_id=user_id, contact_id=contact_id)
    new_contacts_for_user = Contacts(user_id=contact_id, contact_id=user_id)

    db.session.add(new_contacts)
    db.session.add(new_contacts_for_user)
    db.session.commit()

    return jsonify({"status": 200}), 200

def accept_contacts(request):
    user_id = get_jwt().get('id')
    contact_id = request.get_json().get('contact_id')

    Contacts.query.filter_by(user_id=user_id, contact_id=contact_id).update({"status": "accepted"})
    Contacts.query.filter_by(user_id=contact_id, contact_id=user_id).update({"status": "accepted"})
    db.session.commit()
    return jsonify({"status": 200}), 200

def reject_contacts(request):
    user_id = get_jwt().get('id')
    contact_id = request.get_json().get('contact_id')

    Contacts.query.filter_by(user_id=user_id, contact_id=contact_id).update({"status": "blocked"})
    Contacts.query.filter_by(user_id=contact_id, contact_id=user_id).update({"status": "blocked"})
    db.session.commit()
    return jsonify({"status": 200}), 200

