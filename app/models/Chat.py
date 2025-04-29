from app.extensions import db


class Chat(db.Model):
    __tablename__ = 'chats'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    is_group = db.Column(db.Boolean, default=False, nullable=False)
