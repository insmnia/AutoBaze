from datetime import datetime
from app import db, login_manager
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


stops_table = db.Table("stops_table", db.Model.metadata,
                       db.Column("order_id", db.Integer,
                                 db.ForeignKey("order.id")),
                       db.Column("stop_id", db.Integer,
                                 db.ForeignKey("stop.id"))
                       )


class Stop(db.Model):
    __tablename__ = "stop"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        return self.name


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    FCs = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(30), nullable=False)
    departure_point = db.Column(db.String(40), nullable=False)
    arrival_point = db.Column(db.String(40), nullable=False)
    order_type = db.Column(db.String(15), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date())
    amount = db.Column(db.Integer)
    state = db.Column(db.String(10), nullable=False)
    creator = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    stops = db.relationship(
        "Stop", secondary=stops_table
    )

    def change_state(self, new_state):
        self.state = new_state

    def __repr__(self):
        return f"{self.id}, {self.FCs}, {self.phone}, {self.email}, {self.date}, {self.order_type}, {self.amount}"

    def __str__(self):
        return f"{self.id}, {self.FCs}, {self.phone}, {self.email}, {self.date}, {self.order_type}, {self.amount}"

    def add_stop(self, stop):
        self.stops.append(stop)

    def remove_stop(self, stop):
        self.stops.remove(stop)


class Day(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False,
                     default=datetime.utcnow().date(), unique=True)
    orders_amount = db.Column(db.Integer, nullable=False, default=20)

    def __repr__(self):
        return f"{self.date} {self.orders_amount}"
