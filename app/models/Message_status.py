from datetime import datetime

from sqlalchemy import ForeignKey

from app import db


class Message_status(db.Model):
    __tablename__ = 'message_statuses'
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)