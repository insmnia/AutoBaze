import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "super key"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI') or 'postgresql://nhmzonsxmrjxdv:9691e189db82b72c14e194ee2f85c20d680d6062d338eaca91394efbe07bcbe6@ec2-52-7-228-45.compute-1.amazonaws.com:5432/d5d51dg6r2gpl0'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ADMIN = ["jlava402@gmail.com"]
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ORDERS_AMOUNT = int(os.environ.get('ORDERS_AMOUNT') or 20)
