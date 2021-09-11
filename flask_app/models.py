from datetime import datetime
from flask_app import db, login_manager
from flask_login import UserMixin
from flask import current_app as app
from time import time
import jwt


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    passwords = db.relationship("Password", backref="author", lazy=True)

    def __repr__(self):
        return f"{self.id} {self.username} {self.email} {self.password}"

    def change_email(self, new_email):
        self.email = new_email

    def set_password(self, password):
        self.password = password

    def get_reset_password_token(self, expires=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time()+expires},
            app.config["SECRET_KEY"], algorithm="HS256"
        )

    @staticmethod
    def verify_token(token):
        try:
            id = jwt.decode(
                token, app.config["SECRET_KEY"],
                algorithms=["HS256"]
            )['reset_password']
        except:
            return
        return User.query.get(id)


class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    password_name = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    password_content = db.Column(db.String(120), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"{self.id} {self.password_name} {self.date_added} {self.password_content}"

    def change_password(self, new_password):
        self.password_content = new_password
