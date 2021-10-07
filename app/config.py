import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "super key"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or 'postgresql://qpqxirbjyzkgcg:6082925c15718d6ced6197e13b409327c514d61e04781cc763b4e27c99949923@ec2-54-172-169-87.compute-1.amazonaws.com:5432/ddo4ed5g58tunt'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ADMIN = ["autobazehelp@yandex.ru"]
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ORDERS_AMOUNT = int(os.environ.get('ORDERS_AMOUNT') or 20)
