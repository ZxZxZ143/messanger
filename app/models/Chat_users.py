from app.extensions import db


class Chat_users(db.Model):
    __tablename__ = 'chat_users'

    chat_id = db.Column(
        db.Integer,
        db.ForeignKey("chats.id"),
        nullable=False,
        primary_key=True,
        autoincrement=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        primary_key=True,
        autoincrement=False
    )
