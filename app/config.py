import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "super key"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or 'sqlite:///db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ADMIN = ["jlava402@gmail.com"]
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ORDERS_AMOUNT = int(os.environ.get('ORDERS_AMOUNT') or 25)
