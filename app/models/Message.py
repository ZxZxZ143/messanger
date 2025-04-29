from app.extensions import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.String(80), db.ForeignKey("chats.id"), unique=False, nullable=False)
    sender_id = db.Column(db.String(80), db.ForeignKey("users.id"), unique=False, nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_edited = db.Column(db.Boolean, nullable=False, default=False)
