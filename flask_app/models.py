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
    orders = db.relationship("Order", backref="author", lazy=True)
    manager = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.username} {self.manager}"

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


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FCs = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    departure_point = db.Column(db.String(40), nullable=False)
    arrival_point = db.Column(db.String(40), nullable=False)
    order_type = db.Column(db.String(15), nullable=False)
    # TODO поменять на Date
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    amount = db.Column(db.Integer)
    state = db.Column(db.String(10), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def change_state(self, new_state):
        self.state = new_state

    def __repr__(self):
        return ""


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False,
                     default=datetime.utcnow().date(), unique=True)
    orders_amount = db.Column(db.Integer, nullable=False, default=20)

    def __repr__(self):
        return f"{self.date} {self.orders_amount}"
