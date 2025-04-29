from flask import Blueprint, request, template_rendered, render_template
from flask_jwt_extended import jwt_required

from app.services.contact_service import get_contacts, add_contacts, accept_contacts, reject_contacts, \
    get_pending_contacts

contacts_bp = Blueprint('contacts', __name__, url_prefix='/contacts')


@contacts_bp.route('/add', methods=['GET'])
def add():
    return render_template(template_name_or_list='add_contact.html')


@contacts_bp.route('/status', methods=['GET'])
def status():
    return render_template(template_name_or_list='accept_contacts.html')

@contacts_bp.route('/get_contacts', methods=['post'])
@jwt_required()
def get_contact():
    return get_contacts()


@contacts_bp.route('/get_pending_contacts', methods=['post'])
@jwt_required()
def get_pending_contact():
    return get_pending_contacts()


@contacts_bp.route('/add_contacts', methods=['POST'])
@jwt_required()
def add_contact():
    return add_contacts(request)


@contacts_bp.route('/accept_contacts', methods=['POST'])
@jwt_required()
def accept_contact():
    return accept_contacts(request)


@contacts_bp.route('/reject_contacts', methods=['POST'])
@jwt_required()
def reject_contact():
    return reject_contacts(request)